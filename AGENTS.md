# Articles Agent Contract

This is a public, Git-first repository for Russian-language articles, source
packs, prompts, and reusable writing workflows. `articles/` contains finished
or in-progress publications, `promts/` contains research and drafting inputs,
and `.claude/skills/` contains the venue-specific writing workflows.

## Working Rules

- Read this file first. Before drafting or editing any article, also read the
  ignored `CLAUDE.local.md`; it owns private project facts, metrics, contact
  rules, and writing guidance. Stop if it is required but unavailable.
- Reuse the matching venue skill under `.claude/skills/` and the existing
  article/prompt pattern before adding a new workflow or format.
- Keep tracked material public-safe: no credentials, private client evidence,
  unpublished contact data, or local configuration.
- Do not invent sources, quotes, measurements, dates, or product claims.
  Preserve source links and distinguish measured facts from interpretation.
- Temporary work belongs in `.tmp/current/`; durable reports belong in
  `docs/reports/{domain}/{YYYY-MM}/`.
- User-facing communication and publication content are Russian unless the
  task explicitly asks for another language.

## Verification And Safety

- Run the focused content or workflow checks defined by the matching skill and
  the current task.
- Full article or product suites are release-only, not a default task gate.
- Do not push, open or merge a PR, publish content, deploy, send messages, make
  paid calls, or mutate live systems without explicit current authorization.
- Before any ordinary push, fetch and prove the remote is not ahead or
  diverged; never stage unrelated work.

<!-- ORCHESTRATION-BASELINE:BEGIN -->
<!-- orchestration-setup: token-efficiency/v1 -->
## Orchestration Defaults

- Route medium or complex work through `orchestrator-stage`; add parallel streams only for a recorded material benefit.
- Native Codex spawns explicitly use `fork_turns="none"` by default. Any non-`none` override needs a task-specific rationale and must keep essential facts reachable through the nearest `AGENTS.md`, the selected Beads goal, or an exact existing reference.
- Spawn prompts contain only Goal, Write zone, Verification, and Stop. Reference current sources; do not copy transcript history or reusable rules.
- Coalesce routine progress. Always surface blockers, decisions, material artifacts, the final result, and platform heartbeats.
- Prefer bounded summarized tool output with an explicit truncation signal. Expand output only for a recorded task-specific reason.
- Workers run only assigned focused RED/GREEN checks. Root owns one final acceptance; the full suite is epic/release-only.
- Reuse the model routes in `orchestrator-stage/references/delegation-and-isolation.md`; do not restate them here.
<!-- ORCHESTRATION-BASELINE:END -->
