---
platform: habr
title: "Новые скиллы для Claude Code: systematic-debugging, senior-devops, senior-prompt-engineer"
author: Igor Maslennikov
date: 2025-12-26
length: 23847 characters
tags: AI, Claude Code, debugging, DevOps, prompt engineering, orchestration, automation
language: ru
---

# Новые скиллы для Claude Code: systematic-debugging, senior-devops, senior-prompt-engineer

> **TL;DR**: Я проанализировал 14 новых скиллов для Claude Code Orchestrator Kit. 5 из них критически полезны и уже интегрированы с агентами. Главный герой — **systematic-debugging** — методология систематического дебага вместо хаотичного "угадывания" фиксов. В статье — подробный разбор архитектуры, код, практическая интеграция с агентами.

---

## Контекст: Игорь Масленников

Я в IT с 2013 года. Последние 2 года активно развиваю AI-направление в DNA IT (AI Dev Team). Результат: клиенты всё чаще выбирают AI-отдел вместо традиционных команд разработчиков. Причина простая — быстрее (1-2 недели вместо 2-3 месяцев), дешевле (-80% затрат), качественнее (автоматизированные проверки).

Всё, о чём я пишу, — протестировано на реальных клиентских проектах. Никакой теории ради теории. Только практика.

---

## Проблема: Хаотичный дебаг и "угадывание" фиксов

Классическая ситуация:
1. Баг обнаружен
2. Разработчик смотрит на код
3. "Наверное, проблема здесь"
4. Чинит
5. Запускает тесты
6. Не работает
7. "Тогда, может быть, проблема в другом месте"
8. Чинит снова
9. Повторяет N раз до победы

Знакомо? Я называю это **"угадывание фиксов"** (guess-and-check debugging).

**Почему это плохо?**
- **Тратится время**: Каждая итерация = минуты (или часы для сложных багов)
- **Нет понимания root cause**: Чинишь симптомы, а не причину
- **Технический долг растёт**: Фиксы накладываются друг на друга без системного анализа
- **После 3-го фикса**: Понимаешь, что проблема в архитектуре, а не в конкретном файле

**Ещё хуже в AI-ассистированной разработке:**
- Claude Code пытается починить баг → фикс не работает
- Пытается снова → фикс частично работает
- Пытается третий раз → контекст переполняется
- В итоге: баг не починен, контекст сожжён

Я столкнулся с этим на клиентских проектах. Агент `bug-fixer` умел находить баги, но не умел **системно** их чинить. Результат — 50% багов чинились с первой попытки, остальные требовали N итераций.

Нужна была **методология**, а не просто "попробуй ещё раз".

---

## Решение: systematic-debugging Skill

В декабре 2025 я проанализировал 14 новых скиллов, доступных в Claude Code. Среди них был **systematic-debugging** — методология систематического дебага вместо "угадывания" фиксов.

**Что это такое?**

Systematic-debugging — это **скилл** (не агент!), который содержит:
- Структурированный 4-фазный процесс дебага
- Правило "3 фикса = пересмотр архитектуры"
- Методологию трассировки данных в многокомпонентных системах
- Decision tree для выбора подхода

**Разница между скиллом и агентом:**
- ✅ **Скилл**: Переиспользуемая утилита (<100 строк), stateless, вызывается через `Skill` tool
- ✅ **Агент**: Изолированный контекст, stateful, вызывается через `Task` tool

Скиллы — это **knowledge base** + **execution logic**, которые агенты используют для выполнения специфических задач.

---

## Архитектура: 4 фазы systematic-debugging

### Фаза 1: Root Cause Analysis

**Цель**: Понять **причину** бага, а не симптом.

**Методология:**

1. **Reproduce the bug**:
   - Создать минимальный воспроизводимый пример
   - Записать точные шаги воспроизведения
   - Определить окружение (OS, версии, конфигурация)

2. **Trace data flow**:
   - Проследить путь данных от входа до ошибки
   - Найти точку, где данные становятся некорректными
   - Использовать breakpoints / логи / assertions

3. **Identify root cause**:
   - НЕ чинить симптом ("null check тут решит проблему")
   - Понять, **почему** данные стали null
   - Проверить upstream: откуда приходят данные?

**Пример** (из реального клиентского проекта):

```typescript
// ❌ WRONG: Чинит симптом
function processUser(user: User | null) {
  if (!user) {
    console.error('User is null');
    return;
  }
  // ...
}

// ✅ RIGHT: Чинит root cause
// Проблема была в async/await:
// fetchUser() возвращал Promise<User>, но мы не ждали resolve
async function processUser(userId: string) {
  const user = await fetchUser(userId); // Теперь ждём
  // ...
}
```

**Правило**: Если не уверен в root cause — **НЕ чини**. Сначала понимание, потом фикс.

---

### Фаза 2: Pattern Analysis

**Цель**: Понять, это **изолированный баг** или **системная проблема**.

**Вопросы:**

1. **Сколько мест затронуто?**
   - Одна функция → локальный фикс
   - 5+ файлов → системная проблема

2. **Есть ли похожие баги в истории?**
   - `git log --grep="similar issue"` (искать похожие фиксы)
   - Если да — это **pattern**, а не одноразовый баг

3. **Нарушена ли архитектурная граница?**
   - Например: компонент UI напрямую работает с БД (минуя API)
   - Или: бизнес-логика в контроллере вместо сервисного слоя

**Правило "3 фикса = пересмотр архитектуры":**

Если для фикса нужно **изменить 3+ файла** в разных модулях — это сигнал:
- ❌ НЕ чини каждый файл отдельно
- ✅ Пересмотри архитектуру: возможно, нужен рефакторинг

**Пример** (из реального проекта):

```
Баг: "Валидация email не работает в 3 местах"

Плохое решение:
- Добавить регулярку в компонент A
- Добавить регулярку в компонент B
- Добавить регулярку в компонент C

Хорошее решение:
- Создать @/lib/validators/email.ts
- Использовать валидатор во всех 3 компонентах
- Добавить тесты для валидатора

Результат: 1 источник правды вместо 3 копий
```

---

### Фаза 3: Hypothesis Generation

**Цель**: Сформулировать **проверяемую гипотезу** о причине бага.

**Структура гипотезы:**

```
Hypothesis:
  The bug occurs because [specific technical reason].

Evidence:
  - [Observation 1]: [What you saw in logs/code]
  - [Observation 2]: [What you saw in tests]

Prediction:
  If I [specific change], then [expected outcome].

Validation:
  Test by [specific test case].
```

**Пример** (реальный баг в Supabase-проекте):

```
Hypothesis:
  The "undefined is not a function" error occurs because
  supabase.auth.getSession() returns null when user is logged out,
  and we call .data.session.user without null-check.

Evidence:
  - Error stack trace points to auth.ts:42
  - Error happens ONLY when user is logged out
  - getSession() docs say: returns null if no session

Prediction:
  If I add optional chaining (?.), the error will disappear.

Validation:
  Test: Log out user → navigate to /profile → should not crash
```

**Правило**: Гипотеза должна быть **проверяемой** (testable). Если не можешь написать тест — гипотеза слишком расплывчатая.

---

### Фаза 4: Implementation & Verification

**Цель**: Применить фикс, проверить, что он работает, убедиться, что не сломал ничего другого.

**Шаги:**

1. **Implement fix** (based on hypothesis)
2. **Run targeted test** (the one from hypothesis)
3. **Run full test suite** (regression check)
4. **Manual verification** (if applicable)
5. **Code review self-check** (did I follow best practices?)

**Quality gates** (обязательные):

```bash
# 1. Type-check
pnpm type-check

# 2. Build
pnpm build

# 3. Tests
pnpm test

# 4. Lint (optional, but recommended)
pnpm lint
```

**Если хотя бы один gate провалился** — фикс откатывается.

**Правило**: Фикс **НЕ считается завершённым**, пока все quality gates не пройдены.

---

## Интеграция: Как systematic-debugging работает с bug-fixer агентом

### До интеграции

**bug-fixer агент** (старая версия):

```markdown
## Phase 2: Implement Fixes

For each bug from plan file:
1. Read bug description
2. Locate affected files
3. Implement fix
4. Run type-check
5. If failed: try again
```

**Проблема**: Нет **методологии**. Агент пытается починить баг напрямую, без анализа root cause.

**Результат**: 50% багов чинятся с первой попытки, остальные требуют N итераций.

---

### После интеграции

**bug-fixer агент** (новая версия с systematic-debugging):

```markdown
## Phase 2: Apply Systematic Debugging

**CRITICAL**: Use `systematic-debugging` Skill BEFORE implementing fix.

### Step 1: Root Cause Analysis (Skill Phase 1)
- Reproduce the bug (create minimal example)
- Trace data flow (from input to error)
- Identify root cause (NOT symptom)

### Step 2: Pattern Analysis (Skill Phase 2)
- Check: How many files affected?
  - 1 file → proceed with fix
  - 3+ files → STOP, report "architectural issue"
- Search git history for similar bugs
- Verify architectural boundaries

### Step 3: Hypothesis Generation (Skill Phase 3)
- Formulate hypothesis (technical reason)
- Gather evidence (logs, stack trace, code)
- Predict outcome (if I change X, then Y)
- Define validation test

### Step 4: Implementation (Skill Phase 4)
- Implement fix based on hypothesis
- Run targeted test (from hypothesis)
- Run quality gates (type-check + build + tests)
- If ANY gate failed: rollback, report failure

**Quality Gate Rules**:
- ✅ All gates passed → proceed to Phase 3
- ❌ Any gate failed → rollback changes, mark bug as "failed", report to orchestrator
```

**Что изменилось:**

1. **Структура**: Вместо "попробуй починить" → 4-фазный процесс
2. **Правило "3 фикса"**: Автоматическая эскалация архитектурных проблем
3. **Гипотеза**: Агент формулирует проверяемую гипотезу перед фиксом
4. **Rollback**: Автоматический откат при провале quality gates

---

### Практический пример: /health-bugs workflow

**Команда**: `/health-bugs`

**Workflow**:

```
1. bug-orchestrator (создаёт план)
   ↓
2. bug-hunter (сканирует код, находит баги)
   ↓
3. bug-orchestrator (валидирует отчёт)
   ↓
4. bug-fixer (+ systematic-debugging) → ЧИНИТ БАГИ СИСТЕМНО
   ↓
5. Quality gates (type-check + build + tests)
   ↓
6. Verification phase (повторный запуск bug-hunter)
   ↓
7. Итерация (если баги остались: шаг 4-6 снова)
   ↓
8. Final summary
```

**Ключевое отличие**: На шаге 4 агент **bug-fixer** теперь использует **systematic-debugging Skill**, а не просто "чинит напрямую".

**Результат** (на реальных проектах):

- **До интеграции**: 50% багов с первой попытки, 3-5 итераций для сложных багов
- **После интеграции**: 85% багов с первой попытки, 1-2 итерации для сложных багов
- **Контекст**: Экономия ~30% контекста (меньше итераций = меньше токенов)

---

## Другие критически полезные скиллы

Помимо systematic-debugging, я интегрировал ещё 4 скилла:

### 2. senior-devops: CI/CD как код

**Назначение**: CI/CD pipelines, Terraform, Kubernetes, deployment strategies.

**Ключевые компоненты:**
- **Pipeline Generator**: Создание GitHub Actions / GitLab CI / Jenkins pipelines
- **Terraform Scaffolder**: Генерация IaC для AWS/GCP/Azure
- **Deployment Manager**: Blue-green / canary / rolling deployments

**Интеграция**: Используется агентом **deployment-engineer**.

**Пример** (генерация GitHub Actions workflow):

```yaml
# Генерируется senior-devops Skill
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality-gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: pnpm/action-setup@v2
      - run: pnpm install --frozen-lockfile
      - run: pnpm type-check
      - run: pnpm build
      - run: pnpm test

  deploy:
    needs: quality-gates
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Deployment script (blue-green strategy)
          ./scripts/deploy.sh --strategy=blue-green
```

**Почему полезно:**

- **Референсы по IaC**: Best practices для Terraform / Pulumi
- **Deployment strategies**: Готовые паттерны для blue-green / canary
- **Security**: Проверка секретов, scan контейнеров

---

### 3. senior-prompt-engineer: Оптимизация промптов

**Назначение**: LLM optimization, prompt patterns, RAG, agent orchestration.

**Ключевые компоненты:**
- **Prompt Optimizer**: Улучшение промптов для точности и эффективности
- **RAG Evaluator**: Оценка качества Retrieval-Augmented Generation
- **Agent Design Patterns**: Паттерны для agentic систем

**Интеграция**: Используется агентом **meta-agent-v3** (создание новых агентов).

**Пример** (оптимизация промпта):

**До оптимизации:**

```markdown
You are a code reviewer. Review the code.
```

**После оптимизации** (senior-prompt-engineer):

```markdown
You are a Senior Code Reviewer specialized in TypeScript/React.

**Your responsibilities:**
1. Check for type safety issues (any types, missing null checks)
2. Identify performance bottlenecks (unnecessary re-renders, memory leaks)
3. Verify architectural boundaries (UI components should not call DB directly)
4. Suggest improvements (code quality, readability, maintainability)

**Output format:**
- Severity: Critical | High | Medium | Low
- Issue: [Brief description]
- Location: [File:line]
- Suggestion: [How to fix]
```

**Разница:**

- ✅ Структура: Чёткие обязанности вместо "review the code"
- ✅ Специализация: TypeScript/React вместо generic
- ✅ Формат вывода: Стандартизированный формат отчёта

**Результат**: Агенты создают **более точные** и **более полезные** промпты для новых агентов.

---

### 4. webapp-testing: E2E тестирование через Playwright

**Назначение**: Тестирование веб-приложений через Playwright.

**Ключевые компоненты:**
- **with_server.py**: Управление серверами (запуск/остановка)
- **Reconnaissance-then-action pattern**: Сначала исследуй UI, потом действуй
- **Decision tree**: Выбор подхода (CSS selectors vs text content vs ARIA labels)

**Интеграция**: Используется после агента **test-writer** в test workflow.

**Пример** (Playwright тест):

```typescript
// Генерируется webapp-testing Skill
import { test, expect } from '@playwright/test';

test('User login flow', async ({ page }) => {
  // Phase 1: Reconnaissance
  await page.goto('http://localhost:3000/login');
  const loginForm = page.locator('form[data-testid="login-form"]');
  expect(loginForm).toBeVisible();

  // Phase 2: Action
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Phase 3: Verification
  await expect(page).toHaveURL(/dashboard/);
  const welcomeMessage = page.locator('h1:has-text("Welcome")');
  expect(welcomeMessage).toBeVisible();
});
```

**Decision tree** (когда использовать какой селектор):

```
IF element has data-testid → use data-testid (most stable)
ELSE IF element has unique ARIA label → use ARIA (accessible)
ELSE IF element has unique text → use text content (readable)
ELSE use CSS selector (least stable, but works)
```

**Почему полезно:**

- **E2E покрытие**: Тестирование реального user flow
- **Regression detection**: Ловит UI-баги до продакшена
- **Integration**: Работает с MCP Playwright сервером

---

### 5. code-reviewer (skill): Автоматизированный code review

**Назначение**: Автоматизированный code review с чек-листами и best practices.

**Ключевые компоненты:**
- **PR Analyzer**: Анализ pull request (scope, risk, complexity)
- **Code Quality Checker**: Проверка антипаттернов, code smells
- **Review Report Generator**: Стандартизированный отчёт

**Интеграция**: Объединён с агентом **code-reviewer** (agent).

**Важная деталь:**

- ✅ **Скилл**: Содержит **knowledge base** (чек-листы, антипаттерны, best practices)
- ✅ **Агент**: Содержит **execution logic** (как читать PR, как генерировать отчёт)
- ✅ **Связь**: Агент **ссылается** на скилл для получения knowledge base

**Пример** (чек-лист из code-reviewer Skill):

```markdown
## TypeScript Code Review Checklist

### Type Safety
- [ ] No `any` types (use `unknown` or specific types)
- [ ] All function parameters have types
- [ ] Return types explicitly declared (no implicit `any`)
- [ ] Null checks for nullable values (`user?.name` or `if (user)`)

### Performance
- [ ] No unnecessary re-renders (React.memo, useMemo, useCallback)
- [ ] Async operations properly handled (loading states, error handling)
- [ ] Large lists virtualized (react-window or similar)

### Architecture
- [ ] UI components do NOT call database directly (use API layer)
- [ ] Business logic NOT in controllers (use service layer)
- [ ] Separation of concerns (UI, logic, data)

### Security
- [ ] No hardcoded credentials (use env vars)
- [ ] User input sanitized (SQL injection, XSS prevention)
- [ ] Authentication/authorization checks
```

**Результат**: Агент **code-reviewer** генерирует детальные отчёты на основе этого чек-листа.

---

## План интеграции: Связь скиллов с агентами

### Фаза 1: Связать скиллы с агентами

```
bug-fixer agent
  └── references: systematic-debugging skill

deployment-engineer agent
  └── references: senior-devops skill

code-reviewer agent
  └── references: code-reviewer skill (merge knowledge)

meta-agent-v3 agent
  └── references: senior-prompt-engineer skill
```

**Как это работает:**

В промпте агента добавляется ссылка на скилл:

```markdown
## Phase 2: Execute Work

**CRITICAL**: Before implementing fix, apply `systematic-debugging` Skill.

Follow Skill phases:
1. Root Cause Analysis
2. Pattern Analysis
3. Hypothesis Generation
4. Implementation & Verification

Refer to `systematic-debugging` Skill for detailed methodology.
```

**Преимущества:**

- **Consistency**: Все агенты используют одну методологию
- **Maintainability**: Обновил скилл → обновились все агенты
- **Clarity**: Агенты фокусируются на execution, скиллы — на knowledge

---

### Фаза 2: Добавить в workflows

```
/health-bugs workflow:
  bug-hunter → bug-fixer (+ systematic-debugging) → verify

Test workflow:
  test-writer → webapp-testing → verify

Code review workflow:
  code-reviewer (agent + skill) → report
```

**Пример**: `/health-bugs` с systematic-debugging

**До интеграции:**

```
bug-hunter находит 20 багов
  ↓
bug-fixer чинит все 20 за раз
  ↓
Результат: 10 исправлено, 10 провалено, контекст переполнен
```

**После интеграции:**

```
bug-hunter находит 20 багов
  ↓
bug-fixer чинит по приоритету (critical → high → medium → low)
  ↓
Для КАЖДОГО бага: systematic-debugging (4 фазы)
  ↓
Quality gates после каждого фикса
  ↓
Rollback при провале
  ↓
Результат: 17 исправлено, 3 эскалировано как "архитектурные проблемы"
```

**Ключевое отличие:** Systematic-debugging **эскалирует архитектурные проблемы** вместо бесконечных попыток фикса.

---

### Фаза 3: Cleanup (что НЕ интегрировал)

Из 14 новых скиллов я **НЕ** интегрировал:

- **move-code-quality**: Нишевый язык (Move blockchain), не наш tech stack
- **lead-research-assistant**: Sales/BD, не связан с разработкой
- **ux-researcher-designer**: UX research, не для CLI toolkit
- **content-research-writer**: Дублирует article-writer-multi-platform

**Причина**: Засоряют список скиллов, не приносят ценности для orchestrator kit.

**Рекомендация**: Оставить для специфических use cases (creative проекты, marketing).

---

## Выводы и метрики

### Что я получил от интеграции

**Скиллы интегрированы**: 5 (systematic-debugging, senior-devops, senior-prompt-engineer, webapp-testing, code-reviewer)

**Агенты улучшены**: 4 (bug-fixer, deployment-engineer, meta-agent-v3, code-reviewer)

**Метрики** (на реальных проектах):

| Метрика | До интеграции | После интеграции | Изменение |
|---------|---------------|------------------|-----------|
| Баги исправлены с 1-й попытки | 50% | 85% | **+35%** |
| Средние итерации на баг | 3-5 | 1-2 | **-60%** |
| Контекст на фикс (токены) | ~15K | ~10K | **-33%** |
| Эскалация архитектурных проблем | 0% (чинили вручную) | 15% (автоматическая) | **+15%** |

**Ключевое улучшение:**

- **Systematic-debugging** сократил "угадывание фиксов" на **60%**
- **Senior-devops** стандартизировал CI/CD (раньше каждый проект — уникальный workflow)
- **Senior-prompt-engineer** улучшил качество новых агентов (создаваемых meta-agent-v3)
- **Webapp-testing** добавил E2E покрытие (раньше только unit-тесты)

---

### Что дальше?

**Планы:**

1. **Интеграция с health workflows**: Добавить systematic-debugging в `/health-security` и `/health-deps`
2. **Automatic skill selection**: Meta-agent-v3 автоматически выбирает релевантные скиллы при создании агента
3. **Skill versioning**: Отслеживание версий скиллов (для обратной совместимости)

**Открытые вопросы:**

- Как обрабатывать конфликты скиллов? (Например, 2 скилла для одной задачи)
- Стоит ли создавать **skill marketplace**? (Community-contributed skills)
- Как измерять ROI скиллов? (Какие метрики важны?)

---

## Disclaimer: Expected Pushback

Я понимаю, что эта статья вызовет критику от разработчиков. "AI не может делать настоящий code review", "Systematic-debugging — это просто очевидные шаги", "Senior-devops — переусложнение".

**Моя позиция**: Я думаю, эта реакция больше о **страхе, смешанном с высокомерием**, чем о технической критике.

**Страх**: "Если AI может делать code review, что случится со мной?"
**Высокомерие**: "Только люди могут писать *настоящий* код, AI — просто игрушка."

**Реальность**: AI не заменяет хороших разработчиков. Он их **усиливает**. Systematic-debugging не заменяет навыки дебага — он их **структурирует**. Senior-devops не заменяет DevOps-инженера — он **стандартизирует** best practices.

Если не согласны — окей. Клонируйте репозиторий, попробуйте, **потом** критикуйте. Я предпочитаю технические аргументы эмоциональным реакциям.

---

## Установка и начало работы

**NPM установка:**

```bash
npm install -g claude-code-orchestrator-kit
# или
npx claude-code-orchestrator-kit
```

**Ручная установка:**

```bash
git clone https://github.com/maslennikov-ig/claude-code-orchestrator-kit.git
cd claude-code-orchestrator-kit
cp .env.example .env.local  # Настроить credentials
./switch-mcp.sh  # Выбрать MCP конфигурацию
# Перезапустить Claude Code
```

**Первые шаги:**

1. Скопировать `.claude/` в ваш проект
2. Скопировать `mcp/` конфигурации
3. Скопировать `CLAUDE.md` (behavioral OS)
4. Настроить `.env.local`
5. Запустить `./switch-mcp.sh` → выбрать BASE
6. Перезапустить Claude Code
7. Попробовать `/health-bugs` для проверки

**Проверка интеграции systematic-debugging:**

```bash
# Запустить /health-bugs workflow
/health-bugs

# Наблюдать:
# 1. bug-hunter находит баги
# 2. bug-fixer применяет systematic-debugging (4 фазы)
# 3. Quality gates после каждого фикса
# 4. Эскалация архитектурных проблем (если 3+ файла)
```

---

## Contact & Feedback

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/maslennikovigor
Заходите, читайте мои мысли и статьи. Я пишу не часто, но когда пишу — это того стоит.

**Прямой контакт**: https://t.me/maslennikovig
Нужно поговорить? Пишите напрямую. Всегда рад общению.

### 💬 Feedback: Я открыт

**Я хочу услышать:**
- **Критику** — Что не так с этим подходом? Где слабые места?
- **Идеи** — Какие функции добавить? Чего не хватает?
- **Предложения** — Как улучшить, оптимизировать, рефакторить систему?
- **Вопросы** — Что-то непонятно? Спрашивайте.

**Каналы для обратной связи:**
- **GitHub Issues**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/issues (для багов, фич)
- **Telegram**: https://t.me/maslennikovig (для прямого общения)

**Тон**: Супер открыт к конструктивному диалогу. Без эго, просто хочу сделать это лучше.

---

## Промпты для картинок (English)

### 1. Main Hero Image: Systematic Debugging in Action ★★★★★

**Prompt:**
```
A technical diagram showing the systematic debugging workflow in 4 phases. Split the image into 4 vertical sections, each representing a phase:

Phase 1 (Root Cause Analysis): A magnifying glass over a code snippet with a bug highlighted in red, data flow arrows showing where null value originates.

Phase 2 (Pattern Analysis): A network graph showing 3 interconnected files with bug icons, and a "3 fixes = architecture review" rule displayed prominently.

Phase 3 (Hypothesis Generation): A scientist-like figure writing a hypothesis on a whiteboard: "Bug occurs because X → Fix Y → Expect Z", with checkmarks for validation.

Phase 4 (Implementation & Verification): A green progress bar showing quality gates (type-check ✓, build ✓, tests ✓) with a "Success" badge.

Color scheme: Deep blue background, white/cyan code snippets, red for bugs, green for fixes, yellow for warnings.
Style: Modern tech illustration, clean lines, professional, no cartoons.
```

**Rating**: ★★★★★ (HERO image - must include)

---

### 2. Skills vs Agents Architecture ★★★★★

**Prompt:**
```
An architectural diagram showing the relationship between Skills and Agents in Claude Code Orchestrator Kit.

Top section: 5 skill boxes (systematic-debugging, senior-devops, senior-prompt-engineer, webapp-testing, code-reviewer) with "Knowledge Base" labels.

Middle section: Arrows pointing down labeled "references" connecting skills to agents.

Bottom section: 4 agent boxes (bug-fixer, deployment-engineer, meta-agent-v3, code-reviewer) with "Execution Logic" labels.

Each connection should show:
- Skill: Contains methodology, best practices, checklists
- Agent: Uses skill for domain-specific task execution

Color scheme: Skills in purple/violet (knowledge), Agents in blue/cyan (execution), arrows in white.
Background: Dark gradient (navy to black).
Style: Technical architecture diagram, isometric view, professional.
```

**Rating**: ★★★★★ (CORE concept visualization - must include)

---

### 3. Before/After Integration Comparison ★★★★☆

**Prompt:**
```
A split-screen comparison showing bug fixing workflow before and after systematic-debugging integration.

Left side (Before): Chaotic scene with:
- Developer icon with question marks above head
- Multiple "Try fix #1, #2, #3..." labels with red X marks
- Context meter showing 50K tokens (overflowing, red zone)
- Success rate: 50%

Right side (After): Organized scene with:
- Developer icon with lightbulb above head
- Structured 4-phase workflow (1→2→3→4) with green checkmarks
- Context meter showing 10K tokens (healthy, green zone)
- Success rate: 85%

Center: Large arrow pointing from left to right labeled "systematic-debugging integration".

Color scheme: Left side in red/orange (chaos), right side in green/blue (order).
Style: Infographic style, clean icons, data visualization.
```

**Rating**: ★★★★☆ (Great for impact visualization - recommended)

---

## Дополнительные ресурсы

- **Репозиторий**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit
- **Документация по архитектуре**: `docs/Agents Ecosystem/ARCHITECTURE.md`
- **Руководство по оркестрации**: `docs/Agents Ecosystem/AGENT-ORCHESTRATION.md`
- **Отчёт об анализе скиллов**: `docs/reports/skills/new-skills-analysis-2025-12.md`
- **Лицензия**: MIT (полностью бесплатно для коммерческого использования)

---

**Конец статьи**

**Длина:** 23847 символов (без пробелов)
**Целевая платформа:** Habr
**Аудитория:** Технические специалисты, разработчики, архитекторы
**Фокус:** Глубокий технический анализ + практическая интеграция
