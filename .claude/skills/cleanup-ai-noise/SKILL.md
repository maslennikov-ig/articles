---
name: cleanup-ai-noise
description: Use at the end of any article-writing skill (habr-article, vcru-article, dzen-article, pikabu-article, telegraph-article, tenchat-article, telegram-article, telegram-announcement) before publication. Saves the draft to .tmp/current/articles/, invokes the ai-text-checker agent with platform context, presents the cleanup report and Needs-human-decision items to the author. Detective companion to the preventive skill `living-text-style` (invoked at ФАЗА 0 before drafting).
allowed-tools: Read, Write, Bash, Task
---

# Cleanup AI Noise

Trigger skill that wires an article-writing flow into the `ai-text-checker` agent. The agent owns the rules; this skill owns the plumbing.

## When to Use

Invoke from **ФАЗА 3** of any article-writing skill, BEFORE the manual «Не робот» checklist. The article-writing skill produces the draft text in conversation; this skill persists it, runs the agent, and presents the result.

Do NOT invoke for non-article content.

## Inputs

- `platform` (required): one of `habr | vc | dzen | pikabu | telegraph | tenchat | telegram | telegram-announcement`
- The final draft text from ФАЗА 2 of the calling article-skill (it lives in conversation context)

## Steps

### 1. Generate filename and path

```
filename = draft-{platform}-{YYYYMMDD-HHmm}.md
path     = .tmp/current/articles/{filename}
```

Use `date +%Y%m%d-%H%M` via Bash for the timestamp (Moscow time is fine — the file is throwaway).

### 2. Ensure target directory exists

```bash
mkdir -p .tmp/current/articles
```

### 3. Save the draft

Write the full final article text from ФАЗА 2 to `path` using the `Write` tool. Do not modify the text — pass it through verbatim.

### 4. Invoke the agent

Call the `Task` tool with:

```
subagent_type: ai-text-checker
description:   AI-noise cleanup for {platform} draft
prompt:        |
  file_path: .tmp/current/articles/{filename}
  platform: {platform}

  Run the full ai-text-checker workflow on this draft.
```

Wait for the agent to return.

### 5. Read the cleaned file

After the agent returns, `Read` the file at `path`. The file is now the post-cleanup version (the agent edited in-place).

### 6. Present results to the author

Output to the user a Russian-language summary. The agent prints the actual backup path in its report — pass it through verbatim.

```
Чистка AI-шума завершена.

Файл (после чистки): {file_path the agent worked on}
Backup (исходник):   {BACKUP_PATH from the agent's report — under .tmp/article-backups/{platform}/}

{полный текст отчёта от агента — таблицы статистики, ключевые правки, спорные места}

Дальше — ручной чек-лист «Не робот» из ФАЗА 3 текущего article-скилла.
Если в блоке «Требует решения автора» есть пункты — реши их вручную перед публикацией.
```

## Output

The author sees:
- Path to cleaned text + backup (centralized in `.tmp/article-backups/{platform}/`)
- Agent's structured report (metrics, layer statistics, top edits, items needing human decision)
- Reminder to run the manual «Не робот» checklist

## Backup convention (IMPORTANT)

Backups are NEVER stored next to the source article. The `ai-text-checker` agent writes them to:

```
.tmp/article-backups/{platform}/{stem}-{YYYYMMDD-HHmm}.bak.md
```

Example: `.tmp/article-backups/habr/codex-128-goal-experiments-20260504-1947.bak.md`

This keeps `articles/{platform}/` directories clean (only finished pieces, no `.bak` clutter). Since `.tmp/` is git-ignored, backups don't pollute commits either.

## Notes

- The `ai-text-checker` agent is the Single Source of Truth for the AI-marker catalog. This skill must NOT duplicate any rules from the agent body.
- If the calling article-skill already has a different draft persistence convention (e.g., a final `articles/{platform}/{slug}.md` save), use that path INSTEAD of `.tmp/current/articles/` — the agent works on whatever path is passed in. Backups still go to the centralized location regardless.
- Per-skill discovery: `/cleanup-ai-noise` triggers this skill in any session.
