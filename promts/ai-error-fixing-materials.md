# Материалы для статьи: "Как я научил ИИ чинить баги в продакшене за меня"

## Метаданные

```yaml
platform: habr
title: "Как я научил ИИ чинить баги в продакшене за меня"
subtitle: "Автоматизация исправления ошибок с Claude Code: от логирования до фикса одной командой"
author: Igor Maslennikov
date: 2026-01-18
tags: [Claude Code, AI, Error Handling, Automation, DevOps, Logging, Supabase, TypeScript]
language: ru
length: ~20000-25000 characters
```

---

## TL;DR (для спойлера в начале)

Я построил систему, где одна команда `/process-logs` в терминале:
1. Достаёт новые ошибки из базы данных
2. Анализирует root cause каждой
3. Создаёт задачу в трекере
4. Делегирует исправление специализированному ИИ-агенту
5. Верифицирует фикс (type-check, build)
6. Помечает ошибку как resolved
7. Записывает, что было исправлено

**Результат:** Ошибка в продакшене → фикс в коде за 2-5 минут. Без моего участия, кроме запуска команды и финального ревью.

**Репозиторий:** [github.com/maslennikov-ig/claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit)

---

## Персональный контекст

Игорь Масленников, IT с 2013, последние 2 года в AI Dev Team (DNA IT). Развиваю Claude Code Orchestrator Kit — open-source набор агентов и скиллов для Claude Code.

У меня 6 проектов на Claude Code. Каждый — это Next.js + Supabase + куча бизнес-логики. И в каждом есть баги. Потому что баги есть везде.

Раньше я тратил часы на:
- Чтение логов
- Поиск места в коде
- Понимание контекста
- Написание фикса
- Проверку, что ничего не сломал

Теперь это делает ИИ. А я просто смотрю, что он наделал, и жму "merge".

---

## Проблема: Баги в продакшене — это неизбежность

### Реальность разработки

Сколько бы ты ни писал тесты, баги будут. Причины:

1. **Edge cases** — пользователи делают то, что ты не предусмотрел
2. **Внешние сервисы** — API падают, таймауты, 500-ки
3. **Данные** — форматы меняются, null там, где не ждали
4. **Race conditions** — параллельные запросы ломают логику

### Типичный день без автоматизации

```
09:00 — Пришёл на работу, открыл логи
09:15 — "Error: Cannot read properties of undefined"
09:30 — Нашёл файл, где падает
09:45 — Понял контекст (читаю соседние файлы)
10:00 — Написал фикс
10:15 — Проверил type-check, билд
10:20 — Закоммитил
10:25 — Следующая ошибка...
```

**25 минут на один баг.** 5 багов в день — это 2 часа. Каждый день.

---

## Решение: Система автоматизированного исправления ошибок

### Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                     Production App                          │
│                                                             │
│  ┌───────────┐    ┌───────────┐    ┌───────────────────┐   │
│  │ tRPC API  │───▶│  Logger   │───▶│  error_logs (DB)  │   │
│  └───────────┘    └───────────┘    └───────────────────┘   │
│                                                             │
│  ┌───────────┐    ┌───────────┐    ┌───────────────────┐   │
│  │  BullMQ   │───▶│  Logger   │───▶│ generation_trace  │   │
│  │  Workers  │    └───────────┘    │      (DB)         │   │
│  └───────────┘                     └───────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Admin Panel /admin/logs                  │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Grouped View    │   List View    │   Realtime Updates │ │
│  │  (fingerprint)   │   (individual) │   (Supabase RT)   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  Статусы: new → in_progress → resolved                     │
│           └──────→ to_verify ──┘                           │
│           └──────→ ignored                                 │
│           └──────→ auto_muted (системный)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    /process-logs Command                    │
│                                                             │
│  1. SELECT * FROM error_logs WHERE status = 'new'          │
│  2. FOR EACH error:                                        │
│     - Создать Beads task                                   │
│     - Делегировать субагенту                               │
│     - Верифицировать фикс                                  │
│     - UPDATE status = 'resolved'                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Компонент 1: Логирование ошибок

### Структура таблицы error_logs

```sql
CREATE TABLE error_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT now(),

  -- Контекст ошибки
  error_message TEXT NOT NULL,
  stack_trace TEXT,
  severity TEXT CHECK (severity IN ('WARNING', 'ERROR', 'CRITICAL')),
  environment TEXT CHECK (environment IN ('dev', 'stage')),

  -- Привязка к сущностям
  course_id UUID REFERENCES courses(id),
  lesson_id UUID REFERENCES lessons(id),
  organization_id UUID REFERENCES organizations(id),
  user_id UUID REFERENCES auth.users(id),

  -- Для tRPC ошибок
  request_id TEXT,           -- nanoid для трейсинга
  trpc_path TEXT,            -- 'lessonContent.approve'
  trpc_input JSONB,          -- sanitized input
  attempted_value TEXT,      -- значение, которое вызвало ошибку

  -- Для BullMQ ошибок
  job_id TEXT,
  job_type TEXT,

  -- Группировка
  fingerprint TEXT,          -- MD5 hash для дедупликации
  problem_id TEXT,           -- human-readable ID: '2025-01-13#42'

  -- Метаданные
  metadata JSONB
);
```

### Сервис логирования

```typescript
// packages/course-gen-platform/src/shared/logger/error-service.ts

export async function logPermanentFailure(params: CreateErrorLogParams): Promise<void> {
  const supabase = getSupabaseAdmin();

  // Auto-detect environment
  const environment = params.environment || detectEnvironment();

  const logData = {
    error_message: params.error_message,
    stack_trace: params.stack_trace || null,
    severity: params.severity,
    environment,
    course_id: params.course_id || null,
    lesson_id: params.lesson_id || null,
    // ... rest of fields
  };

  // Upsert if problem_id provided (для идемпотентности при ретраях)
  if (params.problem_id) {
    await supabase
      .from('error_logs')
      .upsert(logData, { onConflict: 'problem_id' });
  } else {
    await supabase
      .from('error_logs')
      .insert(logData);
  }

  // Check for auto-mute
  const autoMuteResult = shouldAutoMute(params.error_message);
  if (autoMuteResult.mute) {
    await applyAutoMuteStatus(logId, params.error_message);
  }
}
```

### Fingerprinting для группировки

Одна и та же ошибка может случиться 100 раз за час. Без группировки — это 100 отдельных записей.

```typescript
// packages/course-gen-platform/src/shared/logger/fingerprint.ts

export function generateFingerprint(message: string, stack?: string): string {
  // Нормализация — убираем динамические значения
  const normalizedMessage = message
    // UUID → <UUID>
    .replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '<UUID>')
    // Timestamps → <TIMESTAMP>
    .replace(/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/g, '<TIMESTAMP>')
    // Large numbers → <NUM>
    .replace(/\b\d{3,}\b/g, '<NUM>')
    .trim()
    .toLowerCase();

  // Из стека берём только первую строку (тип ошибки)
  const firstStackLine = stack?.split('\n')[0] || '';

  return crypto
    .createHash('md5')
    .update(`${normalizedMessage}|||${firstStackLine}`)
    .digest('hex');
}
```

**Результат:** 100 одинаковых ошибок = 1 группа с count: 100.

---

## Компонент 2: Auto-Mute для ожидаемых ошибок

Не все ошибки — баги. Некоторые — нормальное поведение системы.

### Примеры ожидаемых "ошибок"

| Паттерн | Причина | Почему не баг |
|---------|---------|---------------|
| `Redis connection ended` | graceful_shutdown | Redis отключается при рестарте приложения |
| `/health 404` | monitoring_probe | Health-чеки от Uptime Kuma |
| `Cloudflare 502` | external_service | Проблемы Cloudflare, не наши |
| `Job stalled` | job_lifecycle | BullMQ рестартит долгие LLM-операции |
| `Layer failed, trying next` | cascading_repair | Repair layers работают как задумано |

### Реализация auto-mute

```typescript
// packages/course-gen-platform/src/shared/logger/auto-classification.ts

export const AUTO_MUTE_RULES: AutoMuteRule[] = [
  // Graceful Shutdown
  {
    pattern: /Redis connection (ended|closed)/i,
    reason: 'graceful_shutdown',
    description: 'Redis disconnects during app restart - normal behavior',
  },
  {
    pattern: /graceful.*shutdown/i,
    reason: 'graceful_shutdown',
    description: 'Server shutdown events - expected during deploys',
  },

  // Monitoring Probes
  {
    pattern: /\/api\/trpc\/health.*404/i,
    reason: 'monitoring_probe',
    description: 'Health endpoint probes from monitoring tools',
  },

  // External Services
  {
    pattern: /Cloudflare.*5\d{2}/i,
    reason: 'external_service',
    description: 'Cloudflare edge errors - not our bug',
  },

  // Cascading Repair System
  {
    pattern: /Layer failed, trying next/i,
    reason: 'cascading_repair',
    description: 'Repair layer escalation - expected behavior',
  },

  // ... ещё 8 правил
];

export function shouldAutoMute(errorMessage: string): AutoMuteResult {
  for (const rule of AUTO_MUTE_RULES) {
    if (rule.pattern.test(errorMessage)) {
      return {
        mute: true,
        reason: rule.reason,
        description: rule.description,
      };
    }
  }
  return { mute: false };
}
```

**Результат:** ~30% ошибок автоматически игнорируются. Я вижу только настоящие баги.

---

## Компонент 3: Админка для логов

### UI с realtime-обновлениями

```tsx
// packages/web/app/[locale]/admin/logs/components/logs-page-client.tsx

export function LogsPageClient() {
  return (
    <LogsErrorBoundary>
      <LogsRealtimeProvider>
        <LogsPageContent />
      </LogsRealtimeProvider>
    </LogsErrorBoundary>
  );
}

function LogsPageContent() {
  const { refreshTrigger, hasNewLogs } = useLogsRealtime();
  const [viewMode, setViewMode] = useState<'grouped' | 'list'>('grouped');

  return (
    <div className="flex h-full flex-col space-y-4">
      {/* Индикатор новых ошибок */}
      {hasNewLogs && (
        <Button onClick={requestRefresh}>
          Show new logs
        </Button>
      )}

      {/* Фильтры */}
      <FilterBar
        viewMode={viewMode}
        onViewModeChange={setViewMode}
      />

      {/* Таблица — grouped или list */}
      {viewMode === 'grouped' ? (
        <GroupedLogTable filters={filters} />
      ) : (
        <LogTable filters={filters} />
      )}

      {/* Drawer с деталями */}
      <LogDetailDrawer />
    </div>
  );
}
```

### Realtime через Supabase

```typescript
// packages/web/app/[locale]/admin/logs/components/logs-realtime-provider.tsx

export function LogsRealtimeProvider({ children }: Props) {
  const [hasNewLogs, setHasNewLogs] = useState(false);

  useEffect(() => {
    const channel = supabase
      .channel('error_logs_changes')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'error_logs' },
        () => setHasNewLogs(true)
      )
      .subscribe();

    return () => { channel.unsubscribe(); };
  }, []);

  return (
    <LogsRealtimeContext.Provider value={{ hasNewLogs, ... }}>
      {children}
    </LogsRealtimeContext.Provider>
  );
}
```

**Результат:** Новая ошибка в продакшене → уведомление в админке через ~1 секунду.

---

## Компонент 4: Команда /process-logs

Это сердце системы. Одна команда, которая делает всю работу.

### Workflow

```markdown
# .claude/skills/process-logs/SKILL.md

## Workflow

### Step 1: Fetch New Errors

```sql
-- Получить новые ошибки (исключая auto_muted)
SELECT el.id, el.severity, el.error_message, el.stack_trace,
       el.course_id, el.trpc_path, el.trpc_input
FROM error_logs el
LEFT JOIN log_issue_status lis ON lis.log_id = el.id
WHERE lis.id IS NULL
   OR lis.status NOT IN ('resolved', 'ignored', 'auto_muted')
ORDER BY
  CASE el.severity
    WHEN 'CRITICAL' THEN 1
    WHEN 'ERROR' THEN 2
    ELSE 3
  END,
  el.created_at DESC
LIMIT 20;
```

### Step 2: For EACH Error

```
FOR each error:
  1. CREATE BEADS TASK (трекер):
     bd create --type=bug --title="Fix: <error_message>"
     bd update <id> --status=in_progress

  2. ANALYZE error type → SELECT subagent:
     - DB constraint → database-architect
     - tRPC/API → fullstack-nextjs-specialist
     - Types → typescript-types-specialist
     - UI → nextjs-ui-designer

  3. QUERY context7 for relevant docs

  4. DELEGATE using Task tool:
     Task(subagent_type="<selected>", prompt="Fix error...")

  5. VERIFY results:
     - Read modified files
     - pnpm type-check && pnpm build
     - If errors → re-delegate

  6. MARK resolved in DB:
     INSERT INTO log_issue_status (log_type, log_id, status, notes)
     VALUES ('error_log', '<id>', 'resolved', 'Fixed: <description>')
     ON CONFLICT DO UPDATE...

  7. CLOSE Beads task:
     bd close <id> --reason="Fixed"
```
```

### Субагенты для разных типов ошибок

| Паттерн ошибки | Субагент | Когда использовать |
|----------------|----------|-------------------|
| `violates.*constraint` | `database-architect` | DB constraint violations |
| `tRPC error` | `fullstack-nextjs-specialist` | API bugs |
| `Type.*error` | `typescript-types-specialist` | TypeScript issues |
| `Error querying` | `database-architect` | Query bugs |
| Config missing | **ASK USER** | Нужен ввод человека |
| External service | mark `to_verify` | Мониторим 24h |

### Пример делегирования

```typescript
// Ошибка: "violates check constraint on lesson_status"
// Субагент: database-architect

Task(
  subagent_type="database-architect",
  prompt=`Fix DB constraint violation in error_logs.

  Error: violates check constraint "lesson_status_check"

  Context:
  - Table: lessons
  - Column: status
  - Attempted value: 'approved'
  - Current valid values: draft, generating, generated, error

  Stack trace:
  at LessonContentRouter.approve (routers/lesson-content.ts:142)

  Task:
  1. Create migration to add 'approved' to lesson_status enum
  2. Update any TypeScript types if needed
  3. Verify type-check passes`
)
```

### Обязательные notes

Каждая resolved ошибка получает notes с описанием:

| Status | Format notes |
|--------|-------------|
| `resolved` | `<root_cause>. <action_taken>.` |
| `to_verify` | `<why_pending>. <what_to_check>.` |
| `in_progress` | `Working on mc2-5ch` |

**Примеры:**
- `ESM import conflict. Renamed generator.ts to generator-node.ts.`
- `Constraint missing 'approved'. Added via migration.`
- `Cloudflare 500. External issue, monitoring.`

---

## Реальный пример работы

### Входные данные

```
Error: violates check constraint "generation_status_check"
Severity: ERROR
tRPC Path: lessonContent.approveLesson
Attempted Value: approved
Stack: at LessonContentRouter.approve (lesson-content.ts:142)
```

### Процесс

```bash
$ /process-logs

# Step 1: Fetch errors
Found 3 new errors (1 CRITICAL, 2 ERROR)

# Step 2: Process first error
Creating Beads task: mc2-7x9 "Fix: constraint violation on lesson_status"
Delegating to: database-architect

# Субагент работает...
# - Читает схему БД
# - Создаёт миграцию
# - Обновляет типы

# Step 3: Verify
✓ pnpm type-check - passed
✓ pnpm build - passed

# Step 4: Mark resolved
UPDATE log_issue_status SET status = 'resolved',
  notes = 'Missing approved status. Added via migration.'

# Step 5: Close task
bd close mc2-7x9 --reason="Fixed"

# Repeat for remaining errors...

## Summary
| Severity | Fixed | Pending | To Verify |
|----------|-------|---------|-----------|
| CRITICAL | 1     | 0       | 0         |
| ERROR    | 2     | 0       | 0         |

Beads Tasks: mc2-7x9, mc2-7xa, mc2-7xb - all resolved
```

**Время:** 3 ошибки за ~8 минут. Я только запустил команду и проверил результат.

---

## Поиск похожих решённых проблем

Перед фиксом ИИ проверяет, решали ли мы это раньше:

```sql
-- Search similar resolved errors
SELECT el.id, el.error_message, lis.notes, el.created_at
FROM error_logs el
JOIN log_issue_status lis ON lis.log_id = el.id
WHERE to_tsvector('english', el.error_message)
      @@ plainto_tsquery('english', 'constraint')
  AND lis.status = 'resolved'
ORDER BY el.created_at DESC
LIMIT 5;
```

**Если нашли:** Применяем тот же паттерн решения.

---

## Статистика: До и После

### Время на исправление ошибок

| Метрика | До автоматизации | После автоматизации |
|---------|------------------|---------------------|
| Среднее время на 1 баг | 25 минут | 3 минуты |
| Багов в день | 5 | 5 |
| Времени на баги в день | 2+ часа | 15 минут |
| Времени на баги в неделю | 10+ часов | 1-2 часа |

### Качество исправлений

| Метрика | До | После |
|---------|-----|-------|
| Root cause найден | ~70% | ~95% |
| Документация фикса | Редко | Всегда (notes) |
| Повторные баги | Часто | Редко (поиск похожих) |

---

## Следующий уровень: Полная автоматизация

### Что можно добавить

1. **Автозапуск при новой ошибке**
   ```typescript
   // Supabase trigger → Edge Function → /process-logs
   CREATE OR REPLACE FUNCTION notify_new_error()
   RETURNS trigger AS $$
   BEGIN
     PERFORM pg_notify('new_error', NEW.id::text);
     RETURN NEW;
   END;
   $$ LANGUAGE plpgsql;
   ```

2. **Отчёт тестерам**
   ```
   🐛 Bug Fixed Automatically

   Error: constraint violation on lesson_status
   Root cause: Missing 'approved' status in enum
   Fix: Migration 20250118_add_approved_status.sql

   Status: ✅ Fixed and deployed
   Commit: abc123
   ```

3. **Метрики в Grafana**
   - Время от ошибки до фикса
   - Процент автоматических исправлений
   - Топ-10 recurring ошибок

### Почему я пока не автоматизирую полностью

**Контроль важнее скорости.**

- Хочу видеть, что ИИ делает
- Хочу ревьюить фиксы перед мержем
- Хочу понимать паттерны ошибок

Полная автоматизация — это следующий этап. Когда доверие к системе вырастет.

---

## Применимость к другим проектам

### Минимальная версия (любой проект)

1. Таблица `error_logs` в БД
2. Логгер, который пишет в неё
3. Команда для Claude Code

**Подходит для:** Pet-проекты, небольшие проекты, MVP.

### Продвинутая версия (как у меня)

1. Два источника: `error_logs` + `generation_trace`
2. Fingerprinting для группировки
3. Auto-mute для ожидаемых ошибок
4. Realtime-обновления в админке
5. Интеграция с трекером (Beads)
6. Субагенты для разных типов ошибок

**Подходит для:** Продакшен-проекты, команды, SaaS.

### Пример из другого проекта (BuhBot)

```typescript
// bobabuh/backend/src/services/logging/error-capture.service.ts

export class ErrorCaptureService {
  async captureError(options: ErrorCaptureOptions): Promise<void> {
    const fingerprint = this.generateFingerprint(
      options.message,
      options.stack
    );

    // Дедупликация: проверяем за последние 24 часа
    const existing = await prisma.errorLog.findFirst({
      where: {
        fingerprint,
        timestamp: { gte: twentyFourHoursAgo }
      }
    });

    if (existing) {
      // Update occurrence count
      await prisma.errorLog.update({
        where: { id: existing.id },
        data: {
          occurrenceCount: { increment: 1 },
          lastSeenAt: new Date()
        }
      });
    } else {
      // Create new
      await prisma.errorLog.create({
        data: { fingerprint, message, ... }
      });
    }
  }
}
```

---

## Что это НЕ заменяет

**Важно понимать ограничения:**

1. ❌ **Не заменяет тесты** — превентивная защита лучше реактивной
2. ❌ **Не заменяет code review** — ИИ может наделать глупостей
3. ❌ **Не заменяет мониторинг** — нужно видеть метрики, не только логи
4. ❌ **Не ловит все баги** — только те, что попали в логи

**Это дополнение**, а не замена. Ещё один слой защиты.

---

## Что дальше

В следующей статье расскажу про:
- **Blue-Green деплой** — как мы деплоим без даунтайма
- **Dev и Staging окружения** — как изолируем изменения
- **CI/CD pipeline** — автоматизация от коммита до продакшена

**Если интересно — пишите в комментариях**, какие аспекты раскрыть подробнее.

---

## Где взять

**Репозиторий:** [github.com/maslennikov-ig/claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit)

**Что внутри:**
- Скилл `/process-logs` — готовый к использованию
- Примеры миграций для `error_logs`
- Auto-mute правила
- 36+ других агентов и скиллов

**Лицензия:** MIT

---

## Автор

**Игорь Масленников**
*AI-агенты, LLM-архитектура, автоматизация разработки.*

📢 **Telegram:** [@maslennikovigor](https://t.me/maslennikovigor) — бенчмарки, DevOps-лайфхаки, AI-новости
💬 **Личный контакт:** [@maslennikovig](https://t.me/maslennikovig)
🐙 **GitHub:** [maslennikov-ig](https://github.com/maslennikov-ig)

---

## P.S. для агента-автора

### Ключевые моменты статьи

1. **Главная идея:** Одна команда `/process-logs` → ИИ чинит баги автоматически
2. **Компоненты:** Логирование → Auto-mute → Админка → Обработка
3. **Практичность:** Конкретные примеры кода, SQL, конфигов
4. **Результат:** 2+ часа → 15 минут в день на баги

### Структура

- Начать с боли (баги занимают время)
- Показать решение (архитектура)
- Детали каждого компонента (с кодом)
- Реальный пример работы
- Статистика до/после
- Следующий уровень (полная автоматизация)
- Применимость к другим проектам

### Тон

- Первое лицо ("я сделал", "у меня работает")
- Практичность (код > теория)
- Честность (ограничения, что не заменяет)
- Без хайпа (не "революция", а "удобный инструмент")

### Избегать

- ❌ "В заключение хочется отметить..."
- ❌ "Подводя итоги..."
- ❌ "Данная технология позволяет..."
- ❌ Избыточные эмодзи

### Длина

20000-25000 символов — достаточно для глубокого погружения, но без воды.

---

## Технические детали для референса

### Файлы проекта

```
packages/course-gen-platform/src/shared/logger/
├── auto-classification.ts   # Auto-mute rules
├── auto-mute-service.ts     # Apply auto-mute status
├── error-service.ts         # logPermanentFailure()
├── types.ts                 # ErrorLog, ErrorSeverity
├── utils.ts                 # detectEnvironment()
└── index.ts                 # Export logger

packages/course-gen-platform/src/server/routers/admin/
└── logs.ts                  # tRPC router for admin logs

packages/web/app/[locale]/admin/logs/
├── page.tsx                 # Server component
└── components/
    ├── logs-page-client.tsx # Client component
    ├── log-table.tsx        # List view
    ├── grouped-log-table.tsx # Grouped view
    ├── filter-bar.tsx       # Filters
    └── log-detail-drawer.tsx # Details

.claude/skills/process-logs/
└── SKILL.md                 # Command definition
```

### SQL для создания таблиц

```sql
-- error_logs table
CREATE TABLE error_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT now(),
  error_message TEXT NOT NULL,
  stack_trace TEXT,
  severity TEXT CHECK (severity IN ('WARNING', 'ERROR', 'CRITICAL')),
  environment TEXT CHECK (environment IN ('dev', 'stage')),
  fingerprint TEXT,
  problem_id TEXT UNIQUE,
  course_id UUID,
  lesson_id UUID,
  organization_id UUID,
  user_id UUID,
  request_id TEXT,
  trpc_path TEXT,
  trpc_input JSONB,
  attempted_value TEXT,
  job_id TEXT,
  job_type TEXT,
  metadata JSONB
);

-- log_issue_status table
CREATE TABLE log_issue_status (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  log_type TEXT NOT NULL,
  log_id UUID NOT NULL,
  fingerprint TEXT,
  status TEXT CHECK (status IN ('new', 'in_progress', 'to_verify', 'resolved', 'ignored', 'auto_muted')),
  notes TEXT,
  updated_by UUID,
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(log_type, log_id)
);

-- Trigger for fingerprint sync
CREATE TRIGGER trg_sync_log_status_fingerprint
BEFORE INSERT OR UPDATE ON log_issue_status
FOR EACH ROW
EXECUTE FUNCTION sync_log_status_fingerprint();
```

### Beads integration

```bash
# Create task for error
bd create --type=bug --priority=2 --title="Fix: constraint violation" --files "packages/course-gen-platform/src/server/routers/lesson-content.ts"

# Start work
bd update mc2-7x9 --status=in_progress

# Complete
bd close mc2-7x9 --reason="Fixed via migration 20250118_add_approved_status.sql"
```

---

## Ссылки для агента-автора

### Ключевые файлы проекта (для референса)

**Логирование:**
- Auto-classification rules: `packages/course-gen-platform/src/shared/logger/auto-classification.ts`
- Error service: `packages/course-gen-platform/src/shared/logger/error-service.ts`
- Types: `packages/course-gen-platform/src/shared/logger/types.ts`
- Auto-mute service: `packages/course-gen-platform/src/shared/logger/auto-mute-service.ts`

**tRPC роутер:**
- Admin logs router: `packages/course-gen-platform/src/server/routers/admin/logs.ts`

**Админка (UI):**
- Logs page: `packages/web/app/[locale]/admin/logs/page.tsx`
- Client component: `packages/web/app/[locale]/admin/logs/components/logs-page-client.tsx`
- Realtime provider: `packages/web/app/[locale]/admin/logs/components/logs-realtime-provider.tsx`
- Log table: `packages/web/app/[locale]/admin/logs/components/log-table.tsx`
- Grouped table: `packages/web/app/[locale]/admin/logs/components/grouped-log-table.tsx`
- Detail drawer: `packages/web/app/[locale]/admin/logs/components/log-detail-drawer.tsx`

**Скилл process-logs:**
- SKILL.md: `.claude/skills/process-logs/SKILL.md`

**Миграции БД:**
- Fingerprint trigger: `packages/course-gen-platform/supabase/migrations/20260117100001_add_fingerprint_sync_trigger.sql`
- Error log fingerprint: `packages/course-gen-platform/supabase/migrations/20260117_add_error_log_fingerprint.sql`
- Grouped RPC: `packages/course-gen-platform/supabase/migrations/20260117100000_add_grouped_error_logs_rpc.sql`
- Log issue status: `packages/course-gen-platform/supabase/migrations/20251222150000_add_log_issue_status_table.sql`
- Enhanced error logs: `packages/course-gen-platform/supabase/migrations/20260113150000_enhance_error_logs_problem_id.sql`

**Документация:**
- Error log grouping feature: `docs/features/error-log-grouping.md`
- Admin logs guide: `.claude/docs/admin-logs-guide.md`
- Code review report: `docs/reports/code-review/2026-01/error-log-grouping-review.md`

**Альтернативный проект (BuhBot) для референса:**
- Error capture service: `/home/me/code/bobabuh/backend/src/services/logging/error-capture.service.ts`
- Logger: `/home/me/code/bobabuh/backend/src/utils/logger.ts`
- CLAUDE.md: `/home/me/code/bobabuh/CLAUDE.md`

**Blue-Green и Deployment:**
- ADR-004 Blue-Green: `docs/ADR-004-blue-green-deployment.md`
- ADR-005 Deployment Strategy: `docs/ADR-005-deployment-strategy.md`
- Deploy script: `scripts/deploy_blue_green.sh`
- Rollback script: `scripts/rollback_blue_green.sh`
- Deployment guide: `.claude/docs/deployment-guide.md`
- CI/CD workflow: `.github/workflows/ci-cd.yml`

### Внешние ссылки

**Open Source репозиторий:**
- GitHub: https://github.com/maslennikov-ig/claude-code-orchestrator-kit

**Telegram:**
- Канал автора: https://t.me/maslennikovigor
- Личный контакт: https://t.me/maslennikovig

**GitHub автора:**
- https://github.com/maslennikov-ig

### Технологии (для Context7 queries)

При необходимости агент может запросить документацию через Context7:
- **Supabase** — база данных, realtime, RLS
- **tRPC** — type-safe API
- **Next.js** — App Router, Server Components
- **BullMQ** — job queues
- **Pino** — structured logging
- **Zod** — validation schemas

### Примеры статей того же автора (для стиля)

- MCP Tool Search: `/home/me/code/articles/docs/promts/mcp-tool-search-materials.md`
