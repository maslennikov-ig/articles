# Context Tax is Dead: как MCP Tool Search освободил 76K токенов в Claude Code

<spoiler title="TL;DR — что случилось 14 января 2026">

14 января 2026 Anthropic выпустили **MCP Tool Search** — автоматическую оптимизацию загрузки MCP серверов ([читать оригинальную статью](https://www.anthropic.com/engineering/advanced-tool-use)). Вместо того чтобы грузить все 7-8 серверов сразу (~82,000 токенов!), Claude Code теперь умно подгружает только нужные (~5,700 токенов baseline + по требованию).

**Полный breakdown контекста при старте:**
- **ДО:** 143k использовано (72%) → только **57k свободно** для работы
- **ПОСЛЕ:** 67k использовано (34%) → **133k свободно** для работы
- **Экономия:** +76k токенов (+133% к свободному пространству)

**Что я сделал за 2 часа:**
- Обновил 6 проектов на единую MCP конфигурацию
- Убрал все .env файлы, скрипты переключения, direnv-магию
- Хардкодим креденшалы прямо в `.mcp.json` (он в .gitignore)
- Получил **93% экономию на MCP** (82k → 5.7k) + **53% общей экономии** (143k → 67k)

**Результат:** Один файл `.mcp.json`, никаких скриптов, автоматическая оптимизация. Просто работает.

**Репозиторий:** [github.com/igormaslennikov-io/claude-code-orchestrator-kit](https://github.com/igormaslennikov-io/claude-code-orchestrator-kit)

</spoiler>

## Кто я и почему это важно

Игорь Масленников, в IT с 2013 года, последние 2 года развиваю AI Dev Team в DNA IT. У нас 3 человека + 44 AI-агента выполняют работу ~20 специалистов. Стоимость -80%, время разработки с 2-3 месяцев до 1-2 недель.

Развиваю [Claude Code Orchestrator Kit](https://github.com/igormaslennikov-io/claude-code-orchestrator-kit) — open-source набор из 44 агентов, 20+ команд, 30+ скиллов для Claude Code.

**У меня 6 активных проектов на Claude Code:**
- **claude-code-orchestrator-kit** — публичный open-source
- **mc2, coffee, bobabuh** — клиентские проекты
- **repa-maks, Happiness-Bot** — личные pet-проекты

В каждом проекте была своя конфигурация MCP серверов. И везде была **боль**.

## Проблема 1: Контекст жрут MCP серверы

### Как было раньше (до 14 января 2026)

У меня в каждом проекте было 6-8 MCP серверов:

- **context7** — документация (~5,000 токенов)
- **sequential-thinking** — глубокий анализ (~3,000 токенов)
- **supabase** — база данных (~8,000 токенов)
- **playwright** — UI тестирование (~12,000 токенов)
- **shadcn** — UI компоненты (~6,000 токенов)
- **serena** — IDE помощник (~11,000 токенов)
- **github** — работа с GitHub (~26,000 токенов)

**Итого:** ~55,000-70,000 токенов **только на MCP серверы**. Но это не всё!

### Полный breakdown контекста при старте Claude Code

Реальная проблема глубже. MCP серверы — это только **один** компонент бюджета контекста. При старте Claude Code потребляет токены на:

**ДО MCP Tool Search (все MCP серверы загружены):**

| Компонент | Размер | Процент | Описание |
|-----------|--------|---------|----------|
| System prompt | 3.1k | 1.5% | Инструкции для Claude Code, правила поведения |
| System tools | 12.4k | 6.2% | Встроенные инструменты (Read, Write, Edit, Bash, Grep, etc.) |
| Reserved space | 45.0k | 22.5% | Резерв для autocompact + output tokens |
| **MCP tools** | **82.0k** | **41.0%** | Внешние серверы (context7, supabase, playwright, shadcn, etc.) |
| Custom agents | 584 | 0.3% | Агенты из .claude/agents/ |
| Memory files | 312 | 0.2% | CLAUDE.md, CLAUDE.local.md |
| Messages | 8 | 0.0% | История разговора (пустая) |
| **ИТОГО** | **143k** | **72%** | **Использовано из 200k** |
| **Свободно** | **57k** | **28%** | **Для работы** |

**Только 57K свободно из 200K!** (источник: [Scott Spence, Optimising MCP Server Context](https://scottspence.com/posts/optimising-mcp-server-context-usage-in-claude-code))

### Реальный пример (проект coffee)

Запускаю Claude Code:

```bash
$ claude
Starting Claude Code...
Loading MCP servers: context7, sequential-thinking, supabase,
                     playwright, shadcn, serena
MCP Tools loaded: 127 tools (82,000 tokens)
System prompt: 3.1k | System tools: 12.4k | Reserved: 45.0k | MCP: 82.0k
Total context used: 143,000 / 200,000 tokens (72%)
Available for work: 57,000 tokens
```

**Всего 57K из 200K доступно для работы!**

У меня осталось только 57K токенов на весь разговор. После чтения 3-4 файлов (по 10-15K каждый) контекст начинает заканчиваться, и Claude начинает "забывать" начало разговора.

### ПОСЛЕ MCP Tool Search (автоматическая оптимизация)

**С Tool Search (lazy loading MCP серверов):**

| Компонент | Размер | Процент | Описание |
|-----------|--------|---------|----------|
| System prompt | 3.1k | 1.5% | Без изменений |
| System tools | 12.4k | 6.2% | Без изменений |
| Reserved space | 45.0k | 22.5% | Без изменений |
| **MCP tools** | **5.7k** | **2.8%** | **Tool Search baseline (вместо 82k!)** |
| Custom agents | 584 | 0.3% | Без изменений |
| Memory files | 312 | 0.2% | Без изменений |
| Messages | 8 | 0.0% | Без изменений |
| **ИТОГО** | **67k** | **34%** | **Использовано из 200k** |
| **Свободно** | **133k** | **66.5%** | **Для работы** |

**133K свободно из 200K! В 2.3 раза больше!**

### Сравнительная таблица: экономия контекста

| Компонент | До Tool Search | После Tool Search | Экономия |
|-----------|----------------|-------------------|----------|
| System prompt | 3.1k | 3.1k | 0% |
| System tools | 12.4k | 12.4k | 0% |
| Reserved | 45.0k | 45.0k | 0% |
| **MCP tools** | **82.0k** | **5.7k** | **93%** |
| **ИТОГО** | **143k** | **67k** | **53%** |
| **Свободно** | **57k** | **133k** | **+76k токенов** |

**Экономия:** 82k → 5.7k на MCP = **76k дополнительных токенов** для работы (93% экономия на MCP!)

### Проблема усугубляется с агентной архитектурой

Я работаю с архитектурой, где агенты вызывают друг друга. Каждый агент получает **свой контекст**, и все они тратят токены на загрузку:

**ДО Tool Search:**
```
Main agent:        143k использовано, 57k свободно
  ├─ bug-hunter:   143k использовано, 57k свободно
  ├─ bug-fixer:    143k использовано, 57k свободно
  └─ test-runner:  143k использовано, 57k свободно
```

**ПОСЛЕ Tool Search:**
```
Main agent:        67k использовано, 133k свободно
  ├─ bug-hunter:   67k использовано, 133k свободно
  ├─ bug-fixer:    67k использовано, 133k свободно
  └─ test-runner:  67k использовано, 133k свободно
```

**Разница:** Каждый агент получает +76k токенов для работы вместо загрузки MCP!

Я помню, как в середине декабря запустил `/health-bugs` (команда для поиска багов), и на третьем агенте контекст переполнился. Пришлось перезапускать всю цепочку заново. Теперь все 4 агента работают с комфортом. 😤 → ✅

## Проблема 2: Хаос с конфигурациями

У меня было 3 разных подхода к управлению MCP в проектах:

### Вариант 1: Split configs (orchestrator-kit)

```bash
# Было:
mcp/.mcp.base.json            # Только context7 + sequential-thinking
mcp/.mcp.full.json            # Все 7 серверов
mcp/.mcp.frontend.json        # Для frontend задач
mcp/.mcp.supabase-only.json   # Только БД
./switch-mcp.sh               # Скрипт переключения
```

**Проблема:** Забываешь переключить — работаешь не с теми серверами. Или наоборот — грузишь full, когда нужен только context7.

Однажды я весь день дебажил проблему с Supabase, а потом понял, что работал в base конфигурации, где Supabase вообще не подключен. 🤦

### Вариант 2: Хардкоженные креденшалы (mc2, coffee)

```json
{
  "mcpServers": {
    "supabase": {
      "args": ["--project-ref=diqooqbuchsliypgwksu"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

`.mcp.json` в .gitignore — безопасно, но **неудобно**: токены в разных местах, файлы не в git, коллеги не могут быстро поднять проект.

### Вариант 3: Переменные окружения (попытка решить)

```json
{
  "mcpServers": {
    "supabase": {
      "args": ["--project-ref=${SUPABASE_PROJECT_REF}"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}"
      }
    }
  }
}
```

Выглядит чисто. **НО**: Claude Code **НЕ ЧИТАЕТ `.env` файлы**.

Нужно экспортировать вручную:

```bash
export $(cat .env | xargs)
claude
```

Или ставить direnv. Или писать wrapper скрипты. Или добавлять в `~/.bashrc`.

**Геморрой на геморрое.**

Я потратил час на настройку direnv в coffee проекте. Оно не заработало. Оказалось, direnv не подхватывает переменные для GUI приложений на macOS. Пришлось писать `claude.sh` wrapper. Который потом забыл запустить и работал без Supabase. Опять. 😩

## Решение: MCP Tool Search от Anthropic

14 января 2026 Anthropic выпустили статью: [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)

### Ключевая идея

**Tool Search Tool** — это meta-инструмент, который умеет искать нужные инструменты по запросу.

Вместо:
```
Загрузить все 127 инструментов (55,000-70,000 токенов)
```

Работает так:
```
1. Загрузить Tool Search Tool (~8,700 токенов baseline)
2. Claude понял, что ему нужно работать с документацией
3. Tool Search возвращает инструменты context7 (~5,000 токенов)
4. Claude использует context7
```

### Автоматическое включение

**Claude Code делает это автоматически**, если:
- Суммарный размер MCP инструментов >10K токенов
- В конфигурации >5 серверов

Не нужно ничего настраивать. Работает из коробки.

### Результаты из статьи Anthropic

**Тесты на MCP evaluations:**
- Claude Opus 4: улучшение с 49% до 74% (+25%)
- Claude Opus 4.5: улучшение с 79.5% до 88.1% (+8.6%)

**Экономия токенов (данные из статьи Anthropic):**
- Было (5 серверов): ~55,000 токенов
- Было (большие развертывания): до 134,000 токенов
- Стало: ~8,700 токенов baseline + по требованию
- **Экономия: 85-90%**

**Примеры реальных серверов:**
- GitHub: 35 tools (~26,000 tokens)
- Slack: 11 tools (~21,000 tokens)
- Jira: ~17,000 tokens
- Grafana: 5 tools (~3,000 tokens)
- Sentry: 5 tools (~3,000 tokens)
- Splunk: 2 tools (~2,000 tokens)

Когда я прочитал эти цифры, сразу понял — это то, что мне нужно. В тот же день начал миграцию.

## Наша реализация: 6 проектов за 2 часа

Я решил унифицировать все 6 проектов на один подход.

### Целевая архитектура

**Для публичных проектов (orchestrator-kit):**

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-supabase",
               "--project-ref=${SUPABASE_PROJECT_REF}"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}"
      }
    }
  }
}
```

- `.mcp.json` в git (безопасно, используются env vars)
- `.mcp.local.json` в .gitignore (для локальных креденшалов)
- Пользователи добавляют свои креденшалы в .mcp.local.json

**Для личных проектов (mc2, coffee, bobabuh):**

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-supabase",
               "--project-ref=diqooqbuchsliypgwksu"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

- `.mcp.json` в .gitignore (хардкоженные креденшалы)
- Один файл, никаких скриптов, никаких .env

### Почему хардкодим креденшалы?

**Первоначально я хотел использовать .env:**

```bash
# .env
SUPABASE_PROJECT_REF=diqooqbuchsliypgwksu
SUPABASE_ACCESS_TOKEN=sbp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Проблема:** Claude Code НЕ читает .env автоматически.

**Варианты решения:**
1. ❌ Экспортировать вручную: `export $(cat .env | xargs) && claude`
2. ❌ Использовать direnv (нужна установка, настройка shell)
3. ❌ Написать wrapper скрипт `claude.sh` для каждого проекта
4. ✅ **Хардкодить в `.mcp.json` (в .gitignore)**

**Выбрал вариант 4** — максимально простой:
- Один файл
- Никаких зависимостей
- Никаких скриптов
- Работает везде (Linux, macOS, Windows)

## Миграция: конкретные цифры

### Проект 1: orchestrator-kit (open-source)

**Было:**
- 9 файлов в `mcp/` (.mcp.base.json, .mcp.full.json, .mcp.frontend.json...)
- `switch-mcp.sh` скрипт для переключения
- Нужно помнить, какая конфигурация активна

**Стало:**
- Один `.mcp.json` в корне (env vars, в git)
- `.mcp.local.json` в .gitignore
- Удалено: switch-mcp.sh, 8 legacy конфигов

**Экономия контекста:**
- До MCP Tool Search: 143k использовано, 57k свободно
- После MCP Tool Search: 67k использовано, 133k свободно
- **Экономия на MCP: 93% (82k → 5.7k)**
- **Общая экономия: 53% (143k → 67k)**

### Проект 2: mc2 (клиентский)

**Было:**
- 6 серверов
- Хардкоженные креденшалы в .mcp.json
- .mcp.json в .gitignore
- Но креденшалы были вперемешку (часть в args, часть в env)

**Проблема при проверке:**

```bash
$ claude doctor

[Warning] [supabase] Missing environment variables:
  SUPABASE_PROJECT_REF, SUPABASE_ACCESS_TOKEN
```

**Причина:** Креденшалы были в `.env`, но Claude Code их не видел!

**Решение:**

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-supabase",
               "--project-ref=diqooqbuchsliypgwksu"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

**После:**

```bash
$ claude doctor

✅ All MCP servers configured correctly
```

Вот это был момент! 🎉

**Экономия контекста:**
- Было: 143k использовано, 57k свободно
- Стало: 67k использовано, 133k свободно
- **+76k токенов для работы**

### Проект 3: coffee (7 серверов + GitHub)

**Особенность:** У coffee есть GitHub MCP сервер.

**Было:**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

Хардкожено, но работает.

**Стало:** То же самое, но добавил serena (IDE помощник).

**Серверов:** 7 (было 6)

**Экономия контекста:**
- Было: ~150k использовано (7 серверов включая GitHub), ~50k свободно
- Стало: 67k использовано, 133k свободно
- **+83k токенов для работы**

### Проекты 4-6: repa-maks, bobabuh, Happiness-Bot

**Аналогично:** Единая конфигурация, хардкоженные креденшалы, .mcp.json в .gitignore.

### Итого по всем проектам:

| Проект | Серверов | MCP было | MCP стало | Свободно было | Свободно стало | Выигрыш |
|--------|----------|----------|-----------|---------------|----------------|---------|
| orchestrator-kit | 6 | 82.0k | 5.7k | 57k | 133k | +76k |
| mc2 | 6 | 82.0k | 5.7k | 57k | 133k | +76k |
| coffee | 7 | ~90.0k | 5.7k | ~49k | 133k | +84k |
| repa-maks | 5 | ~65.0k | 5.7k | ~74k | 133k | +59k |
| bobabuh | 6 | 82.0k | 5.7k | 57k | 133k | +76k |
| Happiness-Bot | 5 | ~65.0k | 5.7k | ~74k | 133k | +59k |

**Среднее: +72k токенов** дополнительного свободного пространства для работы

## Практический пример: реальная сессия

### До MCP Tool Search

```bash
$ claude
Starting Claude Code...
Loading MCP servers: context7, sequential-thinking, supabase,
                     playwright, shadcn, serena
MCP Tools loaded: 127 tools (82,000 tokens)
System prompt: 3.1k | System tools: 12.4k | Reserved: 45.0k | MCP: 82.0k
Total context used: 143,000 / 200,000 tokens (72%)
Available for work: 57,000 tokens

> Найди документацию по React hooks

[Claude читает 2 файла = 20,000 токенов]
[Свободно: 37,000 / 200,000]

> Создай компонент с useState

[Claude пишет код = 8,000 токенов]
[Свободно: 29,000 / 200,000]

> Теперь добавь useEffect

[Начинает забывать начало разговора после 3-5 запросов]
[Контекст: переполнен через 5-7 запросов с большими файлами]
```

### После MCP Tool Search

```bash
$ claude
Starting Claude Code...
MCP Tool Search enabled (threshold exceeded)
System prompt: 3.1k | System tools: 12.4k | Reserved: 45.0k | MCP: 5.7k
Total context used: 67,000 / 200,000 tokens (34%)
Available for work: 133,000 tokens

> Найди документацию по React hooks

[Tool Search активируется]
[Загружает context7: ~5,000 токенов]
[Свободно: 128,000 / 200,000]

[Claude работает с документацией]
[Свободно: 98,000 / 200,000 после 10 запросов с большими файлами]
```

**Разница:**
- До: **57K свободно** → контекст заканчивается через 3-5 запросов
- После: **133K свободно** → можно работать 20-30 запросов

**На 76K токенов больше пространства для работы! (+133% к свободному контексту)**

Это реальные цифры из моей сессии 15 января в проекте coffee. Я запустил Claude, попросил помочь с рефакторингом компонента, и мы работали 23 запроса подряд без переполнения контекста. Раньше бы переполнился на 4-м. ✅

## Как работает auto-optimization

### Автоматическое определение

Claude Code проверяет:

```javascript
// Псевдокод
if (totalMcpToolsSize > 10000 tokens) {
  enableToolSearch()
} else {
  loadAllTools()
}
```

### On-demand загрузка

1. Claude понял задачу: "Нужно протестировать UI"
2. Tool Search ищет релевантные инструменты: `playwright`
3. Загружает только playwright (~12,000 токенов)
4. Claude работает с playwright
5. Задача закончена → playwright может быть выгружен

### Интеллектуальный кеш

Claude Code кеширует загруженные инструменты в рамках сессии:
- Первый вызов: ~12,000 токенов (playwright)
- Повторные вызовы: 0 токенов (уже загружено)

Это как lazy loading для AI-инструментов. Гениально просто.

## Архитектурные решения

### 1. Публичный vs Приватный проект

**Orchestrator-kit (публичный):**

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-supabase",
               "--project-ref=${SUPABASE_PROJECT_REF}"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}"
      }
    }
  }
}
```

- `.mcp.json` в git
- `.mcp.local.json` в .gitignore
- Пользователи добавляют свои креденшалы в .mcp.local.json

**mc2, coffee (приватные):**

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-supabase",
               "--project-ref=diqooqbuchsliypgwksu"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

- `.mcp.json` в .gitignore
- Хардкоженные креденшалы

### 2. Проверка безопасности

**Перед миграцией я проверил:**

```bash
# Убедился что .mcp.json в .gitignore
$ grep "\.mcp\.json" .gitignore
.mcp.json  # ✅ Найдено

# Убедился что файл не в git истории
$ git log --all --oneline -- .mcp.json
# ✅ Пусто (файл никогда не коммитился)
```

**Для новых проектов:**

```bash
echo ".mcp.json" >> .gitignore
echo ".mcp.local.json" >> .gitignore
```

## Удаление legacy решений

После миграции удалил:

```bash
# 1. Wrapper скрипты
rm claude.sh

# 2. .envrc (direnv)
rm .envrc

# 3. .env (не нужны для MCP)
rm .env

# 4. Legacy конфигурации
rm switch-mcp.sh
mv mcp/.mcp.*.json mcp/legacy/  # На всякий случай

# 5. Документация про .env
# Обновил README.md — убрал инструкции про direnv
```

**Результат:** Чистая структура проекта, без костылей.

Было очень приятно удалить все эти велосипеды. Минус 200 строк документации в README. Минус 5 файлов конфигураций. Минус 50 строк bash-скриптов. 😎

## Статистика: До и После

### Экономия токенов (реальные цифры)

**Сессия разработки (20 запросов к Claude):**

| Этап | До MCP Tool Search | После MCP Tool Search |
|------|--------------------|-----------------------|
| Старт (использовано) | 143,000 токенов (72%) | 67,000 токенов (34%) |
| Старт (свободно) | 57,000 токенов (28%) | 133,000 токенов (66%) |
| После 5 запросов | ~27K свободно | ~103K свободно |
| После 10 запросов | ❌ ~7K свободно (начинает забывать) | ~73K свободно |
| После 20 запросов | ❌ Переполнен (давно) | ~43K свободно |

### Сложность настройки

| Аспект | До | После |
|--------|-----|-------|
| Файлов в проекте | 9-12 | 1 |
| Скриптов | switch-mcp.sh, claude.sh | 0 |
| Зависимостей | direnv / manual export | 0 |
| Время настройки | 10-15 минут | 0 минут |
| Когнитивная нагрузка | Высокая | Нулевая |

### Настроение разработчика

| Ситуация | До | После |
|----------|-----|-------|
| "Забыл переключить конфиг" | 😤 | 😎 |
| "Контекст переполнен через 5 запросов" | 🤯 | 😊 |
| "Нужно настроить новый проект" | 😩 | ✅ |

## Где взять

Все конфигурации — в open-source проекте **Claude Code Orchestrator Kit**:

**Репозиторий:** [github.com/igormaslennikov-io/claude-code-orchestrator-kit](https://github.com/igormaslennikov-io/claude-code-orchestrator-kit)

**Лицензия:** MIT (бесплатно, можно использовать в коммерческих проектах)

**Что есть в репозитории:**
- Унифицированная `.mcp.json` конфигурация
- Документация по MCP Tool Search
- 44 AI-агента
- 20+ slash-команд
- 30+ переиспользуемых скиллов
- Quality gates для CI/CD

### Быстрый старт

```bash
# 1. Клонируем
git clone https://github.com/igormaslennikov-io/claude-code-orchestrator-kit.git
cd claude-code-orchestrator-kit

# 2. Копируем .mcp.json в свой проект
cp .mcp.json /path/to/your/project/

# 3. Добавляем в .gitignore (если приватный)
echo ".mcp.json" >> .gitignore

# 4. Запускаем!
claude
```

**Всё!** MCP Tool Search активируется автоматически.

## Что мы сделали

1. ✅ Мигрировали 6 проектов на единую MCP конфигурацию
2. ✅ Убрали все .env файлы, скрипты, direnv
3. ✅ Хардкодим креденшалы в `.mcp.json` (в .gitignore)
4. ✅ Получили 93% экономию на MCP (82k → 5.7k) + 53% общей экономии (143k → 67k)

**MCP Tool Search — это не просто оптимизация.** Это фундаментальное изменение того, как работает Claude Code:

- **Раньше:** 143k использовано при старте → только 57k свободно → работаем 3-5 запросов
- **Теперь:** 67k использовано при старте → 133k свободно → работаем 20-30 запросов

**+76k токенов (+133%) дополнительного свободного пространства для работы.**

Это реально меняет рабочий процесс. Я могу делать глубокий рефакторинг без страха, что контекст переполнится. Могу запускать длинные цепочки агентов. Могу работать с большими файлами. Просто могу работать. 🚀

## Для кого это

- ✅ Разработчики с >3 MCP серверами
- ✅ Команды с агентными архитектурами (каждый агент = свой контекст)
- ✅ Проекты с длинными диалогами (архитектурные обсуждения, дебаг)
- ✅ Все, кто видел "context overflow" больше 1 раза в день

## Что дальше

Anthropic только начали. В статье упомянули:
- **Programmatic Tool Use** — агенты могут вызывать инструменты программно
- **Tool choice** — явное управление выбором инструментов
- **Caching** — переиспользование контекста между сессиями

**Это будущее AI-ассистированной разработки.** И оно уже здесь.

Я уже тестирую programmatic tool use в новой версии orchestrator-kit. Планирую написать об этом отдельную статью. Следите за обновлениями в Telegram.

---

## Disclaimer: Expected Pushback

Я понимаю, что статья может вызвать критику от разработчиков. "Это просто lazy loading", "Не нужно 7 серверов сразу", "Правильнее использовать environment variables".

Моё мнение: **критика технических решений важна, но эмоциональные реакции — нет.**

**Да, это lazy loading.** Но гениальность в автоматизме — не нужно ничего настраивать.

**Да, можно использовать меньше серверов.** Но зачем ограничивать себя, если система может подгружать их по требованию?

**Да, env variables чище.** Но хардкод креденшалов в .gitignore — проще и работает везде.

Если вы не согласны — окей. Клонируйте репозиторий, попробуйте, потом скажите, где я ошибаюсь. Предпочитаю технические аргументы эмоциональным реакциям.

---

## Контакты и обратная связь

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/aigencypro
Заходите, читайте мысли и статьи. Пишу редко, но когда пишу — стоит прочитать.

**Прямой контакт**: https://t.me/aigencypro
Нужно поговорить? Пишите напрямую. Всегда рад общению.

### 💬 Обратная связь: я максимально открыт

**Хочу услышать:**
- **Критику** — что не так с подходом? Где слабые места?
- **Идеи** — какие фичи добавить? Чего не хватает?
- **Предложения** — как улучшить, оптимизировать, рефакторить систему?
- **Вопросы** — что-то непонятно? Спрашивайте.

**Каналы для фидбека:**
- **GitHub Issues**: https://github.com/igormaslennikov-io/claude-code-orchestrator-kit/issues (для багов, фич)
- **Telegram**: https://t.me/aigencypro (для прямого общения)

**Тон**: Максимально открыт к конструктивному диалогу. Без эго, просто хочу сделать это лучше.

---

## Ссылки

- [Anthropic: Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) — оригинальная статья про MCP Tool Search
- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp) — официальная документация
- [Scott Spence: Optimising MCP Server Context Usage](https://scottspence.com/posts/optimising-mcp-server-context-usage-in-claude-code) — детальный breakdown потребления токенов
- [Claude Code Orchestrator Kit](https://github.com/igormaslennikov-io/claude-code-orchestrator-kit) — наш репозиторий

---

**Игорь Масленников**
*Пишу про AI-агентов, LLM-архитектуру и автоматизацию разработки.*

📢 **Telegram:** [@aigencypro](https://t.me/aigencypro) — бенчмарки, DevOps-лайфхаки, AI-новости
🐙 **GitHub:** [igormaslennikov-io](https://github.com/igormaslennikov-io)
