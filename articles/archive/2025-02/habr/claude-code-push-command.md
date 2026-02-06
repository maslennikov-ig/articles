---
platform: habr
title: "/push — как мы автоматизировали релизы в Claude Code и забыли про ручные changelog'и"
author: Igor Maslennikov
date: 2025-12-20
length: ~20000 characters
tags: [Claude Code, DevOps, Git, Release Automation, Bash, Conventional Commits, Changelog, AI, LLM]
language: ru
---

# /push — как мы автоматизировали релизы в Claude Code и забыли про ручные changelog'и

*Одна команда — и Claude Code сам анализирует коммиты, определяет тип релиза, генерирует changelog, обновляет версии и пушит в GitHub. Разбираем внутрянку 1000-строчного bash-скрипта.*

---

<spoiler title="TL;DR для нетерпеливых">

**Команда `/push`** — это slash-команда для Claude Code, которая:
- Анализирует все коммиты с последнего релиза
- Автоматически определяет тип версии (patch/minor/major) по conventional commits
- Генерирует CHANGELOG.md в формате Keep a Changelog
- Обновляет все package.json в монорепозитории
- Создаёт git tag и пушит в remote
- Откатывает все изменения при ошибке

**Репозиторий:** [github.com/maslennikov-ig/claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) (MIT, бесплатно)

</spoiler>

---

## Проблема: Релизы — это боль

Каждый разработчик знает этот ритуал:

1. Посмотреть `git log`, чтобы понять, что изменилось
2. Решить, какой номер версии поставить
3. Обновить `package.json` (а если монорепо — то все 5 штук)
4. Написать CHANGELOG (и забыть половину фич)
5. Сделать коммит "chore: bump version"
6. Создать тег
7. Запушить
8. Понять, что забыл добавить важный фикс в changelog
9. Сделать `--amend`, удалить тег, пересоздать тег...
10. 🤯

В нашем проекте [Claude Code Orchestrator Kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) релизы случаются 2-3 раза в день. После 50-го "chore: bump version" я решил, что хватит.

---

## Решение: Одна команда — `/push`

Теперь мой релиз выглядит так:

```bash
/push patch
```

И Claude Code делает всё сам:

```
╔═══════════════════════════════════════════════════════════╗
║                    Release Automation                     ║
╚═══════════════════════════════════════════════════════════╝

ℹ️  Running pre-flight checks...

✅ On branch: main
✅ Remote configured
✅ Node.js available
✅ Current version: 1.3.4
✅ Last tag: v1.3.4
✅ Found 3 commits since last release

ℹ️  Analyzing commits since v1.3.4...

ℹ️  Commit summary:
  ✨ 1 features
  🐛 1 bug fixes
  📝 1 other changes

═══════════════════════════════════════════════════════════
                    RELEASE PREVIEW
═══════════════════════════════════════════════════════════

📌 Version: 1.3.4 → 1.3.5 (PATCH)
   Reason: Manually specified

📦 Package Updates:
  ✓ package.json

📄 CHANGELOG.md Entry:
───────────────────────────────────────────────────────────
## [1.3.5] - 2025-12-20

### Added
- **agents**: add new security-scanner worker (abc1234)

### Fixed
- **api**: fix authentication timeout issue (def5678)
───────────────────────────────────────────────────────────

✅ Released v1.3.5
✅ Tag: v1.3.5
✅ Pushed to origin/main
```

**Весь процесс занимает 3-5 секунд.**

---

## Как это работает под капотом

### Архитектура

Команда `/push` — это [slash-команда Claude Code](https://docs.anthropic.com/en/docs/claude-code/tutorials#slash-commands). Она определена в файле `.claude/commands/push.md`:

```markdown
---
description: Automated release management with version bumping and changelog updates
argument-hint: [patch|minor|major]
---

Execute the release automation script with auto-confirmation for Claude Code.

**Features:**
- Auto-syncs package.json versions with latest git tag
- Analyzes commits since last release
- Auto-detects version bump type from conventional commits
- Generates CHANGELOG entries
- Updates all package.json files
- Creates git tag and pushes to GitHub
- Full rollback support on errors
```

Это обёртка над bash-скриптом `release.sh` на 1050+ строк. Разберём ключевые части.

---

## Фича 1: Auto-commit перед релизом

**Проблема:** Вы поработали, накопили изменения, хотите релизнуть. Но сначала надо всё закоммитить. А это отдельная история с придумыванием сообщения.

**Решение:** Скрипт сам коммитит незакоммиченные изменения с умным определением типа:

```bash
# Detect commit type based on changed files
local commit_type="chore"
local commit_scope=""

# Get file changes with status
local file_status=$(git diff --cached --name-status)

# Priority-based detection
local new_agents=$(echo "$file_status" | grep "^A.*\.claude/agents/.*\.md$" | wc -l)
local new_skills=$(echo "$file_status" | grep "^A.*\.claude/skills/.*/SKILL\.md$" | wc -l)
local new_commands=$(echo "$file_status" | grep "^A.*\.claude/commands/.*\.md$" | wc -l)

# New agents = feat(agents)
if [ "$new_agents" -gt 0 ]; then
    commit_type="feat"
    commit_scope="agents"
    local agent_name=$(basename "$agent_file" .md)
    commit_desc="add ${agent_name} agent"
fi
```

**Как это работает:**
1. Скрипт детектит, какие файлы изменились
2. По паттернам определяет тип коммита:
   - Новые агенты → `feat(agents): add security-scanner agent`
   - Новые скиллы → `feat(skills): add validate-plan skill`
   - Изменения скриптов → `chore(scripts): update automation scripts`
   - Документация → `docs: update documentation`
3. Автоматически стейджит и коммитит

Результат:
```
ℹ️  Uncommitted changes detected. Auto-committing before release...
✅ Changes committed (15 files)
ℹ️  Commit type: feat(agents): add 3 new agents (bug-hunter, ...)
```

---

## Фича 2: Синхронизация версий с Git Tags

**Проблема:** В монорепозитории легко получить рассинхрон: `package.json` говорит `1.3.2`, а последний тег — `v1.3.4`. Это приводит к конфликтам при следующем релизе.

**Решение:** Скрипт сверяет версию в `package.json` с последним тегом и автоматически синхронизирует:

```bash
# Get last git tag
LAST_TAG=$(git tag --sort=-version:refname | safe_first || echo "")

# Sync package.json version with git tag if needed
TAG_VERSION="${LAST_TAG#v}" # Remove 'v' prefix
if [ "$CURRENT_VERSION" != "$TAG_VERSION" ]; then
    log_warning "Version mismatch: package.json ($CURRENT_VERSION) != tag ($TAG_VERSION)"
    log_info "Syncing package.json versions to $TAG_VERSION..."

    # Find and update all package.json files
    find "$PROJECT_ROOT" -name "package.json" -not -path "*/node_modules/*" -print0 | \
    while IFS= read -r -d '' pkg_file; do
        sed -i "s/\"version\": \"[^\"]*\"/\"version\": \"$TAG_VERSION\"/" "$pkg_file"
    done

    log_success "Synced all package.json files to version $TAG_VERSION"
fi
```

Это спасает от ситуации "у меня локально 1.3.2, а на remote уже 1.3.4".

---

## Фича 3: Умный анализ Conventional Commits

**Проблема:** Определить тип релиза — это не просто "есть фича или нет". Надо учитывать breaking changes, security fixes, deprecations.

**Решение:** Скрипт парсит все коммиты и категоризирует их по типам:

```bash
# Supported conventional commit types
local breaking_pattern='^[a-z]+(\([^)]+\))?!:'     # type!: → major
local feat_pattern='^feat(\([^)]+\))?:'            # feat: → minor
local fix_pattern='^fix(\([^)]+\))?:'              # fix: → patch
local security_pattern='^security(\([^)]+\))?:'    # security: → patch (high priority!)
local deprecate_pattern='^deprecate(\([^)]+\))?:'  # deprecate: → shown in changelog
local remove_pattern='^remove(\([^)]+\))?:'        # remove: → shown in changelog

for commit in "${ALL_COMMITS[@]}"; do
    local message=$(echo "$commit" | cut -d' ' -f2-)

    if [[ "$message" =~ $breaking_pattern ]]; then
        BREAKING_CHANGES+=("$commit")
    elif [[ "$message" =~ $security_pattern ]]; then
        SECURITY_FIXES+=("$commit")
    elif [[ "$message" =~ $feat_pattern ]]; then
        FEATURES+=("$commit")
    # ... и так далее
    fi
done
```

**Автоопределение версии:**

```bash
detect_version_bump() {
    if [ ${#BREAKING_CHANGES[@]} -gt 0 ]; then
        BUMP_TYPE="major"  # Breaking changes → major
    elif [ ${#FEATURES[@]} -gt 0 ]; then
        BUMP_TYPE="minor"  # New features → minor
    elif [ ${#SECURITY_FIXES[@]} -gt 0 ]; then
        BUMP_TYPE="patch"  # Security fixes → patch
    elif [ ${#FIXES[@]} -gt 0 ]; then
        BUMP_TYPE="patch"  # Bug fixes → patch
    else
        BUMP_TYPE="patch"  # Default
    fi
}
```

Результат:
```
ℹ️  Commit summary:
  🔥 1 breaking changes
  🔒 2 security fixes
  ✨ 5 features
  🐛 3 bug fixes
  ⚠️  1 deprecations
  ♻️  2 refactors

✅ Auto-detected version bump: major (Found 1 breaking change(s))
```

---

## Фича 4: Генерация CHANGELOG по Keep a Changelog

**Проблема:** Писать changelog вручную — это:
1. Скучно
2. Легко что-то забыть
3. Нет единого формата

**Решение:** Скрипт генерирует changelog по стандарту [Keep a Changelog](https://keepachangelog.com/):

```bash
generate_changelog_entry() {
    local version="$1"
    local date="$2"

    echo "## [$version] - $date"
    echo ""

    # Security section FIRST (highest priority!)
    if [ ${#SECURITY_FIXES[@]} -gt 0 ]; then
        echo "### Security"
        for commit in "${SECURITY_FIXES[@]}"; do
            format_changelog_line "$commit"
        done
    fi

    # Added section (features)
    if [ ${#FEATURES[@]} -gt 0 ]; then
        echo "### Added"
        for commit in "${FEATURES[@]}"; do
            format_changelog_line "$commit"
        done
    fi

    # Changed section (breaking, refactor, perf)
    if [ ${#BREAKING_CHANGES[@]} -gt 0 ]; then
        echo "### Changed"
        for commit in "${BREAKING_CHANGES[@]}"; do
            format_changelog_line "$commit" "⚠️ BREAKING: "
        done
    fi

    # ... Deprecated, Removed, Fixed, Other
}
```

**Форматирование строк:**

```bash
format_changelog_line() {
    local commit="$1"
    local hash=$(echo "$commit" | awk '{print $1}')
    local message=$(echo "$commit" | cut -d' ' -f2-)

    # Extract scope: "feat(api): add auth" → "**api**: add auth"
    local scope_pattern='^[a-z]+(\(([^)]+)\))?!?:[ ]+(.+)$'
    if [[ "$message" =~ $scope_pattern ]]; then
        local scope="${BASH_REMATCH[2]}"
        local msg="${BASH_REMATCH[3]}"

        if [ -n "$scope" ]; then
            echo "- **${scope}**: ${msg} (${hash})"
        else
            echo "- ${msg} (${hash})"
        fi
    fi
}
```

**Результат в CHANGELOG.md:**

```markdown
## [2.0.0] - 2025-12-20

### Security
- **auth**: fix JWT token validation bypass (abc1234)

### Added
- **agents**: add security-scanner worker (def5678)
- **commands**: add /health-security command (ghi9012)

### Changed
- ⚠️ BREAKING: **api**: change authentication flow (jkl3456)

### Fixed
- **build**: fix TypeScript compilation errors (mno7890)
```

---

## Фича 5: Безопасный Rollback

**Проблема:** Что если скрипт упадёт посередине? Вы получите:
- Половину обновлённых package.json
- Незаконченный changelog
- Созданный тег без пуша
- 💀

**Решение:** Скрипт создаёт бэкапы ПЕРЕД изменением файлов и восстанавливает их при ошибке:

```bash
# State tracking for rollback
CREATED_COMMIT=""
CREATED_TAG=""
declare -a BACKUP_FILES=()

create_backup() {
    local file="$1"
    if [ ! -f "$file" ]; then return 0; fi

    local backup="${file}.backup.$$"
    cp "$file" "$backup"
    BACKUP_FILES+=("$backup")
    log_info "Created backup: ${backup##*/}"
}

# Trap for cleanup on error
trap cleanup EXIT

cleanup() {
    local exit_code=$?

    if [ $exit_code -ne 0 ]; then
        log_error "Error occurred during release process"
        log_warning "Rolling back changes..."

        # Delete tag if created
        if [ -n "$CREATED_TAG" ]; then
            git tag -d "$CREATED_TAG" 2>/dev/null || true
            log_success "Deleted tag $CREATED_TAG"
        fi

        # Rollback commit
        if [ -n "$CREATED_COMMIT" ]; then
            git reset --soft HEAD~1 2>/dev/null || true
            log_success "Rolled back commit"
        fi

        # Restore files from backups
        restore_from_backups

        log_info "Rollback complete. Files restored from backups."
    else
        cleanup_backups  # Success - remove backup files
    fi
}
```

**Почему не `git restore`?**

Мы специально НЕ используем `git restore`, потому что это затёрло бы ручные правки, которые пользователь мог сделать до запуска скрипта. Бэкапы сохраняют именно то состояние, которое было до `release.sh`.

---

## Фича 6: SIGPIPE-safe для macOS

**Проблема:** На macOS с bash 3.2 и `set -o pipefail`, команда `head` вызывает SIGPIPE (exit code 141), когда закрывает pipe раньше, чем пишущий процесс завершится.

```bash
# Это падает на macOS:
git tag --sort=-version:refname | head -n 1
```

**Решение:** Заменяем `head` на `awk`:

```bash
# SIGPIPE-safe replacement for head -n N
safe_head() {
    local n="${1:-1}"
    awk -v n="$n" 'NR <= n {print} NR > n {exit}'
}

# Optimized for first line only
safe_first() {
    awk 'NR==1 {print; exit}'
}

# Usage:
LAST_TAG=$(git tag --sort=-version:refname | safe_first || echo "")
```

Теперь работает на Linux, macOS, и даже на древних системах.

---

## Фича 7: Проверка Remote Status

**Проблема:** Вы делаете релиз, а remote уже ушёл вперёд. Push фейлится, вы в раздрае.

**Решение:** Pre-flight check перед началом:

```bash
check_remote_status() {
    local branch="$1"

    # Fetch latest (without merging)
    git fetch origin "$branch" --quiet 2>/dev/null

    # Check if remote is ahead
    local behind
    behind=$(git rev-list --count "HEAD..origin/$branch" 2>/dev/null || echo "0")

    if [ "$behind" -gt 0 ]; then
        log_error "Remote is $behind commit(s) ahead of local"
        log_info "Please pull changes first:"
        echo "  git pull origin $branch"
        exit 1
    fi

    log_success "Local branch is up to date with remote"
}
```

---

## Интеграция с Claude Code

Магия `/push` в том, что это не просто bash-скрипт. Это **slash-команда**, которую Claude Code понимает нативно.

### Как создать свою slash-команду

1. Создайте файл `.claude/commands/my-command.md`:

```markdown
---
description: My awesome automation
argument-hint: [arg1|arg2]
---

Here's what this command does...

# Usage:
bash .claude/scripts/my-script.sh $ARGUMENTS --yes
```

2. Используйте в Claude Code:

```
/my-command arg1
```

Claude Code подставит `arg1` вместо `$ARGUMENTS` и выполнит скрипт.

### Флаг `--yes`

Обратите внимание на `--yes` в команде. Это **критически важно** для интеграции с Claude Code:

```bash
# Skip confirmation if --yes flag provided
if [ "$auto_confirm" = "true" ]; then
    log_info "Auto-confirming release (--yes flag provided)"
    return 0
fi

read -p "Proceed with release? [Y/n]: " confirm
```

Без `--yes` скрипт будет ждать пользовательского ввода, а Claude Code не умеет интерактивно отвечать на `read`.

---

## Preview Mode

Перед выполнением релиза скрипт показывает превью всех изменений:

```bash
show_preview() {
    cat << EOF
═══════════════════════════════════════════════════════════
                    RELEASE PREVIEW
═══════════════════════════════════════════════════════════

📌 Version: $CURRENT_VERSION → $NEW_VERSION (${BUMP_TYPE^^})
   Reason: $AUTO_DETECT_REASON

📊 Commits included: ${#ALL_COMMITS[@]}
   🔥 ${#BREAKING_CHANGES[@]} breaking changes
   🔒 ${#SECURITY_FIXES[@]} security fixes
   ✨ ${#FEATURES[@]} features
   🐛 ${#FIXES[@]} bug fixes

📦 Package Updates:
$(find "$PROJECT_ROOT" -name "package.json" -not -path "*/node_modules/*" | while read pkg; do
    echo "  ✓ ${pkg#$PROJECT_ROOT/}"
done)

📄 CHANGELOG.md Entry:
───────────────────────────────────────────────────────────
$(generate_changelog_entry "$NEW_VERSION" "$DATE")
───────────────────────────────────────────────────────────

💬 Git Commit Message:
───────────────────────────────────────────────────────────
chore(release): v$NEW_VERSION
───────────────────────────────────────────────────────────

🏷️  Git Tag: v$NEW_VERSION
🌿 Branch: $BRANCH
EOF
}
```

Вы видите ВСЁ, что произойдёт, до того как это произойдёт.

---

## Реальные примеры использования

### Быстрый патч-релиз

```bash
/push patch
# 1.3.4 → 1.3.5
```

### Minor релиз с новыми фичами

```bash
/push minor
# 1.3.5 → 1.4.0
```

### Major релиз (breaking changes)

```bash
/push major
# 1.4.0 → 2.0.0
```

### Авто-определение по коммитам

```bash
/push
# Скрипт сам решит: есть feat: → minor, только fix: → patch
```

---

## Статистика: До и После

| Метрика | До (вручную) | После (/push) |
|---------|--------------|---------------|
| Время на релиз | 5-10 минут | 3-5 секунд |
| Ошибки в changelog | ~30% релизов | 0% |
| Забытые package.json | ~20% | 0% |
| Рассинхрон версий | Постоянно | Никогда |
| Настроение разработчика | 😤 | 😎 |

---

## Где взять

Скрипт — часть open-source проекта **Claude Code Orchestrator Kit**:

**Репозиторий:** [github.com/maslennikov-ig/claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit)

**Лицензия:** MIT (бесплатно, можно использовать в коммерческих проектах)

**Что ещё есть в репозитории:**
- 36+ AI-агентов для Claude Code
- 20+ slash-команд
- 18+ переиспользуемых скиллов
- 7 MCP-конфигураций
- Quality gates для CI/CD

### Быстрый старт

```bash
# Клонируем
git clone https://github.com/maslennikov-ig/claude-code-orchestrator-kit.git

# Копируем .claude в свой проект
cp -r claude-code-orchestrator-kit/.claude /path/to/your/project/

# Используем!
/push patch
```

---

## Заключение

`/push` — это пример того, как можно автоматизировать рутинные задачи в Claude Code. Мы потратили день на написание 1000+ строк bash, но теперь экономим 5-10 минут на каждом релизе. При 2-3 релизах в день это **час в неделю**.

А главное — больше никаких "чёрт, я забыл добавить фикс в changelog" и "почему у меня версия 1.3.2, а на remote 1.3.5?".

**P.S.** Если у вас есть идеи, как улучшить скрипт — открывайте issue или PR на GitHub. Проект развивается, и мы рады контрибьюторам.

---

**Автор:** Игорь Масленников
*Пишу про AI-агентов, LLM-бенчмарки и архитектуру софта.*

📢 **Мой канал в Telegram:** [@maslennikovigor](https://t.me/maslennikovigor) — там я публикую свежие бенчмарки и DevOps-лайфхаки.
💬 **Личный контакт:** [@maslennikovig](https://t.me/maslennikovig)

---

**А как вы автоматизируете релизы?** Делитесь в комментариях — интересно узнать, какие инструменты используете.
