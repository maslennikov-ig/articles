# CLAUDE.md

@AGENTS.md

## Claude Code CLI Adapter

- Primary workflow comes from global `~/.claude/CLAUDE.md` and the `orchestration-bridge` plugin.
- For medium/complex, risky, docs-sensitive, delegated, file-changing, or handoff-prone work, use `orchestration-bridge:orchestrator-stage`.
- Use Docs L1/L2: `@neuledge/context` first with lockfile-routed package/version; Context7 MCP or first-party docs as fallback only when L1 is missing, stale, or insufficient.
- Repository rules, writing prerequisites, safety boundaries, and verification
  are owned by `AGENTS.md` and are not repeated in this adapter.
