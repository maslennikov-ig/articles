---
name: graphify-project
description: Use when enabling, auditing, refreshing, or using Graphify as a local project knowledge graph, especially when setup must be skill-driven and must not use external model/API-backed Graphify extraction unless explicitly authorized.
---

# Graphify Project

## Core Rule

This skill is the workflow. The `graphify` CLI is only the local graph engine used by the workflow.

Do not interpret a request to "enable Graphify" as permission to run standalone external model/API-backed extraction. Do not configure API keys, hosted backends, paid model calls, or Graphify git hooks unless the user explicitly asks in the current task.

For Codex, a narrow project-local `PreToolUse` hook that runs `graphify hook-check` is allowed and expected during setup. This is not the same as Graphify git hooks.

Default mode:

- local Graphify CLI installed or verified
- `.graphifyignore`, repo instructions, and optional orchestration config updated
- `.codex/hooks.json` includes the Codex `PreToolUse` Graphify reminder hook when the repo uses Codex
- `graphify update .` and `graphify cluster-only . --no-viz` used for a local project graph/report
- generated `graphify-out/` kept local and ignored unless the repo explicitly wants shared graph artifacts
- semantic/docs/PDF enrichment attempted only through an already available and authorized local/session-backed path; otherwise report it as blocked or deferred

## Preflight

Before changing files:

1. Read repo instructions: `AGENTS.md`, `CLAUDE.md`, `.codex/orchestrator.toml`, handoff/project notes, and `.gitignore` when present.
2. Create or select a Beads task if Beads is available and the setup will change files.
3. Inspect the repo shape, generated folders, dependencies, build outputs, temp/test artifacts, secrets/env files, large media, worktrees, and useful docs/research/PDF sources.
4. Decide whether the repo is large or durable enough to benefit from Graphify. For tiny/simple repos, stop with a recommendation instead of forcing setup.

## Setup

1. Verify or install the CLI engine:

   ```bash
   graphify --version
   graphify --help
   ```

   If missing, prefer `uv tool install graphifyy`, then `pipx install graphifyy`, then `pip install --user graphifyy`.

   If the latest package fails while building a native `tree-sitter-*` dependency because the local machine lacks `gcc`/`cc`, prefer a user-space compiler before asking for system packages:

   ```bash
   npm install -g @ziglang/cli
   ln -sf "$(npm prefix -g)/bin/zig" "$HOME/.local/bin/zig"
   CC="$HOME/.local/bin/zig-cc-python" uv tool install --force --python 3.12 graphifyy
   ```

   The `zig-cc-python` wrapper should call `zig cc` and filter only `-Wl,--exclude-libs,ALL`, which Zig's linker does not support. If a user-space compiler is not acceptable or cannot be installed, use the last known working pinned version only as a fallback, for example `uv tool install --python 3.12 graphifyy==0.8.18`.

2. Create or update `.graphifyignore`.

   Exclude dependency folders, build outputs, coverage, temp files, test artifacts, secrets, local worktrees, runtime state, large raw recordings, and agent runtime noise. Keep stable docs, architecture notes, ADRs, runbooks, research notes, and relevant PDFs unless the repo deliberately excludes them.

3. Add `graphify-out/` to `.gitignore` unless the repo explicitly commits shared graph artifacts.

4. Add a compact repo rule to `AGENTS.md` or the repo equivalent:

   - read `graphify-out/GRAPH_REPORT.md` before broad search for architecture, impact, or unfamiliar areas
   - use focused `graphify query`, `graphify path`, or `graphify explain`
   - never paste `graphify-out/graph.json` into chat context
   - Codex `PreToolUse` Graphify hook is allowed for graph reminders
   - do not install Graphify git hooks or external semantic backends unless explicitly asked
   - record `graph-reviewed: used`, `updated`, `no-change-needed`, or `blocked`

5. Add or merge `.codex/hooks.json` for Codex projects:

   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             {
               "type": "command",
               "command": "/home/me/.local/bin/graphify hook-check"
             }
           ]
         }
       ]
     }
   }
   ```

   If the `graphify` binary lives elsewhere, use `which graphify` and record the resolved absolute path. Do not add git hooks with `graphify hook install`.

6. If `.codex/orchestrator.toml` exists, add a small `[knowledge_graph]` section with graph dir, ignore file, update/query commands, hook policy, and closeout marker. Use `hooks_allowed = "codex_pre_tool_use_only"` or equivalent, `git_hooks_allowed = false`, and `codex_pre_tool_use_hook = true`.

## Build And Refresh

Use the local graph engine:

```bash
graphify update .
graphify cluster-only . --no-viz
```

Run these commands after all tracked setup files are written. If the agent commits, rebases, or otherwise changes `HEAD` after building the graph, run them again. Before final reporting, compare `git rev-parse --short=8 HEAD` with `Built from commit` in `graphify-out/GRAPH_REPORT.md`; for setup work they must match unless the final state intentionally has only uncommitted local changes, which must be reported.

If `.graphifyignore` was tightened to exclude sources that may already be in an existing graph, rebuild from a clean local graph directory instead of relying only on incremental update:

```bash
rm -rf graphify-out
graphify update .
graphify cluster-only . --no-viz
```

Then run 2-3 focused smoke checks, for example:

```bash
graphify query "What are the main architecture subsystems in this project?" --graph graphify-out/graph.json --budget 2000
graphify query "Where are the main entrypoints and configuration files?" --graph graphify-out/graph.json --budget 2000
graphify explain "README.md" --graph graphify-out/graph.json
```

Prefer exact node IDs from `GRAPH_REPORT.md` when broad natural-language queries are noisy.

## Semantic Sources

Be precise about the mode:

- `code/local graph`: Graphify CLI graph/report built without external model backend.
- `full semantic`: docs/research/PDF or other semantic extraction completed through an available and authorized backend or session-backed workflow.
- `blocked/deferred semantic`: full semantic extraction would require missing support, API keys, hosted model calls, or user authorization.

Do not run `graphify extract` with `openai`, `anthropic`, `gemini`, `claude`, or similar backend modes unless the user explicitly authorizes those model/backend calls for this task and credentials are already configured. Never print secrets.

If full semantic mode is blocked, keep the local graph and report:

```text
Graphify is installed and the local graph/report are available, but full semantic extraction is blocked or deferred because no authorized session-backed or backend mode is available.
```

## Closeout

Before reporting completion:

1. Run `git status --short` and `git diff --check`.
2. Confirm `graphify-out/` is ignored and not staged.
3. Confirm `.codex/hooks.json` contains only the intended Codex `PreToolUse` Graphify hook.
4. Confirm Graphify git hooks are not installed unless explicitly requested.
5. Confirm `graphify-out/GRAPH_REPORT.md` `Built from commit` matches current `HEAD` after setup or after any commit made during setup. If not, rerun `graphify update .` and `graphify cluster-only . --no-viz`.
6. Confirm `graphify-out/graph.json` has no forbidden `source_file` entries for excluded runtime/noise roots such as `.worktrees/`, `.claude/`, `node_modules/`, and `graphify-out/`.
7. Update Beads with commands and graph status when Beads is available.
8. Report `docs-reviewed: updated` or `docs-reviewed: no-change-needed`.
9. Report `graph-reviewed: updated`, `used`, `no-change-needed`, or `blocked` with command evidence.

Final report must include:

- Graphify version and install method
- mode: `code/local graph`, `full semantic`, or `blocked/deferred semantic`
- node/edge counts when available
- included and excluded sources
- changed files
- smoke query summaries
- blockers and next recommended action
