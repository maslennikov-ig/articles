# CLAUDE.md

## Claude Code CLI Adapter

- Primary workflow comes from global `~/.claude/CLAUDE.md` and the `orchestration-bridge` plugin.
- For medium/complex, risky, docs-sensitive, delegated, file-changing, or handoff-prone work, use `orchestration-bridge:orchestrator-stage`.
- Use Docs L1/L2: `@neuledge/context` first with lockfile-routed package/version; Context7 MCP or first-party docs as fallback only when L1 is missing, stale, or insufficient.
- Use Beads when available for file-changing, delegated, long, or handoff-prone work.
- Remote push, PR creation, merge, deploy, force-push, and production mutation require repo contract support and current user authorization.

## Project Conventions

**Code Standards**:
- No hardcoded credentials
- Temporary work: `.tmp/current/` (git ignored). Reports: `docs/reports/{domain}/{YYYY-MM}/`.

Project-specific facts, metrics, contact rules, and writing guidelines live in `CLAUDE.local.md` (git-ignored) — read it before drafting or editing any article.

## Reference Docs

- Agent orchestration: `docs/Agents Ecosystem/AGENT-ORCHESTRATION.md`
- Architecture: `docs/Agents Ecosystem/ARCHITECTURE.md`
- Quality gates: `docs/Agents Ecosystem/QUALITY-GATES-SPECIFICATION.md`
- Report templates: `docs/Agents Ecosystem/REPORT-TEMPLATE-STANDARD.md`
