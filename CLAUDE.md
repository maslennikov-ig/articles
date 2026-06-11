# CLAUDE.md

@../AGENTS.md

## Claude Code CLI Adapter

- Target runtime: Claude Code CLI in the VS Code integrated terminal on WSL.
- Primary workflow comes from global `~/.claude/CLAUDE.md` and the `orchestration-bridge` plugin.
- For medium/complex, risky, docs-sensitive, delegated, file-changing, or handoff-prone work, use `orchestration-bridge:orchestrator-stage`.
- Do not use `template-bridge` for new orchestration.
- Use Docs L1/L2: `@neuledge/context` first with lockfile-routed package/version; Context7 MCP or first-party docs only when L1 is missing, stale, or insufficient.
- Use Beads when available for file-changing, delegated, long, or handoff-prone work.
- Remote push, PR creation, merge, deploy, force-push, and production mutation require repo contract support and current user authorization.

## Preserved Project Notes

## Project Conventions

**File Organization**:
- Agents: `.claude/agents/{domain}/{orchestrators|workers}/`
- Commands: `.claude/commands/`
- Skills: `.claude/skills/{skill-name}/SKILL.md`
- Temporary: `.tmp/current/` (git ignored)
- Reports: `docs/reports/{domain}/{YYYY-MM}/`

**Code Standards**:
- Type-check must pass before commit
- Build must pass before commit
- No hardcoded credentials

**Agent Selection**:
- Worker: Plan file specifies nextAgent (health workflows only)
- Skill: Reusable utility, no state, <100 lines

**Supabase Operations**:
- Use Supabase MCP when `.mcp.json` includes supabase server
- Project: MegaCampusAI (ref: `diqooqbuchsliypgwksu`)
- Migrations: `packages/course-gen-platform/supabase/migrations/`

**MCP Configuration**:
- BASE (`.mcp.base.json`): context7 + sequential-thinking (~600 tokens)
- FULL (`.mcp.full.json`): + supabase + playwright + n8n + shadcn (~5000 tokens)
- Switch: `./switch-mcp.sh`

---

## Reference Docs

- Agent orchestration: `docs/Agents Ecosystem/AGENT-ORCHESTRATION.md`
- Architecture: `docs/Agents Ecosystem/ARCHITECTURE.md`
- Quality gates: `docs/Agents Ecosystem/QUALITY-GATES-SPECIFICATION.md`
- Report templates: `docs/Agents Ecosystem/REPORT-TEMPLATE-STANDARD.md`
