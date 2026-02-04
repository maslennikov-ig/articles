---
platform: habr
series: Claude Code Orchestrator Kit
part: 1 of 3
title: "Изоляция контекста через субагенты: архитектурный паттерн для долгосрочной работы с Claude Code"
author: Igor Maslennikov
date: 2025-11-11
length: 21847 characters
tags: [Claude Code, архитектура, AI-агенты, оркестрация, контекстное окно, TypeScript, MCP]
language: ru
---

# Изоляция контекста через субагенты: архитектурный паттерн для долгосрочной работы с Claude Code

*Как превратить Claude Code из мощного ассистента в профессиональную платформу оркестрации с 33+ специализированными агентами*

---

## Контекст: кто пишет и почему это важно

Игорь Масленников. В IT с 2013 года. Много лет управлял классической IT-компанией DNA IT. Последние два года активно развиваю подразделение AI Dev Team — и вижу интересную тенденцию: **всё больше клиентов выбирают именно это подразделение**. Не потому что модно, а потому что быстрее (1-2 недели вместо 2-3 месяцев), дешевле (минус 80% от стоимости), и, как ни странно, качественнее благодаря автоматическим проверкам.

Эта статья — о том, как мы организовали работу с Claude Code на уровне **архитектурных паттернов**, а не «промптинга». И почему это даёт измеримые результаты.

---

## Проблема: Claude Code быстро «выгорает»

Claude Code — мощный инструмент. Но при работе над реальным проектом быстро упирается в проблему: **контекстный бюджет**.

**Классический сценарий**:
1. Начинаете работу над проектом. Контекст: ~10K токенов.
2. Через 3-4 задачи: контекст раздулся до 30K токенов (история изменений, прошлые обсуждения).
3. Через неделю: 50K+ токенов. Claude Code начинает «забывать» детали, даёт неполные ответы, требует переспрашивания.
4. Через 10 дней: контекст переполнен. Нужно начинать новую сессию, теряя накопленный контекст.

**Результат**: Эффективная работа — максимум неделю. Дальше — деградация качества.

**Почему так происходит?** Claude Code работает как монолитный ассистент: всё в одной сессии, вся история в одном контексте. Это удобно для мелких задач, но катастрофично для долгосрочных проектов.

---

## Решение: паттерн оркестрации

Мы переосмыслили роль Claude Code: из **исполнителя всех задач** превратили в **оркестратор**, который:
- Сам выполняет только тривиальные задачи (исправление опечаток, простые импорты)
- Все сложные задачи **делегирует специализированным субагентам**
- Каждый субагент работает в **изолированном контексте**
- После завершения задачи субагент **возвращает контроль** оркестратору и **уничтожается** (контекст очищается)

**Аналогия**: Представьте, что вы — руководитель проекта. Вы не пишете код сами — вы ставите задачи специалистам (бэкенд, фронтенд, тестирование), проверяете результат, даёте обратную связь. Ваша голова не забита деталями реализации каждой задачи — вы держите общую картину.

**Результат**:
- Основной контекст Claude Code: стабильно ~10-15K токенов (вместо 50K+)
- Можно работать над проектом **бесконечно долго** без деградации качества
- Каждый субагент — эксперт в своей области

---

## Ключевая инновация: CLAUDE.md как Behavioral OS

Стандартная практика использования `CLAUDE.md`:
- Разработчики складывают туда **всю историю проекта**
- Результат: тысячи токенов уходят на информацию, которая нужна раз в месяц

**Наша инновация**: `CLAUDE.md` = **Behavioral Operating System** (операционная система поведения)

Вместо истории проекта мы храним там **правила оркестрации**:

```markdown
## Core Rules

**1. GATHER FULL CONTEXT FIRST (MANDATORY)**

Before delegating or implementing any task:
- Read existing code in related files
- Search codebase for similar patterns
- Review relevant documentation (specs, design docs, ADRs)
- Check recent commits in related areas
- Understand dependencies and integration points

NEVER delegate or implement blindly.

**2. DELEGATE TO SUBAGENTS**

Before delegation:
- Provide complete context (code snippets, file paths, patterns, docs)
- Specify exact expected output and validation criteria

After delegation (CRITICAL):
- ALWAYS verify results (read modified files, run type-check)
- NEVER skip verification
- If incorrect: re-delegate with corrections and errors

**3. EXECUTE DIRECTLY (MINIMAL ONLY)**

Direct execution only for:
- Single dependency install
- Single-line fixes (typos, obvious bugs)
- Simple imports
- Minimal config changes

Everything else: delegate.
```

**Результат**: Главный Claude Code работает как **профессиональный менеджер проектов**, а не как "делай всё сам и сгорай на середине". Вся история проекта собирается **on-demand** (только когда нужно), основной контекст остаётся чистым.

---

## Архитектура системы: оркестратор + воркеры

### 1. Главный Claude Code = Оркестратор

**Роль**: Управление, не исполнение.

**Перед делегированием**:
- Собирает полный контекст задачи (читает код, ищет паттерны, проверяет историю коммитов)
- Готовит детальную инструкцию для субагента (примеры кода, путь к файлам, критерии успеха)
- Создаёт **plan file** — JSON-файл с описанием задачи

**После делегирования**:
- Читает отчёт субагента
- **Верифицирует результат** (читает изменённые файлы, запускает type-check)
- Если что-то не так — заново делегирует с указанием ошибок
- Если всё ОК — переходит к следующей задаче

**Ключевое правило**: Никогда не пропускать верификацию. Даже если субагент отрапортовал успех.

### 2. Субагенты = Специализированные исполнители

У нас 33+ субагентов. Примеры:

**bug-hunter** — сканирует кодовую базу, находит баги, категоризирует по приоритету (critical/high/medium/low).

**bug-fixer** — берёт список багов из отчёта bug-hunter, исправляет по приоритетам, проверяет через type-check и тесты.

**security-scanner** — ищет уязвимости (SQL injection, XSS, проблемы RLS политик).

**database-architect** — проектирует схемы БД, создаёт миграции, валидирует нормализацию.

**meta-agent-v3** — создаёт новых субагентов по запросу за 2-3 минуты (следует архитектурным паттернам проекта).

**Каждый субагент следует 5-фазной структуре**:
1. **Phase 1: Read Plan** — Читает `.{workflow}-plan.json` от оркестратора
2. **Phase 2: Execute** — Выполняет работу (domain-specific logic)
3. **Phase 3: Validate** — Запускает quality gates (type-check, build, tests)
4. **Phase 4: Report** — Генерирует стандартизированный отчёт
5. **Phase 5: Return Control** — Возвращает контроль оркестратору и завершает работу

**Контекст субагента** изолирован: он не видит историю других задач, только текущую. После завершения — контекст уничтожается.

---

## Return Control Pattern: критический паттерн изоляции

**Проблема**: Если оркестратор вызывает субагента через Task tool напрямую → создаётся вложенный контекст → нарушается изоляция → накапливается память.

**Правильная схема**:

```
┌─────────────────────────────────────────────────────────┐
│ Оркестратор (главный Claude Code)                      │
│  1. Собирает контекст (Read, Grep, WebSearch)          │
│  2. Создаёт plan file (.bug-detection-plan.json)       │
│  3. Валидирует план (validate-plan-file Skill)         │
│  4. Сигнализирует готовность ("План готов, см. .tmp/") │
│  5. ВЫХОДИТ (возвращает контроль пользователю)         │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Главная сессия (пользователь)                          │
│  → Вызывает субагента через Task tool                  │
│  → Task: "@bug-hunter"                                  │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Субагент (bug-hunter в изолированном контексте)        │
│  1. Читает .bug-detection-plan.json                    │
│  2. Выполняет сканирование кодовой базы                │
│  3. Категоризирует баги (critical/high/medium/low)     │
│  4. Запускает валидацию (run-quality-gate Skill)       │
│  5. Генерирует отчёт (.bug-detection-report.md)        │
│  6. ВЫХОДИТ (возвращает контроль пользователю)         │
└─────────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Оркестратор (возобновляет работу)                      │
│  1. Читает отчёт (.bug-detection-report.md)            │
│  2. Верифицирует результаты (проверяет файлы)          │
│  3. Принимает решение (accept/reject)                  │
│  4. Если OK → следующая фаза                           │
│  5. Если NOT OK → повторная делегация с коррекцией     │
└─────────────────────────────────────────────────────────┘
```

**Преимущество**: Контексты полностью изолированы. Оркестратор видит только результаты, не детали реализации. Каждый субагент работает в чистом контексте без наследования истории.

---

## Пример: Plan File (JSON Schema)

**bug-detection-plan.json**:
```json
{
  "workflow": "bug-management",
  "phase": "detection",
  "phaseNumber": 1,
  "config": {
    "categories": [
      "type-errors",
      "runtime-errors",
      "security",
      "performance",
      "dead-code",
      "debug-code"
    ],
    "maxBugsPerRun": 1000
  },
  "validation": {
    "required": ["report-exists", "type-check"],
    "optional": ["tests"]
  },
  "nextAgent": "bug-hunter",
  "timestamp": "2025-11-11T14:23:45.123Z",
  "metadata": {
    "createdBy": "bug-orchestrator",
    "iteration": 1,
    "maxIterations": 3
  }
}
```

**Структура плана**:
- `workflow` — название workflow (bug-management, security-audit, dependency-update)
- `phase` — текущая фаза (detection, fixing, verification)
- `config` — параметры работы (какие категории багов искать, лимиты)
- `validation` — какие проверки запустить после выполнения
- `nextAgent` — какой воркер должен обработать этот план
- `metadata` — контекст (кто создал, номер итерации, лимиты)

**Зачем отдельный файл?** Полная изоляция: субагент получает только то, что ему нужно. Никакой истории переписки, никаких лишних деталей.

---

## Quality Gates: автоматическая валидация

После каждой задачи — обязательная проверка. Никаких исключений.

**Реализация**: Skill `run-quality-gate`

**Пример использования в воркере**:
```markdown
## Phase 3: Validate Work

Use `run-quality-gate` Skill to execute validation:

**Type-Check Gate**:
- Command: `pnpm type-check`
- Blocking: true
- If FAILED: Rollback changes, report failure, exit
- If PASSED: Proceed to build gate

**Build Gate**:
- Command: `pnpm build`
- Blocking: true
- If FAILED: Rollback changes, report failure, exit
- If PASSED: Proceed to tests

**Tests Gate**:
- Command: `pnpm test`
- Blocking: false (warn only)
- If FAILED: Log warning, proceed
- If PASSED: Proceed to Phase 4
```

**Логика качественных гейтов** (из run-quality-gate.md):
```
IF exit_code == 0:
  action = "continue"
  passed = true
ELSE:
  IF blocking == true:
    action = "stop"      # Останавливаем workflow
  ELSE:
    action = "warn"      # Логируем, продолжаем
  passed = false
```

**Результат**: Каждый коммит проходит type-check, build, тесты. Баги ловятся до деплоя, а не после.

---

## Health Workflows: итеративные циклы детекции и исправления

### Проблема

Классический подход к багфиксингу:
1. Разработчик находит баг (вручную или от пользователя)
2. Исправляет баг (возможно, создавая новые)
3. Отдаёт на тестирование
4. Тестировщик находит новые баги
5. Repeat

**Недостатки**: Реактивный подход, высокая стоимость, баги доходят до продакшена.

### Наше решение: автоматические health workflows

**Команды**:
- `/health-bugs` — детекция и исправление багов
- `/health-security` — поиск и устранение уязвимостей
- `/health-deps` — аудит и обновление зависимостей
- `/health-cleanup` — детекция и удаление мёртвого кода

### Архитектура /health-bugs

**Итеративный цикл** (до 3 итераций):

```
Iteration 1:
  ├─ Phase 1: Bug Detection (bug-hunter)
  │   └─ Сканирует весь проект
  │   └─ Категоризирует: critical (5), high (12), medium (33), low (87)
  │   └─ Генерирует bug-detection-report.md
  │
  ├─ Phase 2: Fix Critical Bugs (bug-fixer)
  │   └─ Читает отчёт, берёт critical bugs (5 штук)
  │   └─ Исправляет каждый баг
  │   └─ Запускает type-check + build
  │   └─ Генерирует bug-fixes-implemented.md
  │
  ├─ Phase 3: Fix High Priority Bugs (bug-fixer)
  │   └─ Читает отчёт, берёт high bugs (12 штук)
  │   └─ Исправляет каждый баг
  │   └─ Запускает type-check + build
  │   └─ Генерирует bug-fixes-implemented.md
  │
  ├─ Phase 4-5: Medium и Low (аналогично)
  │
  └─ Phase 6: Verification
      └─ Повторный запуск bug-hunter
      └─ Проверка: остались ли баги?
      └─ Если YES + iterations < 3 → Iteration 2
      └─ Если NO → Final Summary
```

**Зачем итерации?** Исправление одного бага может создать новые (типизация, рефакторинг). Итеративный подход гарантирует, что проект становится чище с каждым циклом.

**Реальный пример** (из нашей практики):
- Iteration 1: Найдено 137 багов → исправлено 137 → осталось 14 (новые, из-за рефакторинга)
- Iteration 2: Найдено 14 багов → исправлено 14 → осталось 2 (edge cases)
- Iteration 3: Найдено 2 бага → исправлено 2 → осталось 0
- **Результат**: Проект чистый, type-check проходит, build успешен.

---

## SpecKit Enhancement: Phase 0 (Planning Before Execution)

### Проблема с оригинальным SpecKit

**SpecKit от GitHub** — отличный инструмент для structured development:
- `/speckit.specify` — создаёт спецификацию
- `/speckit.plan` — генерирует план реализации
- `/speckit.tasks` — разбивает на задачи
- `/speckit.implement` — выполняет задачи

**Но**: Сразу начинает выполнение без подготовки агентов.

**Проблема**: Если для задачи нужен специализированный агент, которого ещё нет → workflow ломается.

### Наше решение: Phase 0 (Planning Phase)

**Phase 0 выполняется ПЕРЕД началом реализации**:

#### Task 1: Executor Assignment (Назначение исполнителей)

Анализируем каждую задачу из `tasks.md` и назначаем исполнителя:

```markdown
**Задача**: Implement JWT authentication with refresh tokens

**Анализ**:
- Сложность: HIGH (работа с токенами, безопасность, database)
- Существующие агенты: database-architect (не подходит, нет auth expertise)
- Решение: Нужен новый агент

**Назначение**: [EXECUTOR: FUTURE-auth-specialist]
```

**Классификация**:
- `[EXECUTOR: MAIN]` — тривиальные задачи (1-2 строки кода, simple imports)
- `[EXECUTOR: existing-agent]` — если есть 100% совпадение с существующим агентом
- `[EXECUTOR: FUTURE-agent-name]` — если нужен новый агент

#### Task 2: Meta-Agent Creation (Создание агентов)

Если найдены FUTURE-агенты → запускаем meta-agent-v3:

```
Найдено FUTURE агентов: 3
  - auth-specialist (JWT, refresh tokens, session management)
  - email-notification-service (SMTP, templates, queue)
  - analytics-tracker (event tracking, metrics, dashboards)

Запуск meta-agent-v3 (3 вызова в параллель в одном сообщении):
  1. Task: "@meta-agent-v3 Create auth-specialist worker..."
  2. Task: "@meta-agent-v3 Create email-notification-service worker..."
  3. Task: "@meta-agent-v3 Create analytics-tracker worker..."

После создания → просьба перезапустить Claude Code для загрузки новых агентов
```

**Atomicity Rule (Критично)**: 1 задача = 1 вызов агента. Параллельные задачи = N вызовов в **одном сообщении**.

**Почему важно?** Если запускать последовательно → контекст переполняется. Если параллельно в одном сообщении → контекст остаётся чистым.

#### Task 3: Research Resolution (Решение исследовательских задач)

**Simple Research** (решается сразу):
- Использование существующих библиотек (WebSearch, Context7)
- Проверка документации (Read, Grep)
- Анализ кодовой базы (Grep, Read)

**Complex Research** (требует deep thinking):
- Архитектурные решения с несколькими вариантами
- Выбор стека технологий
- Проектирование сложных систем

Для сложных случаев: создание английского промпта в `{FEATURE_DIR}/research/`, отправка на deepresearch, ожидание результатов.

**Результат Phase 0**: Все агенты готовы, все исследования завершены, можно начинать параллельное выполнение задач без блокировок.

---

## Worktrees: параллельная разработка 5-7 фичей

### Проблема классического workflow

Работа над одной фичей → клиент просит срочно сделать другую → приходится:
1. `git stash` (сохранить текущие изменения)
2. `git checkout -b urgent-feature` (переключиться на новую фичу)
3. Работать над новой фичей (теряя контекст первой)
4. `git checkout original-feature` (вернуться к первой)
5. `git stash pop` (восстановить изменения)
6. Вспоминать, где остановился

**Результат**: Постоянные переключения, потеря контекста, стресс.

### Наше решение: Git Worktrees + Claude Code

**Команда**: `/worktree-create feature/new-auth-flow`

**Что происходит**:
```bash
# Создаётся отдельная директория
.worktrees/
  └─ feature-new-auth-flow/
      ├─ .git (ссылка на основной репозиторий)
      ├─ package.json
      ├─ src/
      └─ ... (полная копия проекта)

# Создаётся отдельная ветка
git branch feature/new-auth-flow

# Worktree привязан к этой ветке
git worktree list
  /home/user/project              (main)
  /home/user/project/.worktrees/feature-new-auth-flow  (feature/new-auth-flow)
```

**VS Code Integration** (из `.vscode/settings.local.json.example`):
```json
{
  "folders": [
    {
      "name": "🏠 Main Project",
      "path": "."
    },
    {
      "name": "🌿 Feature: New Auth",
      "path": ".worktrees/feature-new-auth-flow"
    },
    {
      "name": "🌿 Feature: Dashboard Redesign",
      "path": ".worktrees/feature-dashboard-redesign"
    }
  ]
}
```

**Использование**:
1. Открываем VS Code
2. В селекторе папок видим 3 workspace:
   - Main Project (production hotfixes)
   - Feature: New Auth (Claude Code active)
   - Feature: Dashboard Redesign (Claude Code active)
3. Переключаемся между ними через селектор (не через git checkout)
4. Каждый worktree = отдельная сессия Claude Code = изолированный контекст

**Реальная практика** (мы так работаем):
- Main workspace: Мониторинг продакшена, hotfix если нужно
- Worktree 1: Фича A (Claude Code активно работает)
- Worktree 2: Фича B (Claude Code активно работает)
- Worktree 3: Фича C (Claude Code активно работает)
- Worktree 4: Experimental refactoring (Claude Code следит)

**Результат**: 5-7 проектов одновременно, нулевое загрязнение контекста, изолированное тестирование.

---

## MCP Dynamic Switching: управление контекстным бюджетом

### Проблема

**Claude Code MCP Servers** предоставляют мощные интеграции:
- **Context7**: Документация библиотек (~600 токенов)
- **Supabase**: Операции с БД (~1500 токенов)
- **Sequential Thinking**: Усиленная логика (~500 токенов)
- **Playwright**: Автоматизация браузера (~800 токенов)
- **shadcn**: UI компоненты (~700 токенов)

**Проблема**: FULL конфигурация = ~5000 токенов (10% контекстного окна).

**Реальность**: Редко нужны все серверы одновременно.

### Решение: switch-mcp.sh

**Скрипт** (100 строк bash):
```bash
#!/bin/bash

echo "MCP Configuration Switcher"
echo "Current: $(cat .mcp.json | jq -r '.mcpServers | keys | length') servers"
echo ""
echo "Available configurations:"
echo "1) BASE (~600 tokens) - Context7 + Sequential Thinking"
echo "2) SUPABASE (~2500 tokens) - BASE + Supabase"
echo "3) FRONTEND (~2000 tokens) - BASE + Playwright + shadcn"
echo "4) FULL (~5000 tokens) - All servers"
echo ""
read -p "Select: " choice

case $choice in
  1) cp mcp/.mcp.base.json .mcp.json ;;
  2) cp mcp/.mcp.supabase.json .mcp.json ;;
  3) cp mcp/.mcp.frontend.json .mcp.json ;;
  4) cp mcp/.mcp.full.json .mcp.json ;;
esac

echo "✅ Switched to $config"
echo "⚠️  Restart Claude Code to apply"
```

**Реальный workflow**:
```
09:00 - Утро: BASE config (general development)
       ~ Работа над фичами, рефакторинг

11:30 - Задача с БД: ./switch-mcp.sh → SUPABASE
       ~ Создание миграций, изменение схемы

14:00 - UI работа: ./switch-mcp.sh → FRONTEND
       ~ Компоненты, стили, Playwright тесты

16:30 - Сложная фича: ./switch-mcp.sh → FULL
       ~ Нужно всё сразу (БД + UI + тесты)

18:00 - Конец дня: ./switch-mcp.sh → BASE
       ~ Обратно на минимальную конфигурацию
```

**Экономия**: 500-4500 токенов контекста. Загружаем только то, что нужно сейчас.

---

## Webhook Integration: уведомления о завершении задач

### Проблема

Запустили задачу в Claude Code → переключились на другой проект → не знаем, когда возвращаться → теряем время.

### Решение

**Конфигурация** (`.claude/settings.local.json`):
```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "notify-send 'Claude Code' 'Task completed!' -i checkbox-checked"
      }
    ]
  }
}
```

**Как работает**:
1. Claude Code завершает задачу (статус "Stop")
2. Триггерится webhook
3. Выполняется команда (notify-send на Linux, osascript на macOS)
4. Приходит системное уведомление

**Примеры**:

**Telegram Bot**:
```bash
curl -s -X POST https://api.telegram.org/bot{TOKEN}/sendMessage \
  -d chat_id={CHAT_ID} \
  -d text="✅ Claude Code: Task completed in worktree feature-new-auth"
```

**Slack Webhook**:
```bash
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK \
  -d '{"text":"Claude Code task completed!", "channel":"#dev-notifications"}'
```

**Результат**: Запустил задачу → переключился на другое → получил уведомление → вернулся ровно когда нужно. Продуктивность растёт.

---

## Результаты: метрики из реальной практики

Эти цифры — не прогнозы, а данные из работы **AI Dev Team** за последние 2 года.

### Скорость разработки

**Традиционный подход**: 2-3 месяца на проект средней сложности
**С оркестратором**: 1-2 недели
**Ускорение**: **~75% быстрее**

**Почему быстрее?**
- Параллельная работа: 5-7 проектов одновременно через worktrees
- Автоматизация рутины: health workflows работают без участия человека
- Нет простоя: webhook-уведомления при завершении задач

### Стоимость

**Традиционная модель**: Без AI-автоматизации те же задачи требовали бы кратно больше ресурсов
**С оркестратором**: 54 специалиста + 44 AI-агента, 3-7 человек на проект
**Снижение стоимости**: **-80%**

**Откуда экономия?**
- Автоматические проверки (quality gates) вместо ручного code review
- Автоматическое обнаружение багов и уязвимостей (health workflows)
- Систематический рефакторинг (dead code cleanup, dependency updates)

### Качество

**Парадокс**: Меньше багов, чем при традиционной разработке.

**Почему?**
- **Обязательная верификация**: После каждой задачи — type-check + build + тесты
- **Автоматические security-сканы**: Регулярные проверки на SQL injection, XSS, RLS gaps
- **Систематический подход**: Все задачи выполняются по одним и тем же паттернам

### Контекстное окно

**Standard Claude Code**: ~50K токенов после нескольких задач (непригодно для работы)
**Orchestrator Kit**: ~10-15K токенов в главном оркестраторе (стабильно)
**Результат**: **Можно работать над проектом бесконечно долго**

### Масштабируемость

**Традиционный отдел**: Больше проектов = больше людей
**С оркестратором**: Создаём новых субагентов через meta-agent (2-3 минуты), добавляем worktree (30 секунд)
**Текущая пропускная способность**: **5-7 проектов одновременно (54 специалиста, 3-7 человек на проект)**

---

## Техническая архитектура: краткий обзор

**Файловая организация**:
```
.claude/
  ├─ agents/
  │   ├─ health/
  │   │   ├─ orchestrators/ (bug-orchestrator, security-orchestrator)
  │   │   └─ workers/ (bug-hunter, bug-fixer, security-scanner)
  │   ├─ meta/ (meta-agent-v3, skill-builder-v2)
  │   └─ speckit/ (planning-agent, task-executor)
  │
  ├─ commands/ (19+ slash команд)
  │   ├─ health-bugs.md
  │   ├─ worktree-create.md
  │   └─ push.md
  │
  ├─ skills/ (15+ переиспользуемых утилит)
  │   ├─ run-quality-gate/
  │   ├─ validate-plan-file/
  │   └─ generate-report-header/
  │
  └─ schemas/ (JSON схемы для plan files)

mcp/ (6 MCP конфигураций)
  ├─ .mcp.base.json (~600 токенов)
  ├─ .mcp.supabase.json (~2500 токенов)
  └─ .mcp.full.json (~5000 токенов)

CLAUDE.md (Behavioral OS — правила оркестрации)
```

**Компоненты**:
- **33+ агентов**: 4 orchestrators + 24 workers + 5 support
- **19+ команд**: health workflows, worktree management, releases
- **15+ skills**: validation, formatting, parsing utilities
- **6 MCP configs**: BASE → FULL (контроль контекстного бюджета)

---

## Дисклеймер: ожидаемая критика и моя позиция

Понимаю, что эта статья вызовет негатив у части разработчиков. Истории про «vibe coding», опасения «AI заменит программистов», обвинения в упрощении.

**Моё мнение**: Эта реакция — больше про **страх, смешанный с надменностью**, чем про техническую критику.

**Страх**: «Если AI делает мою работу, что будет со мной?»
**Надменность**: «Только люди могут писать *настоящий* код, AI — игрушка.»

**Реальность**: AI не заменяет хороших разработчиков. Он их **усиливает**. Orchestrator Kit — не про замену программистов. Это про:
- Удаление рутины (автоматические проверки, детекция багов)
- Систематизацию процессов (качественные гейты, верификация)
- Сохранение контекста (чтобы разработчики фокусировались на архитектуре и сложных проблемах)

**Если не согласны** — отлично. Склонируйте репо, попробуйте, а потом расскажите, где я не прав. Предпочитаю технические аргументы эмоциональным реакциям.

---

## Установка и начало работы

**NPM Installation**:
```bash
npm install -g claude-code-orchestrator-kit
```

**Ручная установка**:
```bash
git clone https://github.com/maslennikov-ig/claude-code-orchestrator-kit.git
cd claude-code-orchestrator-kit
./switch-mcp.sh  # Выбрать BASE конфигурацию
# Перезапустить Claude Code
# Попробовать /health-bugs
```

**Интеграция в существующий проект**:
1. Копируем `.claude/` в свой проект
2. Копируем `mcp/` конфигурации
3. Копируем `CLAUDE.md` (Behavioral OS)
4. Настраиваем `.env.local` (если нужны credentials)
5. Запускаем `./switch-mcp.sh` → выбираем BASE
6. Перезапускаем Claude Code
7. Пробуем `/health-bugs` для проверки

---

## Что дальше: анонс серии

Эта статья — **часть 1 из 3**. Я рассказал о концепции, архитектуре, ключевых паттернах.

**Часть 2** (выйдет через неделю): Deep Dive в технические детали
- Полная структура воркера (5 фаз с примерами кода)
- meta-agent-v3 внутри (как создаются агенты за 2-3 минуты)
- Health workflows: полный разбор итеративных циклов
- Skills Library: создание переиспользуемых утилит

**Часть 3** (выйдет через 2 недели): Практические кейсы и рабочие процессы
- Реальные примеры из AI Dev Team (кейсы с цифрами)
- Worktree workflow для 5-7 параллельных фич
- MCP switching стратегии (когда что использовать)
- Lessons learned за 2 года работы

---

## Контакты и обратная связь

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/maslennikovigor

У меня там всего 73 подписчика. Буду очень рад, если кто-то из вас станет сотым. Пишу редко, но когда пишу — стараюсь, чтобы было по делу.

**Прямой контакт** (для обсуждений): https://t.me/maslennikovig

Нужно обсудить напрямую? Пишите. Всегда открыт к диалогу.

### 💬 Обратная связь: я широко открыт

**Буду очень рад услышать**:
- **Критику** — Что не так с этим подходом? Где слабые места?
- **Идеи** — Какие фичи добавить? Чего не хватает?
- **Предложения** — Как улучшить, оптимизировать, рефакторить систему?
- **Вопросы** — Что-то неясно? Спрашивайте.

**Каналы для связи**:
- **GitHub Issues**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/issues (для багов, фич-реквестов)
- **GitHub Discussions**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/discussions (для идей и вопросов)
- **Telegram**: https://t.me/maslennikovig (для прямого диалога)

**Тон**: Никакого эго — просто хочу сделать систему лучше.

---

**Игорь Масленников**
Основатель AI Dev Team
В IT с 2013 года

**Репозиторий**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit
**Лицензия**: MIT (полностью бесплатно для коммерческого использования)

---

*Продолжение следует: Часть 2 — Deep Dive в технические детали (следующая неделя)*
