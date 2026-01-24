# Материалы для статьи: "Anthropic выпустили Tasks в Claude Code — и вот почему я пока останусь на Beads"

## Метаданные

```yaml
platform: habr
title: "Anthropic выпустили Tasks в Claude Code — и вот почему я пока останусь на Beads"
subtitle: "Новая система управления задачами vs Git-backed трекер: честное сравнение для соло-разработчика"
author: Igor Maslennikov
date: 2026-01-24
tags: [Claude Code, Beads, AI, Task Management, Git, Anthropic, Developer Tools, Productivity]
language: ru
length: ~15000-18000 characters
```

---

## TL;DR (для спойлера в начале)

В январе 2026 Anthropic выпустили **Tasks** — новую систему управления задачами в Claude Code. Это апгрейд старых Todos: теперь задачи персистентны между сессиями, субагенты их видят, есть зависимости между задачами.

**Звучит круто. Но я пока остаюсь на Beads.**

Почему? Одно слово: **Git-backed**. Мои задачи живут в репозитории, версионируются, переносятся между машинами. Tasks от Anthropic хранятся в `~/.claude/` — это глобально, это не в проекте, это не в Git.

**Для кого Tasks подойдут:** Короткие сессии, одна машина, только Claude Code.

**Для кого Beads лучше:** Длинные проекты, несколько машин, история решений, смена AI-агентов.

---

## Персональный контекст

Игорь Масленников, IT с 2013, последние 2 года в AI Dev Team (DNA IT). Развиваю [Claude Code Orchestrator Kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) — open-source набор из 36+ агентов.

У меня 6 проектов на Claude Code. Каждый требует трекинга задач. И я перепробовал всё: markdown-файлы, GitHub Issues, Beads, а теперь — встроенные Tasks.

Эта статья — результат недели экспериментов с новой системой.

---

## Что такое Tasks в Claude Code

### Эволюция: Todos → Tasks

**Старая система Todos (до января 2026):**
- Задачи жили в памяти сессии
- Закрыл терминал — задачи пропали
- Субагенты не видели задачи основного агента
- Нет зависимостей между задачами

**Новая система Tasks (v2.1.16+):**
- Персистентность через `CLAUDE_CODE_TASK_LIST_ID`
- Субагенты видят общий список
- Dependency tracking (задача A блокирует задачу B)
- Инструменты: `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet`

### Как включить

```bash
# Запустить с shared task list
CLAUDE_CODE_TASK_LIST_ID=my-project claude

# Отключить (вернуться к старым Todos)
CLAUDE_CODE_ENABLE_TASKS=false claude
```

### Пример использования

```
> Создай задачу для рефакторинга auth модуля

TaskCreate:
  subject: "Refactor auth module"
  description: "Разделить auth.ts на отдельные файлы..."
  activeForm: "Refactoring auth module"

> Какие задачи сейчас есть?

TaskList:
  1. [pending] Refactor auth module
  2. [in_progress] Fix login bug
  3. [completed] Add logout button
```

### Что реально улучшилось

| Аспект | Старые Todos | Новые Tasks |
|--------|--------------|-------------|
| Персистентность | В памяти | Между сессиями |
| Субагенты | Не видят | Видят через shared ID |
| Зависимости | Нет | `blockedBy`, `blocks` |
| Статусы | 3 | 3 + dependency state |
| Background tasks | Нет | `/tasks`, Ctrl+B |

---

## Что такое Beads

### Философия

Beads — это git-backed issue tracker для AI-агентов от Steve Yegge. Ключевая идея: **задачи — это часть кодовой базы**.

```
project/
├── .beads/
│   ├── issues/
│   │   ├── issue-001.json
│   │   ├── issue-002.json
│   │   └── ...
│   └── db.sqlite
├── src/
└── ...
```

### Как работает

```bash
# Создать задачу
bd create --type=feature --title="Add dark mode"

# Посмотреть текущие
bd list

# Найти в истории
bd search "payment"

# Закрыть с причиной
bd close mc2-7x9 --reason="Implemented in commit abc123"
```

### Ключевые преимущества

1. **Git-backed:** `git commit .beads/` — история всех задач
2. **Portable:** `git clone` — задачи приезжают с проектом
3. **Searchable:** SQLite для быстрых запросов
4. **Cross-agent:** Работает с любым AI (Claude, Cursor, Windsurf)
5. **"Land the plane":** Автогенерация prompt для следующей сессии

---

## Сравнение: Tasks vs Beads

### Таблица возможностей

| Критерий | Claude Code Tasks | Beads |
|----------|-------------------|-------|
| **Персистентность** | `~/.claude/` (глобально) | `.beads/` (в проекте) |
| **Git-backed** | Нет | Да |
| **Версионирование** | Нет | `git log .beads/` |
| **Переносимость** | Через `TASK_LIST_ID` | `git clone` |
| **История поиска** | Нет (или через сессии) | `bd search` |
| **Кросс-агентность** | Только Claude Code | Любой агент |
| **Setup** | Из коробки | Установка `bd` CLI |
| **Зависимости** | Есть | Есть |

### Где хранятся данные

**Claude Code Tasks:**
```
~/.claude/
├── projects/
│   └── coffee/
│       └── sessions/
├── plans/
└── [tasks storage - internal]
```

Нельзя указать произвольный путь. Feature requests на GitHub помечены как **"not planned"**:
- Issue #19986 — `plansDirectory` setting (OPEN)
- Issue #12939 — planStorage setting (NOT PLANNED)

**Beads:**
```
/home/me/code/coffee/
├── .beads/
│   ├── issues/
│   │   └── issue-mc2-7x9.json
│   └── db.sqlite
├── src/
└── .gitignore  # .beads/ НЕ игнорируется!
```

### Реальный сценарий: Смена машины

**С Claude Code Tasks:**
```bash
# Машина 1
CLAUDE_CODE_TASK_LIST_ID=coffee-project claude
# Создал задачи, работал...

# Машина 2
git clone project
cd project
claude
# Задач нет. Нужно знать TASK_LIST_ID
# И даже с ним — задачи на машине 1, не здесь
```

**С Beads:**
```bash
# Машина 1
bd create --title="Refactor auth"
git add .beads/ && git commit -m "Add auth refactoring task"
git push

# Машина 2
git clone project
cd project
bd list
# Задача здесь. Вся история здесь.
```

### Реальный сценарий: Поиск старого решения

**Проблема:** "Как мы решали проблему с rate limiting год назад?"

**С Claude Code Tasks:**
```bash
# Хммм...
# Можно поискать в сессиях?
claude --resume  # Показывает список сессий
# Но как найти нужную среди сотен?
# ctrl+r для поиска... но это поиск по запросам, не по задачам
```

Альтернатива — сторонние инструменты:
- `claude-history` (Rust CLI)
- `cc-conversation-search`

**С Beads:**
```bash
bd search "rate limit"

Results:
- mc2-3a2 [resolved] "Fix rate limiting for API calls"
  Notes: "Implemented token bucket algorithm. See commit abc123."
  Closed: 2025-03-15

- mc2-1b7 [resolved] "Rate limit exceeded on OpenAI API"
  Notes: "Added exponential backoff. Migration: 20250312_add_retry.sql"
  Closed: 2025-03-12
```

**Бонус:** Можно даже `git log .beads/issues/issue-mc2-3a2.json` — увидеть историю изменений задачи.

---

## Почему я остаюсь на Beads

### Причина 1: История решений

Это главное. Когда я решаю новую задачу, я ищу похожие в истории:

```bash
bd search "constraint"
# Нашёл 5 задач про constraint violations
# Каждая с notes: что было, как решили

bd show mc2-4x7
# Подробности: root cause, migration, commit
```

В Tasks этого нет. Задачи уходят в никуда после completion.

### Причина 2: Git = источник правды

Моя философия: **всё важное — в Git**.

- Код — в Git
- Документация — в Git
- Миграции — в Git
- Конфиги — в Git
- **Задачи — тоже должны быть в Git**

Tasks от Anthropic ломают эту модель. Задачи живут отдельно от кода.

### Причина 3: Переносимость

У меня 2 машины: рабочий Mac и домашний Linux. Плюс иногда работаю с iPad через SSH.

С Beads: `git pull` — и все задачи актуальны.

С Tasks: Нужно синхронизировать `~/.claude/` между машинами? Как? rsync? Dropbox?

### Причина 4: Свобода выбора агента

Иногда я использую Cursor для быстрых правок. Или Windsurf для специфических задач.

Beads работает везде — это просто файлы в `.beads/`.

Tasks работают только в Claude Code.

---

## Когда Tasks лучше Beads

### Сценарий 1: Быстрый прототип

```bash
# Сел, написал фичу за 2 часа, закрыл
claude
> Создай задачи для MVP
> [работаю 2 часа]
> Всё сделано, выхожу
```

Не нужна история. Не нужна переносимость. Tasks — ок.

### Сценарий 2: Только Claude Code

Если ты используешь только Claude Code и никогда не переключаешься — Tasks проще. Zero setup.

### Сценарий 3: Команда с shared ID

```bash
# Все в команде используют один ID
CLAUDE_CODE_TASK_LIST_ID=team-project claude
```

Это работает. Хотя Beads + Git — надёжнее.

### Сценарий 4: Короткие сессии

Если типичная сессия — 30 минут, история не накапливается. Tasks достаточно.

---

## Гибридный подход

Можно использовать оба инструмента:

**Tasks — для текущей сессии:**
- Декомпозиция большой задачи
- Трекинг прогресса
- Координация субагентов

**Beads — для истории:**
- Архив решённых проблем
- Поиск по прошлым решениям
- Переносимость между машинами

### Пример workflow

```bash
# 1. Создаю epic в Beads
bd create --type=epic --title="Implement payment system"

# 2. В сессии Claude Code — Tasks для декомпозиции
claude
> Разбей payment system на подзадачи
# Tasks: Setup Stripe, Create webhooks, Add UI...

# 3. После завершения — фиксирую в Beads
bd close mc2-8a1 --reason="Implemented. See commits abc..xyz"
git add .beads/ && git commit -m "Close payment epic"
```

---

## Что я хотел бы видеть в Tasks

### 1. Configurable storage path

```json
// .claude/settings.json
{
  "tasksDirectory": "./.claude/tasks"
}
```

Задачи в проекте, а не глобально.

**Статус:** Feature requests помечены как "not planned".

### 2. Export/Import

```bash
claude tasks export > tasks.json
claude tasks import tasks.json
```

Хотя бы ручная переносимость.

### 3. Search by content

```bash
claude tasks search "payment"
```

Поиск по всем задачам, включая closed.

### 4. History retention

Сейчас completed задачи исчезают (или хранятся где-то недоступно).

Хочу:
```bash
claude tasks history --last-30-days
```

---

## Выводы

### Tasks от Anthropic — это хорошо

- Нативная интеграция
- Zero setup
- Dependency tracking
- Субагенты видят задачи

**Прогресс очевиден.** Todos были бесполезны. Tasks — работают.

### Но для меня Beads лучше

- Git-backed история
- Поиск по прошлым решениям
- Переносимость между машинами
- Свобода выбора инструментов

### Рекомендации

| Ты... | Используй |
|-------|-----------|
| Соло на одной машине, короткие сессии | Tasks |
| Соло на нескольких машинах | Beads |
| Хочешь историю решений | Beads |
| Используешь только Claude Code | Tasks |
| Переключаешься между AI-агентами | Beads |
| Работаешь в команде | Beads + Git |

### Мой выбор

Beads для истории и переносимости.
Tasks для координации субагентов в сессии.

Гибрид работает лучше, чем что-то одно.

---

## Ссылки

**Claude Code:**
- [Claude Code Settings](https://code.claude.com/docs/en/settings)
- [GitHub: Claude Code Releases](https://github.com/anthropics/claude-code/releases)
- [GitHub Issue #19986: plansDirectory](https://github.com/anthropics/claude-code/issues/19986)

**Beads:**
- [Steve Yegge: Introducing Beads](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a)
- [Beads: Memory for Coding Agents](https://paddo.dev/blog/beads-memory-for-coding-agents/)

**Сторонние инструменты для Claude Code:**
- [claude-history (Rust CLI)](https://crates.io/crates/claude-history)
- [cc-conversation-search](https://github.com/akatz-ai/cc-conversation-search)
- [Claude Code Assist (VS Code)](https://marketplace.visualstudio.com/items?itemName=agsoft.claude-history-viewer)

**Мой репозиторий:**
- [Claude Code Orchestrator Kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit)

---

## Автор

**Игорь Масленников**
*AI-агенты, LLM-архитектура, автоматизация разработки.*

Telegram: [@maslennikovigor](https://t.me/maslennikovigor) — бенчмарки, DevOps-лайфхаки, AI-новости
Личный контакт: [@maslennikovig](https://t.me/maslennikovig)
GitHub: [maslennikov-ig](https://github.com/maslennikov-ig)

---

## P.S. для агента-автора

### Главная идея статьи

**Интрига в заголовке:** Anthropic выпустили крутую фичу → но я её не использую → почему?

**Ответ:** Git-backed история важнее нативной интеграции.

### Тон и стиль

- Первое лицо: "я пробовал", "у меня работает"
- Честное сравнение, без хейта на Anthropic
- Конкретные примеры: команды, сценарии
- Практичность: когда что использовать

### Структура

1. **Hook:** Anthropic выпустили Tasks — звучит круто
2. **Twist:** Но я остаюсь на Beads
3. **Контекст:** Что такое Tasks, что такое Beads
4. **Сравнение:** Таблица, сценарии
5. **Мои причины:** 4 конкретных пункта
6. **Fair play:** Когда Tasks лучше
7. **Гибрид:** Можно использовать оба
8. **Wishlist:** Что хотелось бы в Tasks
9. **Выводы:** Рекомендации по выбору

### Избегать

- "В заключение хочется отметить..."
- "Подводя итоги, можно сказать..."
- "Данная технология позволяет..."
- Избыточные эмодзи
- Хейт на Anthropic (они делают хорошую работу)

### Ключевые фразы

- "Git-backed — это не фича, это философия"
- "Задачи — часть кодовой базы"
- "История решений важнее текущего списка"
- "Год назад мы это уже решали — но как найти?"

### Длина

15000-18000 символов. Короче предыдущих статей — тема более узкая.

### Эмоциональный arc

1. Интерес: "О, новая фича!"
2. Разочарование: "Но она не решает мою проблему"
3. Понимание: "Вот почему Beads лучше для меня"
4. Баланс: "Но Tasks тоже хороши для X"
5. Практичность: "Вот как выбрать"

---

## Технические детали

### Проверенные факты

- `CLAUDE_CODE_TASK_LIST_ID` — работает, проверено
- `CLAUDE_CODE_ENABLE_TASKS=false` — возврат к Todos
- Tasks появились в v2.1.16 (январь 2026)
- Feature request на configurable path — "not planned"
- Beads хранит в `.beads/` с SQLite

### Источники

1. [Claude Code Settings Docs](https://code.claude.com/docs/en/settings)
2. [GitHub Issue #19986](https://github.com/anthropics/claude-code/issues/19986)
3. [GitHub Issue #13748](https://github.com/anthropics/claude-code/issues/13748)
4. [Beads: Memory for Coding Agents](https://paddo.dev/blog/beads-memory-for-coding-agents/)
5. [Claude Code's hidden conversation history](https://kentgigger.com/posts/claude-code-conversation-history)
6. [How to Search History in Claude Code](https://claudelog.com/faqs/how-to-search-history-in-claude-code/)

### Команды для демонстрации

```bash
# Claude Code Tasks
CLAUDE_CODE_TASK_LIST_ID=demo claude
# В сессии: TaskCreate, TaskList, TaskUpdate

# Beads
bd create --type=bug --title="Fix auth"
bd list
bd search "auth"
bd close mc2-001 --reason="Fixed"
```
