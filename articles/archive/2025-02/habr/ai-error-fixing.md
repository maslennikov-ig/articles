---
platform: habr
title: "2 часа в день на баги → 15 минут: автоматизация исправления ошибок в Claude Code"
subtitle: "Как одна команда /process-logs экономит 8 часов в неделю на исправлении багов"
author: Igor Maslennikov
date: 2026-01-18
tags: [Claude Code, AI, Error Handling, Automation, DevOps, Logging, Supabase, TypeScript]
language: ru
length: 22847 characters
---

# 2 часа в день на баги → 15 минут: автоматизация исправления ошибок в Claude Code

<spoiler title="TL;DR">

Я построил систему, где одна команда `/process-logs` в терминале:

1. Достаёт новые ошибки из базы данных
2. Анализирует root cause каждой
3. Создаёт задачу в трекере
4. Делегирует исправление специализированному ИИ-агенту
5. Верифицирует фикс (type-check, build)
6. Помечает ошибку как resolved
7. Записывает, что было исправлено

**Результат:** Ошибка в продакшене → фикс в коде за 2-5 минут. Без моего участия, кроме запуска команды и финального ревью.

**Репозиторий:** [github.com/maslennikov-ig/claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) (MIT License, 38+ агентов и скиллов)

</spoiler>

## Кто я и зачем мне это

Игорь Масленников, в IT с 2013 года, последние два года развиваю AI Dev Team в DNA IT. Занимаюсь Claude Code Orchestrator Kit — open-source набор агентов и скиллов для автоматизации разработки.

У меня 6 проектов на Claude Code. Каждый — это Next.js + Supabase + куча бизнес-логики. И в каждом есть баги. Потому что баги есть везде.

Раньше я тратил часы на:
- Чтение логов
- Поиск места в коде
- Понимание контекста
- Написание фикса
- Проверку, что ничего не сломал

Теперь это делает ИИ. А я просто смотрю, что он наделал, и жму merge.

## Проблема: Баги в продакшене — это неизбежность

### Реальность разработки

Сколько бы ты ни писал тесты, баги будут. Причины банальны:

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

Я понял, что это не про скорость кодирования. Это про рутину. А рутина отлично автоматизируется.

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

Система состоит из 4 компонентов:

1. **Логирование ошибок** — structured logging в базу данных
2. **Auto-Mute** — автоматическое игнорирование ожидаемых "ошибок"
3. **Админка** — UI с realtime-обновлениями для контроля
4. **Команда /process-logs** — автоматизация обработки

Разберём каждый компонент детально.

## Компонент 1: Логирование ошибок

### Структура таблицы error_logs

Первое, что я сделал — перестал логировать в файлы. Текстовые логи — это боль: их нужно парсить, искать по ним, группировать вручную.

Я создал таблицу `error_logs` в Supabase:

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
  problem_id TEXT UNIQUE,    -- human-readable ID: '2025-01-13#42'

  -- Метаданные
  metadata JSONB
);
```

**Почему важны все эти поля:**

- `severity` — приоритет обработки (CRITICAL → ERROR → WARNING)
- `environment` — dev или stage, чтобы не путать
- `fingerprint` — для группировки одинаковых ошибок (об этом ниже)
- `problem_id` — человекочитаемый ID для обсуждений ("Смотри баг 2025-01-13#42")
- `trpc_path` и `trpc_input` — для API-ошибок: сразу вижу, какой эндпоинт и с какими данными упал

### Сервис логирования

Я написал универсальную функцию `logPermanentFailure()`, которую вызываю из любого места кода:

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

**Где я это вызываю:**

1. **tRPC error handlers** — все API ошибки попадают в лог
2. **BullMQ job failures** — после исчерпания retry attempts
3. **Unhandled rejections** — глобальный обработчик на `process.on('unhandledRejection')`

### Fingerprinting для группировки

Одна и та же ошибка может случиться 100 раз за час. Без группировки — это 100 отдельных записей в админке. С ними невозможно работать.

Я использую fingerprinting — нормализацию сообщения об ошибке и создание MD5 хэша:

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

**Результат:** 100 одинаковых ошибок = 1 группа с count: 100 в админке.

### Problem ID: Человекочитаемый идентификатор

MD5 хэш — это хорошо для машины, но плохо для людей. Как обсуждать баги? "Смотри fingerprint `a3f5b2c...`"? Неудобно.

Я добавил `problem_id` — автоинкрементный ID в формате `YYYY-MM-DD#N`:

```sql
-- Trigger для auto-generation
CREATE OR REPLACE FUNCTION generate_problem_id()
RETURNS TEXT AS $$
DECLARE
    today DATE := CURRENT_DATE;
    seq_num INTEGER;
BEGIN
    INSERT INTO problem_id_sequences (date_key, next_sequence)
    VALUES (today, 1)
    ON CONFLICT (date_key) DO UPDATE
    SET next_sequence = problem_id_sequences.next_sequence + 1
    RETURNING next_sequence INTO seq_num;

    RETURN TO_CHAR(today, 'YYYY-MM-DD') || '#' || seq_num;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

Теперь в админке я вижу: `2025-01-13#42` вместо хэша. В беседе с коллегой: "Чекни баг 13-го января номер 42".

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

Если я буду чинить эти "ошибки", я потрачу время впустую. Поэтому я написал систему автоматического игнорирования.

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

  // Job Lifecycle
  {
    pattern: /Job stalled/i,
    reason: 'job_lifecycle',
    description: 'BullMQ job exceeded lock duration - expected for long LLM ops',
  },

  // ... ещё 7 правил
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

**Важно:** Я не удаляю auto-muted ошибки из базы. Они сохраняются со статусом `auto_muted`. Если паттерн изменится и ошибка станет реальной — я увижу историю.

## Компонент 3: Админка для логов

### UI с realtime-обновлениями

Я сделал админку `/admin/logs` с двумя режимами просмотра:

1. **Grouped View** — группировка по `fingerprint`, показывает count одинаковых ошибок
2. **List View** — все ошибки индивидуально, для детального анализа

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

Новая ошибка в продакшене → уведомление в админке через ~1 секунду:

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

**Результат:** Я вижу ошибки сразу, как они происходят. Не нужно обновлять страницу.

### Два источника данных

В моей системе ошибки приходят из двух таблиц:

1. **error_logs** — системные ошибки, tRPC, worker failures
2. **generation_trace** (где `error_data IS NOT NULL`) — LLM generation errors

Админка агрегирует обе таблицы. Статус хранится в `log_issue_status` с композитным ключом `(log_type, log_id)`.

**UI логика:** Если нет записи в `log_issue_status` → статус "Новый" (new).

## Компонент 4: Команда /process-logs

Это сердце системы. Одна команда, которая делает всю работу.

> **Что такое Skills в Claude Code?**
>
> Skills — это переиспользуемые workflow-файлы (`.claude/skills/*/SKILL.md`), которые Claude Code выполняет при вызове команды. В отличие от простых промптов, Skills содержат чёткие инструкции: какие SQL запросы выполнить, какие субагенты вызвать, как верифицировать результат. Skill `/process-logs` — это ~200 строк Markdown с детальным workflow, который ИИ следует шаг за шагом.

### Workflow

```markdown
### Step 1: Fetch New Errors

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

### Step 2: For EACH Error

FOR each error:
  1. CREATE BEADS TASK (трекер):
     bd create --type=bug --title="Fix: <error_message>"
     bd update <id> --status=in_progress

  2. ANALYZE error type → SELECT subagent:
     - DB constraint → database-architect
     - tRPC/API → fullstack-nextjs-specialist
     - Types → typescript-types-specialist
     - UI → nextjs-ui-designer

  3. QUERY Docs L1/L2 for relevant docs

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

### Субагенты для разных типов ошибок

Я не использую одного универсального агента. У меня есть специализированные субагенты для разных категорий багов:

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

Субагент:
1. Читает текущую схему БД
2. Создаёт миграцию `20250118_add_approved_status.sql`
3. Обновляет TypeScript типы (если нужно)
4. Проверяет, что type-check и build проходят

Я проверяю результат и закрываю задачу.

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

**Зачем:** Через месяц я забуду, что делал. Notes — это документация для будущего меня.

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

**Если нашли:** Применяем тот же паттерн решения. Записываем в notes: `Similar to 2025-01-10. Same fix applied.`

**Результат:** Повторяющиеся баги фиксятся ещё быстрее. Паттерны решений накапливаются в базе.

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

**Вывод:** Я освободил ~8 часов в неделю. Это один полный рабочий день. Каждую неделю.

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

Сейчас я экономлю 8 часов в неделю. Это уже огромный выигрыш. Полная автоматизация даст ещё 1-2 часа. Но добавит риск внести баг вместо исправления.

## Применимость к другим проектам

### Минимальная версия (любой проект)

1. Таблица `error_logs` в БД
2. Логгер, который пишет в неё
3. Команда для Claude Code

**Подходит для:** Pet-проекты, небольшие проекты, MVP.

**Время внедрения:** 2-3 часа (или скопируй готовый промпт из `prompts/setup-error-logging.md` — Claude Code сделает всё за тебя).

### Продвинутая версия (как у меня)

1. Два источника: `error_logs` + `generation_trace`
2. Fingerprinting для группировки
3. Auto-mute для ожидаемых ошибок
4. Realtime-обновления в админке
5. Интеграция с трекером (Beads)
6. Субагенты для разных типов ошибок

**Подходит для:** Продакшен-проекты, команды, SaaS.

**Время внедрения:** 1-2 недели (с учётом настройки всех компонентов).

### Пример из другого проекта (BuhBot)

Я использую ту же систему в другом проекте — BuhBot (бухгалтерский AI-бот):

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

Тот же паттерн, но на Prisma вместо Supabase. Работает отлично.

## Что это НЕ заменяет

**Важно понимать ограничения:**

1. ❌ **Не заменяет тесты** — превентивная защита лучше реактивной
2. ❌ **Не заменяет code review** — ИИ может наделать глупостей
3. ❌ **Не заменяет мониторинг** — нужно видеть метрики, не только логи
4. ❌ **Не ловит все баги** — только те, что попали в логи

**Это дополнение**, а не замена. Ещё один слой защиты.

**Мой workflow:**

1. **Пишу код** — с тестами, с ревью
2. **Деплою** — с мониторингом метрик
3. **Ловлю баги** — автоматически через `/process-logs`
4. **Улучшаю тесты** — чтобы баг не повторился

Автоматизация исправления багов — это последний слой. Если баг дошёл до продакшена — система его поймает и починит. Но лучше, если баг вообще не случится.

## Что дальше

В следующей статье расскажу про:
- **Blue-Green деплой** — как мы деплоим без даунтайма
- **Dev и Staging окружения** — как изолируем изменения
- **CI/CD pipeline** — автоматизация от коммита до продакшена

**Если интересно — пишите в комментариях**, какие аспекты раскрыть подробнее. Особенно интересно услышать:

- Как вы логируете ошибки в своих проектах?
- Автоматизируете ли что-то в баг-фиксинге?
- Сколько времени уходит на исправление багов в вашей команде?

## Где взять

**Репозиторий:** [github.com/maslennikov-ig/claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit)

**Что внутри:**
- **Skill `/process-logs`** — готовый к использованию (Claude Code Skills — это переиспользуемые workflow, которые ИИ выполняет при вызове команды)
- **Готовый промпт** `prompts/setup-error-logging.md` — скопируй, вставь, и ИИ настроит error logging в твоём проекте
- Примеры миграций для `error_logs`
- Auto-mute правила
- 38+ других агентов и скиллов

**Лицензия:** MIT (используйте как хотите, даже в коммерческих проектах)

**Установка:**

```bash
# Клонируйте репозиторий
git clone https://github.com/maslennikov-ig/claude-code-orchestrator-kit.git

# Переключите MCP конфиг (если нужен Supabase)
./switch-mcp.sh

# Перезапустите Claude Code
# Готово — команда /process-logs доступна
```

## Автор

**Игорь Масленnikov**
*AI-агенты, LLM-архитектура, автоматизация разработки.*

📢 **Telegram:** [@maslennikovigor](https://t.me/maslennikovigor) — бенчмарки, DevOps-лайфхаки, AI-новости (пишу редко, но по делу)
💬 **Личный контакт:** [@maslennikovig](https://t.me/maslennikovig)
🐙 **GitHub:** [maslennikov-ig](https://github.com/maslennikov-ig)

---

## Обратная связь

**Я открыт к диалогу:**

- **Критика** — Что не так с этим подходом? Где слабые места?
- **Идеи** — Что добавить? Что улучшить?
- **Вопросы** — Что непонятно? Спрашивайте.

**Где писать:**
- **GitHub Issues:** https://github.com/maslennikov-ig/claude-code-orchestrator-kit/issues (для багов, фичей, идей)
- **Telegram:** https://t.me/maslennikovig (для прямого общения)

**Тон:** Конструктивная критика приветствуется. Хочу сделать систему лучше.
