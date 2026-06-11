---
platform: habr
title: "44 настройки Claude Code, о которых вы не знали, ранжированные от «must have» до «забей»"
author: Igor Maslennikov
date: 2026-01-18
length: ~22000 characters
tags: [Claude Code, AI, DevTools, Configuration, Settings, LLM, MCP, Anthropic]
language: ru
---

# 44 настройки Claude Code, о которых вы не знали, ранжированные от «must have» до «забей»

*Полный справочник settings.json с ранжированием по полезности: от "почему я не знал об этом раньше" до "пригодится раз в год".*

---

<spoiler title="TL;DR — 6 настроек, которые реально меняют workflow">

**Tier 1 (обязательно к настройке):**

```json
{
  "plansDirectory": "./docs/plans",
  "enableAllProjectMcpServers": true,
  "permissions": {
    "allow": ["Bash(npm:*)", "Bash(git:*)", "Edit(src/**)"],
    "deny": ["Read(.env*)"]
  },
  "env": {
    "ENABLE_TOOL_SEARCH": "auto:5"
  }
}
```

**Что это даёт:**
- Планы сохраняются в проекте, а не в `~/.claude/plans` (можно коммитить!)
- MCP серверы включаются автоматически без запросов
- npm/git/редактирование src — без подтверждений
- .env файлы защищены от чтения
- MCP инструменты грузятся лениво → экономия 90% токенов

**Актуально для:** Claude Code 2.1.12 (январь 2026)

</spoiler>

---

## Кто я и почему это важно

Игорь Масленников, в IT с 2013 года, последние 2 года развиваю AI Dev Team в DNA IT. У нас 54 специалиста + 44 AI-агента — команда работает в разы эффективнее за счёт AI-автоматизации. Стоимость -80%, время разработки с 2-3 месяцев до 1-2 недель.

Развиваю [Claude Code Orchestrator Kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) — open-source набор из 44 агентов, 20+ команд, 30+ скиллов для Claude Code.

**Проблема:** За 2 года работы с Claude Code я понял, что большинство разработчиков используют его "из коробки". Не настраивают permissions, не знают про hooks, не используют MCP Tool Search. А потом жалуются на "тупой AI, который постоянно спрашивает подтверждения".

**Решение:** Я собрал все настройки из официальной документации, CHANGELOG и своего опыта в один структурированный справочник. **С ранжированием по полезности** — чтобы вы знали, что настроить в первую очередь.

---

## Как устроен settings.json

### Приоритет настроек

Claude Code читает настройки из нескольких файлов. Если одна и та же настройка указана в разных местах, побеждает файл с более высоким приоритетом:

| Приоритет | Scope | Файл | Когда использовать |
|-----------|-------|------|-------------------|
| 🔴 Высший | Managed (IT) | `/etc/claude-code/managed-settings.json` | Корпоративные политики |
| 🟠 Высокий | Local (личный) | `.claude/settings.local.json` | Персональные настройки (не в git) |
| 🟡 Средний | Project (команда) | `.claude/settings.json` | Настройки проекта (в git) |
| 🟢 Низший | User (глобальный) | `~/.claude/settings.json` | Дефолты для всех проектов |

**Типичный паттерн:**
- `.claude/settings.json` — в git, общие для команды
- `.claude/settings.local.json` — в .gitignore, персональные

---

## Tier 1: Критически полезные

Эти настройки **реально меняют рабочий процесс**. Если вы их не используете — вы теряете время.

### plansDirectory

```json
{ "plansDirectory": "./docs/plans" }
```

**Что делает:** Куда сохраняются планы при использовании Plan Mode (`Shift+Tab` → Plan).

**По умолчанию:** `~/.claude/plans` — файлы теряются в домашней директории, нельзя закоммитить.

**Почему важно:** Планы — это артефакты работы. Я использую их для:
- Code review (коллеги видят, что Claude планировал сделать)
- Документации (планы становятся частью ADR)
- Отката (если что-то пошло не так, смотрю план и понимаю логику)

**Моя конфигурация:**
```json
{ "plansDirectory": "./docs/plans" }
```

Теперь все планы в git, рядом с кодом.

---

### env.ENABLE_TOOL_SEARCH

```json
{
  "env": {
    "ENABLE_TOOL_SEARCH": "auto:5"
  }
}
```

**Что делает:** Активирует ленивую загрузку MCP инструментов вместо загрузки всех сразу.

**Почему важно:** У меня 6 MCP серверов (~82,000 токенов). Без Tool Search они **все** грузятся при старте. С Tool Search — только ~5,700 токенов baseline + по требованию.

| Значение | Поведение |
|----------|-----------|
| `auto` | Активируется при >10% контекста заняты MCP |
| `auto:N` | Активируется при >N% контекста |
| `true` | Всегда включен |
| `false` | Выключен |

**Результат:**
```
ДО:  143k использовано → 57k свободно
ПОСЛЕ: 67k использовано → 133k свободно
Экономия: +76k токенов (+133% к рабочему пространству)
```

Подробнее писал в [статье про MCP Tool Search](https://habr.com/ru/articles/XXX/).

---

### permissions.allow / deny

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run:*)",
      "Bash(pnpm:*)",
      "Bash(git:*)",
      "Edit(src/**)"
    ],
    "deny": [
      "Read(.env*)",
      "Bash(rm -rf:*)"
    ]
  }
}
```

**Что делает:** Автоматически разрешает (allow) или запрещает (deny) операции без запроса.

**Почему важно:** Без этого Claude **каждый раз** спрашивает:

```
Claude wants to run: npm run build
Allow? [Y/n]
```

Умножьте на 50 раз в день — и вы поймёте, зачем нужен allow list.

**Паттерны:**
- `Bash(npm:*)` — любые npm команды
- `Bash(git:*)` — любые git команды
- `Edit(src/**)` — редактирование файлов в src/
- `Read(.env*)` — чтение .env файлов (запретить!)
- `mcp__supabase__*` — все инструменты supabase MCP (v2.1.x)

**Моя конфигурация:**
```json
{
  "permissions": {
    "allow": [
      "Bash(pnpm:*)",
      "Bash(npm:*)",
      "Bash(git:*)",
      "Bash(bd:*)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/credentials*)",
      "Bash(rm -rf:*)"
    ]
  }
}
```

`bd` — это мой алиас для скриптов автоматизации.

---

### enableAllProjectMcpServers

```json
{ "enableAllProjectMcpServers": true }
```

**Что делает:** Автоматически разрешает все MCP серверы из `.mcp.json`.

**По умолчанию:** Claude спрашивает разрешение на каждый сервер при старте:

```
Enable MCP server 'supabase'? [Y/n]
Enable MCP server 'playwright'? [Y/n]
Enable MCP server 'context7'? [Y/n]
...
```

**С enableAllProjectMcpServers:**

```
Loading MCP servers: context7, supabase, playwright, shadcn ✓
```

**Важно:** Включайте только если доверяете MCP серверам в проекте. Для open-source проектов с чужими .mcp.json — лучше оставить false.

---

### model

```json
{ "model": "claude-sonnet-4-20250514" }
```

**Что делает:** Переопределяет модель по умолчанию.

**Когда использовать:**
- Фиксируете версию модели для воспроизводимости
- Используете Sonnet для рутинных задач (дешевле)
- Тестируете новую модель

**Доступные модели (январь 2026):**
- `claude-opus-4-5-20251101` — самая мощная
- `claude-sonnet-4-20250514` — баланс скорость/качество
- `claude-haiku-4-20250514` — быстрая и дешёвая

---

### alwaysThinkingEnabled

```json
{ "alwaysThinkingEnabled": true }
```

**Что делает:** Включает Extended Thinking по умолчанию для всех сессий.

**Что такое Extended Thinking:** Claude "думает вслух" перед ответом. Занимает больше токенов, но улучшает качество сложных задач (архитектура, дебаг, рефакторинг).

**Когда включать:**
- Работаете над сложной архитектурой
- Отлаживаете неочевидные баги
- Нужен глубокий анализ кода

**Когда НЕ включать:**
- Рутинные задачи (создание файлов, простые фиксы)
- Ограниченный бюджет токенов

---

## Tier 2: Очень полезные

Эти настройки не критичны, но **заметно улучшают** опыт работы.

### language

```json
{ "language": "russian" }
```

**Что делает:** Claude отвечает на указанном языке.

**Почему важно:** Без этого Claude отвечает на английском. Приходится писать "отвечай на русском" в каждом промпте.

**Поддерживаемые языки:** Практически любой. Claude определяет по названию: `russian`, `german`, `spanish`, `chinese`, etc.

---

### autoUpdatesChannel

```json
{ "autoUpdatesChannel": "stable" }
```

**Что делает:** Выбирает канал обновлений.

| Значение | Поведение |
|----------|-----------|
| `latest` | Последняя версия (default) — новые фичи, возможные баги |
| `stable` | Версия недельной давности — проверено, стабильно |

**Моя рекомендация:** `stable` для продакшн проектов, `latest` для экспериментов.

---

### permissions.defaultMode

```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

**Что делает:** Режим разрешений при старте сессии.

| Значение | Поведение |
|----------|-----------|
| `default` | Спрашивает разрешения на всё |
| `acceptEdits` | Автоматически принимает редактирования файлов |
| `bypassPermissions` | Пропускает ВСЕ запросы (опасно!) |

**`acceptEdits`** — хороший баланс: Claude может редактировать код без подтверждений, но bash команды всё ещё требуют approval.

---

### permissions.additionalDirectories

```json
{
  "permissions": {
    "additionalDirectories": ["/home/me/shared-libs", "/home/me/docs"]
  }
}
```

**Что делает:** Даёт Claude доступ к директориям вне текущего проекта.

**Когда нужно:**
- Монорепозиторий с shared библиотеками
- Документация в отдельной папке
- Конфиги в ~/.config/

---

### hooks

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "npm run prepare" }]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "npm run cleanup" }]
      }
    ]
  }
}
```

**Что делает:** Выполняет команды на события Claude Code.

**Доступные события:**
| Событие | Когда срабатывает |
|---------|-------------------|
| `SessionStart` | Старт сессии |
| `SessionEnd` | Конец сессии |
| `Stop` / `SubagentStop` | Остановка основного агента / субагента |
| `PreToolUse` / `PostToolUse` | До/после использования инструмента |
| `PreCompact` | Перед компактификацией контекста |
| `UserPromptSubmit` | Отправка промпта пользователем |
| `Setup` | При `claude --init`, `--init-only`, `--maintenance` (v2.1.x) |

**Пример: Прогрев кэша при старте**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "bd prime", "once": true }]
      }
    ]
  }
}
```

`once: true` — выполнить только один раз за сессию (v2.1.x).

---

### enabledMcpjsonServers

```json
{
  "enabledMcpjsonServers": ["context7", "supabase", "playwright"]
}
```

**Что делает:** Выборочно включает только указанные MCP серверы из `.mcp.json`.

**Когда использовать:** В `.mcp.json` 10 серверов, но для текущей задачи нужны только 3.

**Альтернатива:** Использовать `enableAllProjectMcpServers: true` + полагаться на Tool Search (ленивая загрузка).

---

## Tier 3: Полезные

Настройки для **специфических сценариев**. Не обязательны, но пригодятся.

### attribution.commit / attribution.pr

```json
{
  "attribution": {
    "commit": "Co-Authored-By: Claude <noreply@anthropic.com>",
    "pr": ""
  }
}
```

**Что делает:** Настраивает атрибуцию в коммитах и PR.

**Пустая строка = отключить:**
```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

Я оставляю co-authored-by — честность перед коллегами.

---

### cleanupPeriodDays

```json
{ "cleanupPeriodDays": 7 }
```

**Что делает:** Через сколько дней удалять неактивные сессии.

**По умолчанию:** 30 дней. Если работаете интенсивно — можно уменьшить до 7-14.

---

### sandbox

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  }
}
```

**Что делает:** Песочница для bash команд (macOS/Linux).

**`autoAllowBashIfSandboxed: true`** — если песочница включена, bash команды выполняются без подтверждений. Логика: песочница ограничивает ущерб, поэтому можно доверять.

---

### env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE

```json
{
  "env": {
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "80"
  }
}
```

**Что делает:** При каком % заполнения контекста запускать auto-compaction.

**По умолчанию:** ~90%. При 80% — compaction запустится раньше, потеряете меньше контекста при переполнении.

---

### env.MAX_THINKING_TOKENS

```json
{
  "env": {
    "MAX_THINKING_TOKENS": "50000"
  }
}
```

**Что делает:** Бюджет токенов для Extended Thinking.

**Когда увеличивать:** Сложные задачи требуют больше "размышлений". Но помните — это стоит денег.

---

### env.CLAUDE_CODE_MAX_OUTPUT_TOKENS

```json
{
  "env": {
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "32000"
  }
}
```

**Что делает:** Максимум токенов на один ответ Claude.

**По умолчанию:** Зависит от модели. Максимум: 64000.

**Когда увеличивать:** Генерация больших файлов, длинных документов.

---

### env.CLAUDE_CODE_SUBAGENT_MODEL

```json
{
  "env": {
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-4-20250514"
  }
}
```

**Что делает:** Модель для субагентов (Task tool).

**Паттерн:** Основной агент на Opus (качество), субагенты на Sonnet (экономия).

---

## Tier 4: Ситуационно полезные

Эти настройки нужны **в редких случаях**, но когда нужны — очень нужны.

### respectGitignore

```json
{ "respectGitignore": false }
```

**Что делает:** Учитывать ли `.gitignore` в `@` file picker.

**По умолчанию:** true. Файлы из .gitignore не показываются в автокомплите.

**Когда отключать:** Нужен доступ к файлам в .gitignore (логи, кэш, временные файлы).

---

### Визуальные настройки

```json
{
  "showTurnDuration": false,
  "spinnerTipsEnabled": false,
  "terminalProgressBarEnabled": false
}
```

| Настройка | По умолчанию | Что отключает |
|-----------|--------------|---------------|
| `showTurnDuration` | true | "Cooked for 1m 6s" |
| `spinnerTipsEnabled` | true | Tips в спиннере |
| `terminalProgressBarEnabled` | true | Progress bar |

Отключаю `spinnerTipsEnabled` — раздражает.

---

### statusLine

```json
{
  "statusLine": {
    "type": "command",
    "command": "/path/to/status-script.sh"
  }
}
```

**Что делает:** Кастомная строка статуса.

**Пример скрипта:**
```bash
#!/bin/bash
echo "$(git branch --show-current) | $(date +%H:%M)"
```

---

### Таймауты

```json
{
  "env": {
    "BASH_DEFAULT_TIMEOUT_MS": "300000",
    "BASH_MAX_TIMEOUT_MS": "600000",
    "MCP_TIMEOUT": "60000",
    "MCP_TOOL_TIMEOUT": "120000"
  }
}
```

| Переменная | По умолчанию | Что контролирует |
|------------|--------------|------------------|
| `BASH_DEFAULT_TIMEOUT_MS` | 120000 (2 мин) | Таймаут bash по умолчанию |
| `BASH_MAX_TIMEOUT_MS` | 600000 (10 мин) | Максимальный таймаут bash |
| `MCP_TIMEOUT` | 30000 | Таймаут подключения к MCP |
| `MCP_TOOL_TIMEOUT` | 60000 | Таймаут выполнения MCP tool |

**Когда увеличивать:**
- Долгие сборки (npm run build на большом проекте)
- Тяжёлые MCP операции (playwright тесты)

---

### env.MAX_MCP_OUTPUT_TOKENS

```json
{
  "env": {
    "MAX_MCP_OUTPUT_TOKENS": "50000"
  }
}
```

**По умолчанию:** 25000. Максимум токенов в ответах MCP.

**Когда увеличивать:** MCP возвращает большие ответы (playwright screenshots, длинные логи).

---

## Tier 5: Enterprise / Специфические

Для **корпоративных сценариев** или очень специфических задач.

### API и аутентификация

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-...",
    "CLAUDE_CODE_USE_BEDROCK": "1",
    "CLAUDE_CODE_USE_VERTEX": "1"
  }
}
```

**Когда нужно:**
- Собственный API ключ (вместо подписки)
- AWS Bedrock / Google Vertex AI провайдеры

---

### apiKeyHelper

```json
{ "apiKeyHelper": "/path/to/get-api-key.sh" }
```

**Что делает:** Скрипт для динамического получения API ключа.

**Пример:** Интеграция с AWS Secrets Manager, HashiCorp Vault.

---

### Proxy настройки

```json
{
  "env": {
    "HTTP_PROXY": "http://proxy:8080",
    "HTTPS_PROXY": "http://proxy:8080",
    "NO_PROXY": "localhost,127.0.0.1"
  }
}
```

Для корпоративных сетей с прокси.

---

### companyAnnouncements

```json
{
  "companyAnnouncements": [
    "Не забудьте обновить документацию!",
    "Код-ревью обязателен для всех PR"
  ]
}
```

**Что делает:** Показывает случайное объявление при старте сессии.

**Для:** IT-отделов, которые хотят напоминать разработчикам о политиках.

---

### Отключение функций

```json
{
  "env": {
    "DISABLE_TELEMETRY": "1",
    "DISABLE_ERROR_REPORTING": "1",
    "DISABLE_AUTOUPDATER": "1",
    "DISABLE_COST_WARNINGS": "1",
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
    "DISABLE_PROMPT_CACHING": "1"
  }
}
```

| Переменная | Что отключает |
|------------|---------------|
| `DISABLE_TELEMETRY` | Телеметрия |
| `DISABLE_ERROR_REPORTING` | Отправка ошибок |
| `DISABLE_AUTOUPDATER` | Автообновления |
| `DISABLE_COST_WARNINGS` | Предупреждения о стоимости |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS` | Неосновные вызовы API |
| `DISABLE_PROMPT_CACHING` | Кэширование промптов |

**Для:** Параноиков, airgapped сред, экономии трафика.

---

### env.CLAUDE_CODE_HIDE_ACCOUNT_INFO

```json
{
  "env": {
    "CLAUDE_CODE_HIDE_ACCOUNT_INFO": "1"
  }
}
```

**Что делает:** Скрывает email и организацию в UI.

**Для:** Стримеров, демонстраций, скриншотов.

---

## Новое в v2.1.x (январь 2026)

### Hook event: Setup

```json
{
  "hooks": {
    "Setup": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "npm install" }]
      }
    ]
  }
}
```

Запускается при `claude --init`, `--init-only`, `--maintenance`.

### Hooks: once: true

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "bd prime", "once": true }]
      }
    ]
  }
}
```

Выполнить хук **только один раз** за сессию.

### Wildcard MCP permissions

```json
{
  "permissions": {
    "allow": ["mcp__supabase__*"],
    "deny": ["mcp__filesystem__*"]
  }
}
```

Разрешить/запретить все инструменты MCP сервера одной строкой.

### CLI: --tools

```bash
claude --tools Read,Write,Bash
```

Ограничить доступные инструменты в сессии.

---

## Полный пример settings.json

```json
# Docs L1/L2: query @neuledge/context MCP first with package@version from the lockfile and domain/API keywords.
# Context7 calls below are L2 fallback only for L1 miss/stale/insufficient.
{
  "plansDirectory": "./docs/plans",
  "language": "russian",
  "alwaysThinkingEnabled": false,
  "enableAllProjectMcpServers": true,
  "autoUpdatesChannel": "stable",
  "cleanupPeriodDays": 14,

  "permissions": {
    "allow": [
      "Bash(pnpm:*)",
      "Bash(npm:*)",
      "Bash(git:*)",
      "Bash(bd:*)",
      "mcp__context7__*"
    ],
    "deny": [
      "Read(.env*)",
      "Read(**/credentials*)",
      "Bash(rm -rf:*)"
    ],
    "defaultMode": "acceptEdits"
  },

  "attribution": {
    "commit": "Co-Authored-By: Claude <noreply@anthropic.com>",
    "pr": ""
  },

  "env": {
    "ENABLE_TOOL_SEARCH": "auto:5",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "85",
    "MAX_MCP_OUTPUT_TOKENS": "30000"
  },

  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "bd prime", "once": true }]
      }
    ]
  }
}
```

---

## Статистика: До и После

| Метрика | Без настройки | С настройкой |
|---------|---------------|--------------|
| Запросов "Allow?" за сессию | ~50 | 0-5 |
| Контекст при старте | 143K (72%) | 67K (34%) |
| Планы в git | ❌ | ✅ |
| MCP без вопросов | ❌ | ✅ |
| .env защищены | ❌ | ✅ |

---

## Где взять

Все конфигурации — в open-source проекте **Claude Code Orchestrator Kit**:

**Репозиторий:** [github.com/maslennikov-ig/claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit)

**Лицензия:** MIT (бесплатно, можно использовать в коммерческих проектах)

---

## Disclaimer: Expected Pushback

Я понимаю, что кто-то скажет: "Это просто пересказ документации" или "Зачем это, если есть официальные доки".

Моё мнение:

1. **Официальная документация — это справочник**, а не руководство к действию. Она говорит "что есть", а не "что важно".

2. **Ранжирование по полезности — это моя экспертиза** после 2 лет работы с Claude Code и 44 агентов в продакшене.

3. **Примеры из практики — это то, чего не хватает** в официальных доках.

Если не согласны — окей. Попробуйте настройки, потом скажите, где я ошибаюсь.

---

## Контакты

**Автор:** Игорь Масленников
*Пишу про AI-агентов, LLM-архитектуру и автоматизацию разработки.*

📢 **Мой канал в Telegram:** [@maslennikovigor](https://t.me/maslennikovigor) — там я публикую разборы AI-инструментов и DevOps-лайфхаки.

💬 **Личный контакт:** [@maslennikovig](https://t.me/maslennikovig) — для вопросов, идей и обратной связи.

🔧 **GitHub:** [claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) — open-source инструменты для AI-автоматизации.

Если попробуете настройки — напишите, что сработало, что нет. Буду рад фидбеку.

---

## Ссылки

- [Официальная документация Claude Code Settings](https://docs.anthropic.com/en/docs/claude-code/settings)
- [MCP конфигурация](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [GitHub CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)

---

**А какие настройки используете вы?** Делитесь в комментариях — интересно узнать, что ещё можно оптимизировать.
