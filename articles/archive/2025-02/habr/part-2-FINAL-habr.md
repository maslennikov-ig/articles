---
platform: habr
series: Claude Code Orchestrator Kit
part: 2 of 3
title: "Внутри оркестратора: 5-фазная структура воркеров, meta-agent-v3 и Skills Library"
author: Igor Maslennikov
date: 2025-11-11
length: 24567 characters
tags: [Claude Code, архитектура, AI-агенты, оркестрация, TypeScript, MCP, deep-dive]
language: ru
---

# Внутри оркестратора: 5-фазная структура воркеров, meta-agent-v3 и Skills Library

*Deep dive в техническую архитектуру: как работают воркеры, как создаются агенты за 2-3 минуты, и как устроена библиотека переиспользуемых утилит*

---

## Контекст: Продолжение серии

В [первой части](./part-1-FINAL-habr.md) я рассказал о концепции оркестрации, Return Control Pattern и общей архитектуре системы. Эта статья — для тех, кто хочет понять **как именно это работает изнутри**.

Игорь Масленников. В IT с 2013 года. Последние 2 года развиваю AI Dev Team в DNA IT. Всё, что описано ниже — проверено на реальных проектах, а не на демках.

**Что внутри этой части:**
1. Полная 5-фазная структура воркера (с реальным кодом)
2. meta-agent-v3: как создаются агенты за 2-3 минуты
3. Health workflows: полный разбор итеративных циклов
4. Skills Library: архитектура и примеры
5. Файловая организация и JSON-схемы

Если вы не читали первую часть — рекомендую начать с неё. Здесь будет много технических деталей.

---

## Раздел 1: Полная структура воркера (5 фаз)

### Концепция: Воркер = Изолированный исполнитель

**Воркер** — это специализированный агент, который:
- Работает в **изолированном контексте** (не видит историю других задач)
- Читает **plan file** от оркестратора (JSON с инструкциями)
- Выполняет **domain-specific work** (детекция багов, исправление уязвимостей, и т.д.)
- Запускает **quality gates** (type-check, build, tests)
- Генерирует **стандартизированный отчёт** (для оркестратора)
- **Возвращает контроль** оркестратору и завершается (контекст уничтожается)

**Структура воркера — всегда 5 фаз.** Это не догма, а архитектурный паттерн, который даёт:
- Предсказуемость (все воркеры работают одинаково)
- Тестируемость (каждая фаза изолирована)
- Отказоустойчивость (откат возможен на любой фазе)

### Пример: bug-hunter (детектор багов)

Покажу **реальный воркер** из нашего проекта. Файл: `.claude/agents/health/workers/bug-hunter.md`

#### YAML Frontmatter

```yaml
---
name: bug-hunter
description: Use proactively for comprehensive bug detection, code validation, dead code identification, and generating prioritized fix tasks. Specialist for finding security vulnerabilities, performance issues, debug code, dead code, and creating actionable bug reports before deployments.
model: sonnet
color: yellow
---
```

**Что здесь:**
- `name`: Имя агента (kebab-case)
- `description`: Что агент делает + когда его вызывать
- `model`: Модель Claude (`sonnet` для воркеров, баланс цены и качества)
- `color`: Цвет для UI (визуальная идентификация)

#### Phase 0: Read Plan File (Optional)

Воркер **сначала проверяет**, есть ли plan file от оркестратора.

```markdown
### Phase 0: Read Plan File (if provided)

**If a plan file path is provided in the prompt** (e.g., `.tmp/current/plans/bug-detection.json`):

1. **Read the plan file** using Read tool
2. **Extract configuration**:
   - `config.priority`: Filter bugs by priority (critical, high, medium, low, all)
   - `config.categories`: Specific bug categories to focus on
   - `config.maxBugsPerRun`: Maximum bugs to report
   - `phase`: detection or verification
3. **Adjust detection scope** based on plan configuration

**If no plan file** is provided, proceed with default configuration (all priorities, all categories).
```

**Пример plan file** (`.tmp/current/plans/bug-detection.json`):

```json
{
  "workflow": "bug-management",
  "phase": "detection",
  "phaseNumber": 1,
  "config": {
    "priority": "all",
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

**Зачем отдельный файл?** Полная изоляция. Воркер получает **только то, что нужно для задачи**. Никакой истории переписки, никаких лишних деталей из главной сессии.

#### Phase 1: Reconnaissance (Сбор контекста)

```markdown
### Phase 1: Initial Reconnaissance

1. Identify the project type and technology stack using Glob and Read tools
2. Locate configuration files (package.json, tsconfig.json, .eslintrc, etc.)
3. Map out the codebase structure to understand key directories
```

**Реальные команды:**

```bash
# Определить тип проекта
ls -la package.json tsconfig.json next.config.js

# Прочитать package.json (зависимости, скрипты)
cat package.json | grep -E "(dependencies|scripts)" -A 20

# Найти все TypeScript файлы
find src -name "*.ts" -o -name "*.tsx" | wc -l
```

**Результат фазы 1**: Воркер понимает:
- Стек технологий (Next.js + TypeScript + Supabase)
- Структуру проекта (`src/`, `packages/`, и т.д.)
- Доступные скрипты (`npm run lint`, `npm run type-check`, и т.д.)

#### Phase 2: Static Analysis & Validation

```markdown
### Phase 2: Static Analysis & Validation

4. **Optional**: Use `mcp__ide__getDiagnostics({})` if IDE MCP extension available
5. **REQUIRED**: Check framework documentation for proper patterns using Docs L1/L2 before flagging issues
6. Run available linters and type checkers using Bash:
   - For TypeScript/JavaScript: `npx tsc --noEmit`, `npm run lint` or `pnpm lint`
   - For Python: `pylint`, `flake8`, `mypy`
7. **CRITICAL: Test Production Build**:
   - **ALWAYS** run `npm run build` or `pnpm build` to catch build-time errors
   - Next.js production build is STRICTER than `tsc --noEmit`
   - Common build-only errors: Spread operator type errors, Supabase query inference failures
8. Capture and categorize all warnings and errors from both lint and build
```

**Почему проверять через Context7 перед флагом?** Чтобы не флагать **правильные паттерны** как баги.

**Пример проверки** (React hooks паттерн):

```typescript
// bug-hunter находит: useEffect без dependencies
useEffect(() => {
  fetchData();
});

// Перед флагом:
// 1. Запрос к Context7: "React useEffect best practices"
// 2. Получение официальной документации:
//    "useEffect without dependencies runs on every render - this is intentional for some cases"
// 3. Классификация: Warning (не Critical)
```

**Команды:**

```bash
# Type-check
pnpm type-check
# Exit code: 0 = OK, non-zero = errors

# Build (КРИТИЧНО для Next.js)
pnpm build
# Ловит ошибки, которые type-check пропускает
```

**Реальный баг**, который `tsc --noEmit` НЕ НАХОДИТ, а `next build` НАХОДИТ:

```typescript
// TypeScript OK, но Next.js build FAILS
const data = { ...someVariable };
//               ^^^^^^^^^^^^^^
// Error: Type 'never' cannot be spread
```

#### Phase 3: Security, Performance, Dead Code Scan

```markdown
### Phase 3-6: Domain-Specific Scans

9. Search for common security anti-patterns using Grep:
   - SQL injection risks: unsanitized input in queries
   - XSS vulnerabilities: innerHTML, dangerouslySetInnerHTML without sanitization
   - Hardcoded credentials: API keys, passwords, tokens

10. Detect performance bottlenecks:
   - Nested loops with O(n²) or worse complexity
   - Missing memoization for expensive calculations
   - Memory leaks: unclosed connections, missing cleanup

11. Find debug/development code:
   - Console statements: `console\.(log|debug|trace|info)`
   - Development markers: `TODO`, `FIXME`, `HACK`

12. Identify dead code:
   - Large blocks of commented-out code (>3 consecutive lines)
   - Unreachable code after `return`, `throw`
   - Unused imports/variables
```

**Пример: Поиск hardcoded credentials**

```bash
# Поиск API ключей
grep -rn "API_KEY\s*=\s*['\"]" src/

# Результат:
# src/config/secrets.ts:15: const API_KEY = "sk-abc123..."
```

**Пример: Детекция memory leak**

```typescript
// bug-hunter находит:
useEffect(() => {
  const timer = setInterval(() => {
    fetchData();
  }, 1000);
  // Missing cleanup → memory leak
}, []);

// Рекомендация:
useEffect(() => {
  const timer = setInterval(() => {
    fetchData();
  }, 1000);

  // Add cleanup
  return () => clearInterval(timer);
}, []);
```

#### Phase 4: Generate Report

```markdown
### Phase 10: Report Generation

16. Create a comprehensive bug-hunting-report.md file with the enhanced structure
```

**Структура отчёта** (стандартизированная для всех воркеров):

```markdown
---
report_type: bug-hunting
generated: 2025-11-11T14:30:00Z
version: 2025-11-11
status: success
agent: bug-hunter
duration: 3m 45s
files_processed: 147
issues_found: 23
critical_count: 3
high_count: 8
medium_count: 12
low_count: 0
---

# Bug Hunting Report: 2025-11-11

**Generated**: 2025-11-11 14:30:00 UTC
**Status**: ✅ success
**Files Processed**: 147

---

## Executive Summary

Comprehensive bug scan completed successfully. Found 23 bugs across 147 TypeScript files.

### Key Metrics

- **Critical Bugs**: 3 (require immediate attention)
- **High-Priority Bugs**: 8 (fix this sprint)
- **Medium-Priority Bugs**: 12 (schedule next sprint)
- **Files Scanned**: 147
- **Scan Duration**: 3m 45s

---

## Detailed Findings

### Critical (3)

1. **[src/api/database.ts:45] Memory Leak in Connection Pool**
   - **Severity**: Critical
   - **Priority**: P0
   - **Description**: Connection pool not releasing connections after timeout
   - **Impact**: Memory exhaustion after ~2 hours of operation
   - **Location**: `src/api/database.ts:45-67`
   - **Fix**: Implement automatic connection cleanup and recycling
   - **Estimated Time**: 2 hours

[... остальные баги ...]

---

## Validation Results

### Type Check

**Command**: `pnpm type-check`
**Status**: ✅ PASSED
**Exit Code**: 0

### Build

**Command**: `pnpm build`
**Status**: ✅ PASSED
**Exit Code**: 0

---

## Next Steps

1. **Fix Critical Bugs** (P0)
   - Start with memory leak in connection pool
2. **Run Regression Tests**
   - After each fix, verify no new issues
```

#### Phase 5: Return Control

```markdown
Your final output must be:
1. A comprehensive `bug-hunting-report.md` file saved to the project root
2. A summary message to the user highlighting:
   - Total number of issues found by priority
   - Most critical issues requiring immediate attention
   - Estimated effort for cleanup tasks
```

**Важно**: Воркер **НЕ ВЫЗЫВАЕТ** других агентов. Он завершает работу и возвращает контроль оркестратору.

---

### Полная структура файла bug-hunter.md

**Размер**: ~650 строк
**Секции**:
- YAML frontmatter (4 строки)
- Purpose (10 строк)
- MCP Servers (40 строк — какие использовать и зачем)
- Phase 0-10 instructions (400 строк)
- Report structure template (150 строк)
- Best practices (50 строк)

**Это не "промпт"**. Это **исполняемая спецификация агента**. Claude Code читает её и работает **строго по инструкциям**.

---

## Раздел 2: meta-agent-v3 — Фабрика агентов

### Проблема: Создание агента вручную = 1-2 часа

Написать воркера с нуля:
1. Прочитать ARCHITECTURE.md (1,200 строк)
2. Понять 5-фазную структуру
3. Посмотреть существующих агентов (примеры)
4. Написать YAML frontmatter
5. Написать инструкции для каждой фазы
6. Добавить MCP интеграции
7. Написать error handling
8. Написать report template
9. Валидировать структуру

**Итого**: 1-2 часа на одного агента (если знаешь архитектуру).

### Решение: meta-agent-v3

**meta-agent-v3** — это агент, который **создаёт других агентов** за 2-3 минуты.

**Файл**: `.claude/agents/meta/workers/meta-agent-v3.md`
**Размер**: ~500 строк (сконцентрированная версия)

### Алгоритм работы

#### Step 0: Определение типа агента

```markdown
**Step 0: Determine Agent Type**
Ask user: "What type of agent? (worker/orchestrator/simple)"
```

**3 типа агентов:**
1. **Worker**: Выполняет задачи из plan files (bug-fixer, security-scanner)
2. **Orchestrator**: Координирует multi-phase workflows (bug-orchestrator, deployment-orchestrator)
3. **Simple**: Standalone tool без координации (code-formatter, version-bumper)

#### Step 0.5: Загрузка актуальной документации (опционально)

```markdown
**Step 0.5: Load Latest Documentation** (Optional but Recommended)
Use WebFetch to verify current Claude Code patterns:
- `https://docs.claude.com/en/docs/claude-code/sub-agents`
```

**Зачем?** Claude Code обновляется. Паттерны могут меняться. WebFetch даёт актуальную информацию.

**Fallback**: Если WebFetch недоступен — использовать локальные ARCHITECTURE.md + CLAUDE.md.

#### Step 1: Загрузка архитектуры проекта

```markdown
**Step 1: Load Architecture**
- Read `docs/Agents Ecosystem/ARCHITECTURE.md` (focus on agent type section)
- Read `CLAUDE.md` (behavioral rules for agent type)
```

**Что извлекается:**
- Return Control Pattern (для оркестраторов)
- 5-фазная структура (для воркеров)
- Правила валидации (quality gates)
- Форматы отчётов (report templates)
- MCP интеграции (какие серверы использовать)

#### Step 2: Сбор параметров агента

```markdown
**Step 2: Gather Essentials**
- Name (kebab-case)
- Domain (health/release/deployment/etc)
- Purpose (clear, action-oriented)
- [Type-specific details below]
```

**Для воркера**:
- Orchestrator that invokes this worker
- Plan file fields (priority, categories, max items)
- Output (report file, changes made)
- Validation criteria (type-check, build, tests)

**Пример диалога:**

```
meta-agent-v3: What type of agent? (worker/orchestrator/simple)
User: worker

meta-agent-v3: Agent name (kebab-case)?
User: auth-specialist

meta-agent-v3: Domain (health/release/deployment/etc)?
User: auth

meta-agent-v3: Purpose (what does it do)?
User: Implements JWT authentication with refresh tokens, secure session management, and role-based access control

meta-agent-v3: Which orchestrator invokes this worker?
User: auth-orchestrator

meta-agent-v3: Plan file fields (priority, categories, etc)?
User: priority (critical/high/medium), auth_method (jwt/oauth/saml), session_duration

meta-agent-v3: Output format (report file, changes)?
User: auth-implementation-report.md with list of created files, validation results

meta-agent-v3: Validation criteria (type-check, build, tests)?
User: type-check (blocking), build (blocking), tests (non-blocking)
```

#### Step 3: Генерация агента

```markdown
**Step 3: Generate**
- YAML frontmatter → Agent structure → Validate → Write
```

**Процесс генерации:**

1. **YAML Frontmatter**:
```yaml
---
name: auth-specialist
description: Use proactively for implementing JWT authentication with refresh tokens, secure session management, and role-based access control. Expert in authentication patterns, token management, and security best practices.
model: sonnet
color: purple
---
```

2. **5-фазная структура** (для воркера):
```markdown
## Phase 1: Read Plan File
- Check for `.tmp/current/plans/auth-implementation.json`
- Extract config (priority, auth_method, session_duration)
- Validate required fields

## Phase 2: Execute Work
- Implement JWT authentication logic
- Create refresh token mechanism
- Add role-based access control
- Implement session management
- Track changes internally

## Phase 3: Validate Work
- Run type-check (blocking)
- Run build (blocking)
- Run tests (non-blocking)
- Check security best practices

## Phase 4: Generate Report
- Use generate-report-header Skill
- Include validation results
- List created files and changes
- Document security considerations

## Phase 5: Return Control
- Report summary to user
- Exit (orchestrator resumes)
```

3. **MCP интеграции**:
```markdown
## MCP Servers

This agent uses the following MCP servers when available:

### Docs L1/L2 (REQUIRED)
```javascript
// Check authentication best practices
mcp__context7__resolve-library-id({libraryName: "passport"})
mcp__context7__get-library-docs({context7CompatibleLibraryID: "/jaredhanson/passport", topic: "jwt"})
```

### Supabase (if applicable)
```javascript
// For database-backed auth
mcp__supabase__execute_sql({query: "CREATE TABLE sessions..."})
```
```

4. **Error handling**:
```markdown
## Error Handling

**On Validation Failure**:
1. Report failure to orchestrator
2. Include rollback instructions
3. Suggest fixes based on error type
```

5. **Report template**:
```markdown
## Report Structure

Generate `auth-implementation-report.md`:

---
report_type: auth-implementation
generated: ISO-8601
status: success|partial|failed
---

# Auth Implementation Report

## Executive Summary
[Key findings, validation status]

## Work Performed
- Created JWT authentication middleware
- Implemented refresh token rotation
- Added role-based access control
- [etc.]

## Validation Results
- Type Check: ✅ PASSED
- Build: ✅ PASSED
- Tests: ⚠️ PARTIAL (2/5 passed)

## Next Steps
[Recommendations for orchestrator]
```

### Время создания: 2-3 минуты

**Реальный пример** (засекали время):
- Step 0-2 (диалог с пользователем): 1 минута
- Step 3 (генерация): 1-2 минуты (зависит от модели)
- Валидация и сохранение: 10-15 секунд

**Итого**: ~2-3 минуты на создание полнофункционального воркера.

### Что meta-agent-v3 НЕ делает

❌ Не пишет код implementation (только структуру агента)
❌ Не тестирует созданного агента (это делает пользователь)
❌ Не создаёт plan file schemas (используются существующие)

✅ Создаёт **правильную структуру** агента
✅ Следует архитектурным паттернам проекта
✅ Добавляет нужные MCP интеграции
✅ Генерирует валидный YAML frontmatter

---

## Раздел 3: Health Workflows — Полный разбор итеративных циклов

### Проблема: Исправление одного бага создаёт новые

**Реальный сценарий:**

```
Iteration 1:
  Bug hunter находит: 137 багов (critical: 5, high: 12, medium: 33, low: 87)
  Bug fixer исправляет: 137 багов
  Validation: type-check PASSED, build PASSED
  Verification (re-run bug-hunter): 14 NEW bugs (из-за рефакторинга)

Iteration 2:
  Bug hunter находит: 14 багов (critical: 0, high: 2, medium: 5, low: 7)
  Bug fixer исправляет: 14 багов
  Validation: type-check PASSED, build PASSED
  Verification: 2 REMAINING bugs (edge cases)

Iteration 3:
  Bug hunter находит: 2 бага (critical: 0, high: 0, medium: 1, low: 1)
  Bug fixer исправляет: 2 бага
  Validation: type-check PASSED, build PASSED
  Verification: 0 bugs

RESULT: Проект чистый, все баги исправлены
```

**Почему итеративный подход?** Потому что:
- Исправление багов → рефакторинг кода
- Рефакторинг → новые типизации
- Новые типизации → новые ошибки (временные)
- **Одна итерация не гарантирует** полного исправления

### Архитектура: Orchestrator + Workers + Iterative Loop

#### Компоненты

1. **bug-orchestrator** (оркестратор)
   - Создаёт plan files
   - Вызывает воркеров
   - Валидирует результаты
   - Управляет итерациями

2. **bug-hunter** (воркер детекции)
   - Сканирует кодовую базу
   - Находит баги
   - Категоризирует по приоритетам
   - Генерирует отчёт

3. **bug-fixer** (воркер исправления)
   - Читает отчёт bug-hunter
   - Исправляет баги по приоритетам
   - Запускает валидацию
   - Генерирует отчёт изменений

#### Итеративный цикл (детально)

```
┌─────────────────────────────────────────────────────────────┐
│ Iteration 1                                                 │
├─────────────────────────────────────────────────────────────┤
│ Phase 1: Detection                                          │
│   1. bug-orchestrator creates .bug-detection-plan.json     │
│      {                                                       │
│        "workflow": "bug-management",                         │
│        "phase": "detection",                                 │
│        "config": {                                           │
│          "priority": "all",                                  │
│          "categories": ["type-errors", "runtime", "security"]│
│        },                                                    │
│        "nextAgent": "bug-hunter"                             │
│      }                                                       │
│   2. bug-orchestrator signals readiness, EXITS              │
│   3. Main session invokes bug-hunter via Task tool          │
│   4. bug-hunter reads plan, scans codebase                  │
│   5. bug-hunter generates bug-hunting-report.md             │
│      Found: 137 bugs (critical: 5, high: 12, ...)           │
│   6. bug-hunter returns control, EXITS                      │
│   7. bug-orchestrator RESUMES                               │
│   8. bug-orchestrator validates report (quality gate)       │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: Fixing (Staged by Priority)                       │
│   9. bug-orchestrator creates .bug-fixing-critical-plan.json│
│      {                                                       │
│        "workflow": "bug-management",                         │
│        "phase": "fixing",                                    │
│        "config": {                                           │
│          "priority": "critical",                             │
│          "bugs": [<список critical багов из отчёта>]         │
│        },                                                    │
│        "nextAgent": "bug-fixer"                              │
│      }                                                       │
│  10. bug-orchestrator signals readiness, EXITS              │
│  11. Main session invokes bug-fixer via Task tool           │
│  12. bug-fixer reads plan, fixes critical bugs              │
│  13. bug-fixer runs validation (type-check + build)         │
│  14. bug-fixer generates bug-fixes-implemented.md           │
│      Fixed: 5 critical bugs                                 │
│  15. bug-fixer returns control, EXITS                       │
│  16. bug-orchestrator RESUMES                               │
│  17. bug-orchestrator validates fixes (quality gate)        │
│  18. REPEAT for high/medium/low priorities                  │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: Verification                                       │
│  19. bug-orchestrator creates .bug-verification-plan.json   │
│  20. Main session invokes bug-hunter AGAIN                  │
│  21. bug-hunter re-scans codebase                           │
│  22. bug-hunter finds: 14 NEW bugs (regression)             │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: Iteration Decision                                │
│  23. bug-orchestrator checks:                               │
│      - New bugs found? YES (14 bugs)                        │
│      - Iteration < maxIterations? YES (1 < 3)               │
│  24. Decision: GO TO Iteration 2                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Iteration 2                                                 │
├─────────────────────────────────────────────────────────────┤
│ [Повтор Phase 1-3 с новыми багами]                         │
│ Result: 2 remaining bugs                                    │
│ Decision: GO TO Iteration 3                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Iteration 3                                                 │
├─────────────────────────────────────────────────────────────┤
│ [Повтор Phase 1-3]                                          │
│ Result: 0 bugs                                              │
│ Decision: FINAL SUMMARY                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Phase 5: Final Summary                                     │
├─────────────────────────────────────────────────────────────┤
│  1. bug-orchestrator collects all reports                  │
│  2. Generates comprehensive summary:                        │
│     - Total bugs found: 153                                 │
│     - Total bugs fixed: 153                                 │
│     - Iterations: 3                                         │
│     - Time: ~45 minutes                                     │
│  3. Archives reports to docs/reports/bugs/2025-11/          │
│  4. Cleanup temporary files (.tmp/current/)                 │
└─────────────────────────────────────────────────────────────┘
```

### План файлы: Детальные примеры

#### .bug-detection-plan.json

```json
# Docs L1/L2: query @neuledge/context MCP first with package@version from the lockfile and domain/API keywords.
# Context7 calls below are L2 fallback only for L1 miss/stale/insufficient.
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
    "maxBugsPerRun": 1000,
    "scanDepth": "full"
  },
  "validation": {
    "required": ["report-exists", "type-check"],
    "optional": ["tests"]
  },
  "mcpGuidance": {
    "recommended": ["@neuledge/context MCP", "mcp__context7__* fallback"],
    "library": "react",
    "reason": "Validate React patterns before flagging as bugs"
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

**Поля:**
- `workflow`: Имя workflow (bug-management, security-audit, etc.)
- `phase`: Текущая фаза (detection, fixing, verification)
- `config`: Параметры работы воркера
- `validation`: Какие проверки запустить после выполнения
- `mcpGuidance`: Какие MCP серверы использовать и зачем
- `nextAgent`: Какой воркер должен обработать этот план
- `metadata`: Контекст (кто создал, номер итерации, лимиты)

#### .bug-fixing-critical-plan.json

```json
# Docs L1/L2: query @neuledge/context MCP first with package@version from the lockfile and domain/API keywords.
# Context7 calls below are L2 fallback only for L1 miss/stale/insufficient.
{
  "workflow": "bug-management",
  "phase": "fixing",
  "phaseNumber": 2,
  "config": {
    "priority": "critical",
    "bugs": [
      {
        "id": "BUG-001",
        "file": "src/api/database.ts",
        "line": 45,
        "description": "Memory leak in connection pool",
        "fix": "Implement automatic connection cleanup"
      },
      {
        "id": "BUG-002",
        "file": "src/auth/session.ts",
        "line": 123,
        "description": "Race condition in session management",
        "fix": "Add mutex lock"
      }
    ]
  },
  "validation": {
    "required": ["type-check", "build"],
    "optional": ["tests"]
  },
  "mcpGuidance": {
    "recommended": ["@neuledge/context MCP", "mcp__context7__* fallback"],
    "library": "node.js",
    "reason": "Check Node.js best practices for connection pooling"
  },
  "nextAgent": "bug-fixer",
  "timestamp": "2025-11-11T14:45:12.456Z",
  "metadata": {
    "createdBy": "bug-orchestrator",
    "iteration": 1,
    "maxIterations": 3,
    "previousPhase": "detection"
  }
}
```

### Итерационное дерево (визуализация)

```
Iteration 1
├── Phase 1: Detection
│   ├── bug-hunter: Scan full codebase
│   └── Result: 137 bugs found
├── Phase 2: Fixing (Priority: Critical)
│   ├── bug-fixer: Fix 5 critical bugs
│   ├── Validation: type-check ✅, build ✅
│   └── Result: 5 fixed
├── Phase 2: Fixing (Priority: High)
│   ├── bug-fixer: Fix 12 high bugs
│   ├── Validation: type-check ✅, build ✅
│   └── Result: 12 fixed
├── Phase 2: Fixing (Priority: Medium)
│   ├── bug-fixer: Fix 33 medium bugs
│   ├── Validation: type-check ✅, build ✅
│   └── Result: 33 fixed
├── Phase 2: Fixing (Priority: Low)
│   ├── bug-fixer: Fix 87 low bugs
│   ├── Validation: type-check ✅, build ✅
│   └── Result: 87 fixed
├── Phase 3: Verification
│   ├── bug-hunter: Re-scan codebase
│   └── Result: 14 NEW bugs (regression from refactoring)
└── Decision: CONTINUE (14 remaining, iteration 1 < 3)

Iteration 2
├── Phase 1: Detection (SKIP - already have list)
├── Phase 2: Fixing (All priorities)
│   ├── bug-fixer: Fix 14 bugs
│   ├── Validation: type-check ✅, build ✅
│   └── Result: 14 fixed
├── Phase 3: Verification
│   ├── bug-hunter: Re-scan codebase
│   └── Result: 2 REMAINING bugs (edge cases)
└── Decision: CONTINUE (2 remaining, iteration 2 < 3)

Iteration 3
├── Phase 2: Fixing
│   ├── bug-fixer: Fix 2 bugs
│   ├── Validation: type-check ✅, build ✅
│   └── Result: 2 fixed
├── Phase 3: Verification
│   ├── bug-hunter: Re-scan codebase
│   └── Result: 0 bugs
└── Decision: STOP (clean, generate summary)

Final Summary
├── Total bugs: 153
├── Total fixed: 153
├── Iterations: 3
├── Duration: ~45 minutes
└── Status: ✅ ALL BUGS FIXED
```

---

## Раздел 4: Skills Library — Архитектура переиспользуемых утилит

### Концепция: Skill vs Agent

**Skill** — это stateless утилита (<100 строк логики) для конкретной задачи.

**Agent** — это stateful workflow с изолированным контекстом.

| Критерий | Skill | Agent |
|----------|-------|-------|
| Контекст | Работает в контексте вызывающего | Изолированный контекст |
| Вызов | `Skill` tool | `Task` tool |
| Сложность | <100 строк | 200-650 строк |
| State | Stateless | Stateful |
| Пример | `run-quality-gate` | `bug-hunter` |

### Существующие Skills (15+)

**Validation Skills:**
- `run-quality-gate` - Выполнение type-check/build/tests
- `validate-plan-file` - Проверка JSON схемы plan file
- `validate-report-file` - Проверка полноты отчёта

**Reporting Skills:**
- `generate-report-header` - Генерация стандартизированных заголовков
- `format-markdown-table` - Форматирование markdown таблиц
- `format-todo-list` - Создание TodoWrite-совместимых списков
- `generate-changelog` - Генерация changelog из коммитов

**Utility Skills:**
- `parse-git-status` - Парсинг git status в структурированные данные
- `parse-error-logs` - Парсинг build/test/lint output
- `calculate-priority-score` - Подсчёт priority score для багов/задач
- `rollback-changes` - Откат изменений по changes log
- `render-template` - Подстановка переменных в шаблоны

### Пример: run-quality-gate (полный код)

**Файл**: `.claude/skills/run-quality-gate/SKILL.md`

```markdown
---
name: run-quality-gate
description: Execute quality gate validation with configurable blocking behavior. Use when running type-check, build, tests, lint, or custom validation commands in orchestrators or workers to enforce quality standards.
allowed-tools: Bash, Read
---

# Run Quality Gate

Execute validation commands as quality gates with configurable blocking/non-blocking behavior and structured error reporting.

## When to Use

- Type-check validation in pre-flight or quality gates
- Build validation before releases
- Test execution as quality gate
- Lint validation for code quality
- Custom validation commands

## Instructions

### Step 1: Receive Gate Configuration

Accept gate configuration as input.

**Expected Input**:
```json
{
  "gate": "type-check|build|tests|lint|custom",
  "blocking": true,
  "custom_command": "pnpm custom-validate"
}
```

### Step 2: Map Gate to Command

Determine command to execute based on gate type.

**Gate Commands**:
- `type-check` → `pnpm type-check`
- `build` → `pnpm build`
- `tests` → `pnpm test`
- `lint` → `pnpm lint`
- `custom` → Use `custom_command` parameter

### Step 3: Execute Command

Run command via Bash tool with timeout.

**Execution Parameters**:
- Timeout: 300000ms (5 minutes)
- Capture stdout and stderr
- Record exit code
- Track execution duration

### Step 4: Parse Exit Code and Output

Determine if gate passed based on exit code.

**Pass/Fail Logic**:
- Exit code 0 → Passed
- Exit code non-zero → Failed

### Step 5: Determine Action

Calculate action based on result and blocking flag.

**Action Logic**:
```
IF exit_code == 0:
  action = "continue"
  passed = true
ELSE:
  IF blocking == true:
    action = "stop"
  ELSE:
    action = "warn"
  passed = false
```

### Step 6: Return Structured Result

Return complete quality gate result.

**Expected Output**:
```json
{
  "gate": "type-check",
  "passed": true,
  "blocking": true,
  "action": "continue",
  "errors": [],
  "exit_code": 0,
  "duration_ms": 2345,
  "command": "pnpm type-check",
  "timestamp": "2025-11-11T14:30:00Z"
}
```
```

**Использование в воркере:**

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

### Создание нового Skill (через skill-builder-v2)

**Процесс:**

1. Пользователь: "Create skill for parsing TypeScript error output"
2. skill-builder-v2 спрашивает:
   - Skill name? → `parse-typescript-errors`
   - Input format? → Raw TypeScript compiler output (string)
   - Output format? → Structured array of errors with file, line, message
   - Tools needed? → Bash (to run tsc), Read (to parse)
3. skill-builder-v2 генерирует `.claude/skills/parse-typescript-errors/SKILL.md`
4. Валидация: проверка что <100 строк логики, stateless, чёткий input/output
5. Сохранение

**Результат** (2-3 минуты):

```markdown
---
name: parse-typescript-errors
description: Parse TypeScript compiler output into structured error data. Use when processing tsc output for quality gates or reports.
allowed-tools: Bash, Read
---

# Parse TypeScript Errors

## Input Format
```json
{
  "tsc_output": "string (raw TypeScript compiler output)"
}
```

## Output Format
```json
{
  "errors": [
    {
      "file": "src/app.ts",
      "line": 42,
      "column": 15,
      "code": "TS2322",
      "message": "Type 'string' is not assignable to type 'number'"
    }
  ],
  "error_count": 1
}
```

## Instructions

1. Split tsc_output by newlines
2. For each line matching pattern `{file}:{line}:{column} - error TS{code}: {message}`:
   - Extract file, line, column, code, message
   - Add to errors array
3. Count total errors
4. Return structured result
```

---

## Раздел 5: Файловая организация и JSON-схемы

### Структура директорий

```
.claude/
├── agents/
│   ├── health/
│   │   ├── orchestrators/
│   │   │   ├── bug-orchestrator.md
│   │   │   ├── security-orchestrator.md
│   │   │   ├── dead-code-orchestrator.md
│   │   │   └── dependency-orchestrator.md
│   │   └── workers/
│   │       ├── bug-hunter.md
│   │       ├── bug-fixer.md
│   │       ├── security-scanner.md
│   │       ├── vulnerability-fixer.md
│   │       ├── dead-code-hunter.md
│   │       └── dead-code-remover.md
│   ├── meta/
│   │   └── workers/
│   │       ├── meta-agent-v3.md
│   │       └── skill-builder-v2.md
│   └── speckit/
│       ├── orchestrators/
│       │   └── planning-orchestrator.md
│       └── workers/
│           └── task-executor.md
├── commands/
│   ├── health-bugs.md
│   ├── health-security.md
│   ├── health-deps.md
│   ├── health-cleanup.md
│   ├── worktree-create.md
│   ├── worktree-list.md
│   ├── worktree-remove.md
│   └── push.md
├── skills/
│   ├── run-quality-gate/
│   │   └── SKILL.md
│   ├── validate-plan-file/
│   │   └── SKILL.md
│   ├── validate-report-file/
│   │   └── SKILL.md
│   ├── generate-report-header/
│   │   └── SKILL.md
│   ├── parse-error-logs/
│   │   └── SKILL.md
│   ├── rollback-changes/
│   │   └── SKILL.md
│   └── [... 9 more skills ...]
└── schemas/
    ├── base-plan.schema.json
    ├── bug-plan.schema.json
    ├── security-plan.schema.json
    ├── dead-code-plan.schema.json
    └── dependency-plan.schema.json

.tmp/
├── current/
│   ├── plans/
│   │   ├── .bug-detection-plan.json
│   │   ├── .bug-fixing-critical-plan.json
│   │   └── .bug-verification-plan.json
│   ├── changes/
│   │   ├── .bug-changes.json
│   │   └── .security-changes.json
│   ├── backups/
│   │   └── .rollback/
│   │       ├── src-api-database.ts.backup
│   │       └── src-auth-session.ts.backup
│   └── reports/
│       ├── bug-hunting-report.md
│       └── security-audit.md
└── archive/
    └── 2025-11-11-14-30-00/
        ├── plans/
        ├── changes/
        └── reports/

docs/
└── reports/
    ├── bugs/
    │   └── 2025-11/
    │       ├── 2025-11-11-bug-hunting-report.md
    │       └── 2025-11-11-bug-fixes-implemented.md
    ├── security/
    │   └── 2025-11/
    │       └── 2025-11-11-security-audit.md
    └── summaries/
        └── 2025-11-11-health-summary.md

mcp/
├── .mcp.base.json      (~600 tokens)
├── .mcp.supabase.json  (~2500 tokens)
├── .mcp.frontend.json  (~2000 tokens)
└── .mcp.full.json      (~5000 tokens)
```

**Принципы организации:**

1. **Agents** по доменам (`health/`, `meta/`, `speckit/`)
2. **Commands** (19+ slash-команд) в одной директории
3. **Skills** (15+) — каждый в своей папке с `SKILL.md`
4. **Temporary files** в `.tmp/current/` (автоочистка после 7 дней)
5. **Permanent reports** в `docs/reports/{domain}/{YYYY-MM}/`

### JSON Schemas для Plan Files

#### base-plan.schema.json (базовая схема)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["workflow", "phase", "nextAgent", "timestamp"],
  "properties": {
    "workflow": {
      "type": "string",
      "enum": ["bug-management", "security-audit", "dead-code-cleanup", "dependency-update"]
    },
    "phase": {
      "type": "string",
      "enum": ["detection", "fixing", "verification", "audit", "update", "cleanup"]
    },
    "phaseNumber": {
      "type": "integer",
      "minimum": 1
    },
    "config": {
      "type": "object",
      "description": "Domain-specific configuration"
    },
    "validation": {
      "type": "object",
      "properties": {
        "required": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["report-exists", "type-check", "build", "tests", "no-critical-errors"]
          }
        },
        "optional": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "mcpGuidance": {
      "type": "object",
      "properties": {
        "recommended": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "library": {
          "type": "string"
        },
        "reason": {
          "type": "string"
        }
      }
    },
    "nextAgent": {
      "type": "string",
      "description": "Worker agent to invoke for this plan"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "createdBy": {
          "type": "string"
        },
        "iteration": {
          "type": "integer",
          "minimum": 1
        },
        "maxIterations": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10
        }
      }
    }
  }
}
```

#### bug-plan.schema.json (специфика для багов)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "allOf": [
    { "$ref": "base-plan.schema.json" }
  ],
  "properties": {
    "config": {
      "type": "object",
      "required": ["priority"],
      "properties": {
        "priority": {
          "type": "string",
          "enum": ["all", "critical", "high", "medium", "low"]
        },
        "categories": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "type-errors",
              "runtime-errors",
              "security",
              "performance",
              "dead-code",
              "debug-code"
            ]
          }
        },
        "maxBugsPerRun": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10000
        },
        "bugs": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "file", "line", "description"],
            "properties": {
              "id": {
                "type": "string",
                "pattern": "^BUG-[0-9]{3,}$"
              },
              "file": {
                "type": "string"
              },
              "line": {
                "type": "integer",
                "minimum": 1
              },
              "description": {
                "type": "string"
              },
              "fix": {
                "type": "string"
              }
            }
          }
        }
      }
    }
  }
}
```

**Валидация schema** (в оркестраторе):

```markdown
## After Creating Plan File

Use `validate-plan-file` Skill with:
- plan_file_path: `.tmp/current/plans/.bug-detection-plan.json`
- schema_path: `.claude/schemas/bug-plan.schema.json`

If validation fails:
- Report schema errors
- Fix plan file
- Re-validate
- Only proceed when valid
```

---

## Результаты: Измеримые улучшения

Эти цифры — из реальной практики AI Dev Team за последние 2 года.

### Скорость разработки

**До оркестратора:**
- Создание нового feature агента: 1-2 часа вручную
- Запуск health workflow: ~10 минут setup + manual execution
- Параллельная разработка: 1-2 фичи максимум

**С оркестратором:**
- Создание агента через meta-agent-v3: **2-3 минуты**
- Запуск health workflow: **1 команда** (`/health-bugs`)
- Параллельная разработка: **5-7 проектов** через worktrees

**Ускорение**: **~70% быстрее** на рутинных задачах.

### Качество кода

**До оркестратора:**
- Проверка кода: Manual code review (1-2 часа)
- Детекция багов: Reactive (после деплоя)
- Security audit: Раз в квартал (если вспомнили)

**С оркестратором:**
- Проверка кода: Автоматически после каждой задачи (type-check + build + tests)
- Детекция багов: Proactive (`/health-bugs` перед деплоем)
- Security audit: `/health-security` по требованию или по расписанию

**Результат**: **Меньше багов в продакшене**, систематический подход к качеству.

### Контекстное окно

**Standard Claude Code:**
- После 3-4 задач: ~30K токенов
- После недели: ~50K токенов (непригодно для работы)
- Решение: Начать новую сессию (потеря контекста)

**Orchestrator Kit:**
- Главный оркестратор: стабильно **~10-15K токенов**
- Субагенты: изолированный контекст (сброс после задачи)
- Можно работать над проектом **бесконечно долго**

**Экономия**: **60-70% контекстного бюджета**.

---

## Дисклеймер: Ожидаемая критика

Понимаю, что эта статья вызовет критику со стороны разработчиков. В первой части я уже затронул тему **страха + надменности**.

Здесь добавлю: Да, система сложная. Да, есть overhead на создание агентов. Да, не для всех проектов это нужно.

**Но:**
- Мы используем это на **реальных клиентских проектах**
- Измеримые результаты: -80% cost, 1-2 weeks vs 2-3 months
- Всё **открыто и бесплатно** (MIT license)

**Если не согласны** — склонируйте репо, попробуйте `/health-bugs`, запустите meta-agent-v3. **Потом** — критикуйте с техническими аргументами.

---

## Анонс Part 3: Практические кейсы

**Часть 3** (выйдет через 1-2 недели): Практические кейсы и рабочие процессы
- Реальные примеры из AI Dev Team (с цифрами)
- Worktree workflow для 5-7 параллельных фич (как мы это делаем)
- MCP switching стратегии (когда что использовать, токены)
- Lessons learned за 2 года работы (что сработало, что нет)
- Integration с CI/CD (GitHub Actions + health workflows)

---

## Контакты и обратная связь

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/maslennikovigor

У меня там всего 73 подписчика. Буду очень рад, если кто-то из вас станет сотым. Пишу редко, но когда пишу — стараюсь, чтобы было по делу.

**Прямой контакт** (для обсуждений): https://t.me/maslennikovig

Нужно обсудить напрямую? Пишите. Всегда открыт к диалогу.

### 💬 Обратная связь: я широко открыт

**Буду очень рад услышать**:
- **Критику** — Что не так с этим подходом? Где слабые места архитектуры?
- **Идеи** — Какие фичи добавить? Чего не хватает в воркерах?
- **Предложения** — Как улучшить meta-agent-v3? Как оптимизировать Skills?
- **Вопросы** — Что-то неясно в 5-фазной структуре? Спрашивайте.

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
**NPM**: `npm install -g claude-code-orchestrator-kit`
**Лицензия**: MIT (полностью бесплатно для коммерческого использования)

---

*Продолжение следует: Часть 3 — Практические кейсы и lessons learned (через 1-2 недели)*
