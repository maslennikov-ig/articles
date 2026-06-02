# Universal Graphify Implementation Prompt

Use this prompt in Codex, Claude Code, or another coding agent when you want to add Graphify to a repository.

````text
Implement Graphify as a local project knowledge graph for this repository.

Goal:
Set up Graphify so future agents can quickly understand the project, find architectural relationships, avoid broad file-reading loops, and keep the graph refreshed as part of normal development closeout.

Important principles:
- Keep Graphify local-first.
- Do not commit large generated graph outputs unless the project explicitly wants shared graph artifacts.
- Do not install Git hooks unless I explicitly approve them.
- Do not paste the full `graphify-out/graph.json` into chat context.
- Use `GRAPH_REPORT.md` for orientation and focused `graphify query/path/explain` commands for small relevant subgraphs.
- If semantic extraction requires API keys, a model backend, or session-backed Graphify support that is not available, stop and report the missing requirement instead of pretending the graph is complete.

Step 1: Inspect the project

Read:
- repository instructions such as `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or equivalent;
- `.gitignore`;
- package/config files;
- docs folder;
- existing task, handoff, project notes, or issue-tracker state if present;
- current git status.

Identify:
- project language/framework;
- generated folders;
- dependency folders;
- build outputs;
- temporary files;
- test artifacts;
- secrets/env files;
- large media folders;
- docs, research, ADR, runbook, and PDF folders that should be included;
- files that should never be indexed.

Step 2: Install or verify Graphify

Check:

```bash
graphify --version
```

If Graphify is missing, install it using the best package manager for this environment. Prefer one of:

```bash
uv tool install graphifyy
```

or:

```bash
pipx install graphifyy
```

or:

```bash
pip install --user graphifyy
```

Then verify:

```bash
graphify --version
graphify --help
```

Do not install Graphify hooks.

Step 3: Add ignore rules

Create or update `.graphifyignore`.

Exclude at least:
- dependency folders: `node_modules/`, `.venv/`, `venv/`, `vendor/`;
- build outputs: `.next/`, `dist/`, `build/`, `out/`, `coverage/`;
- test/runtime artifacts: `test-results/`, `playwright-report/`, `.tmp/`, temp folders;
- local secrets: `.env*`, `*.pem`, keys, credentials;
- local worktrees or sandbox folders;
- large raw recordings or binary artifacts unless they are intentionally part of the knowledge corpus.

Do not exclude useful docs by accident. Keep:
- `README.md`;
- `docs/**/*.md`;
- architecture docs;
- ADRs;
- runbooks;
- research notes;
- relevant PDFs, if semantic extraction backend is available.

Also update `.gitignore` to ignore:

```gitignore
graphify-out/
```

unless the project explicitly wants to commit shared graph artifacts.

Step 4: Configure project rules for future agents

Update the project's agent instruction file, for example `AGENTS.md`, `CLAUDE.md`, or the repo's equivalent, with a short Graphify rule:

```md
## Graphify Knowledge Graph

- If `graphify-out/GRAPH_REPORT.md` exists, read it before broad code search for architecture, impact, or unfamiliar areas.
- Use focused commands such as `graphify query`, `graphify path`, and `graphify explain` to retrieve small relevant subgraphs.
- Do not paste `graphify-out/graph.json` into chat context.
- Do not install Graphify hooks unless explicitly requested.
- Refresh the graph during closeout when code structure, architecture, public APIs, docs, or major behavior changes.
- Record one of:
  - `graph-reviewed: used - <report/query>`
  - `graph-reviewed: updated - <commands>`
  - `graph-reviewed: no-change-needed - <reason>`
  - `graph-reviewed: blocked - <reason>`
```

If the project has a local orchestration config, add a small Graphify/knowledge-graph section with:
- enabled flag;
- graph directory;
- ignore file;
- update command;
- query command;
- hook policy;
- closeout marker.

Step 5: Build the initial graph

First run a safe code-oriented refresh:

```bash
graphify update .
```

Then regenerate the report:

```bash
graphify cluster-only . --no-viz
```

If `graphify update .` is not enough for docs/PDF/research semantic extraction, check available backend support.

Check for available environment:

```bash
env | grep -E '^(OPENAI|ANTHROPIC|GEMINI|GOOGLE|DEEPSEEK|MOONSHOT|OLLAMA|AWS_)'
```

If a backend is available, run the appropriate full extraction command, for example:

```bash
graphify extract . --backend openai
```

or:

```bash
graphify extract . --backend claude
```

or:

```bash
graphify extract . --backend gemini
```

Use the backend that is actually configured. Do not invent keys. Do not print secrets.

If no backend is available, keep the code graph and report, then state:

```text
Graphify is installed and the code graph is available, but full semantic extraction is blocked because no LLM backend/API/session mode is available.
```

Step 6: Validate the graph

Check files:

```bash
test -f graphify-out/graph.json
test -f graphify-out/GRAPH_REPORT.md
```

Run focused smoke queries:

```bash
graphify query "What are the main architecture subsystems in this project?" --graph graphify-out/graph.json --budget 2000
graphify query "Where are the main entrypoints and configuration files?" --graph graphify-out/graph.json --budget 2000
graphify explain "README.md" --graph graphify-out/graph.json
```

If the project has a specific domain, add 1-2 domain-specific queries.

Summarize:
- graph node/edge count;
- whether the graph is code-only or full semantic;
- included sources;
- excluded sources;
- commands run;
- useful future queries.

Step 7: Integrate into development workflow

Update closeout or completion docs so agents refresh Graphify when needed.

Suggested rule:

```text
Before final completion, if the repo uses Graphify:
- use the graph if the task required architecture, routing, impact analysis, or unfamiliar-code exploration;
- refresh the graph if code structure, public APIs, architecture, docs, major behavior, or module boundaries changed;
- otherwise record `graph-reviewed: no-change-needed - <reason>`.
```

Do not refresh Graphify for every tiny change. Refresh when it helps future navigation.

Step 8: Verify repository state

Run:

```bash
git status --short
git diff --check
```

If the project has normal validation commands, run the lightweight ones that are relevant. Do not run expensive full suites unless justified.

Ensure:
- `.graphifyignore` is tracked;
- `.gitignore` ignores `graphify-out/`;
- generated `graphify-out/` is not accidentally staged;
- project instructions mention Graphify usage;
- no secrets or large generated artifacts are staged.

Final report format:

```md
## Graphify Setup Result

Status: complete / partial / blocked

Installed:
- Graphify version: ...
- Install method: ...

Graph:
- Mode: code-only / full semantic
- Nodes / edges: ...
- Report: `graphify-out/GRAPH_REPORT.md`
- Graph: `graphify-out/graph.json` local only

Included:
- ...

Excluded:
- ...

Workflow integration:
- Updated files: ...
- Closeout marker: `graph-reviewed: ...`

Smoke queries:
- query: ...
  result summary: ...

Blocked or deferred:
- ...

Next recommended action:
- ...
```
````
