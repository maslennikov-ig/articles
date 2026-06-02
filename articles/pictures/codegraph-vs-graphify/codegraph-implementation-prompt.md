# Universal CodeGraph Implementation Prompt

Use this prompt in Codex, Claude Code, or another coding agent when you want to add CodeGraph (the lightweight local symbol index) to a repository AND make the agent actually use it instead of grepping.

Companion to `graphify-implementation-prompt.md`. CodeGraph = lightweight runtime code index. Graphify = full project knowledge graph. They solve different problems; you can use both.

````text
Implement CodeGraph as a local code-symbol index for this repository, and configure the agent to query the index instead of doing broad file reads.

Goal:
Set up CodeGraph so that you (and future agents) resolve "where is X / who calls Y / what breaks if I touch Z" through a fast local index, instead of grepping and reading many files. This cuts tokens, tool calls, and wrong guesses.

Important principles:
- Keep CodeGraph local-first. The index is a derived cache of the code, not a shared artifact.
- The graph is rebuilt from source deterministically. Do not commit it.
- Do NOT place the index database on a network share or sync folder — SQLite there (and on WSL2) hits database-lock issues.
- Do not install Git hooks unless I explicitly approve them.
- If a required step (MCP support in this agent, install permissions) is unavailable, stop and report the missing requirement instead of pretending the index works.

Step 1: Inspect the project
Read:
- agent instruction files such as `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, or equivalent;
- `.gitignore`;
- package/config files to detect language(s) and framework;
- the current git status.
Identify: primary languages, dependency/build/generated folders, and what should never be indexed.

Step 2: Install or verify CodeGraph
Check:

```bash
codegraph --version
```

If missing, install with the best method for this environment, for example:

```bash
npx @colbymchenry/codegraph
```

Then verify `codegraph --version` and `codegraph --help`.
Do not install CodeGraph Git hooks.

Step 3: Build the initial index

```bash
codegraph init
```

This parses the code locally via tree-sitter into a local SQLite index (`.codegraph/`). No external API calls, nothing leaves the machine. Confirm the index was created and report rough node/symbol counts if the CLI prints them.

Step 4: Register CodeGraph as an MCP server for THIS agent

CodeGraph runs as an MCP (stdio) server started by `codegraph serve --mcp`. Register it using the MCP config format of the agent you are running in. Detect which agent this is and use the correct location:

- Codex CLI: the MCP-servers section of `~/.codex/config.toml`, plus rules in `~/.codex/AGENTS.md`.
- Claude Code: the `mcpServers` block in `~/.claude.json` (or project `.mcp.json`), plus rules in `CLAUDE.md`.
- Cursor / others: that tool's MCP config + its rules file.

Canonical server entry (adapt to the target format):

```
command: codegraph
args:    ["serve", "--mcp"]
type:    stdio
```

Do NOT hardcode a config format you are unsure about — use the documented MCP format of the actual agent, and report exactly what you wrote and where.

Step 5: Add the usage rule (this is what makes the agent actually use the index)

Update the project/agent instruction file (`AGENTS.md` / `CLAUDE.md` / equivalent) with a short, explicit rule. Without this rule the agent ignores the MCP server and keeps grepping out of habit:

```md
## CodeGraph Index

- For navigation, impact analysis, or exploring unfamiliar code, prefer the CodeGraph MCP tools (`codegraph_search`, `codegraph_context`, `codegraph_trace`) over grep/glob/Read.
- Only fall back to raw file reads when the index has no answer.
- The index lives in `.codegraph/` and auto-syncs via file watchers; do not commit it.
```

Step 6: Keep the index out of version control

Add to `.gitignore`:

```gitignore
# CodeGraph index — derived cache, rebuilt from source
.codegraph/
```

Each developer runs `codegraph init` once on their own machine; the watcher keeps it fresh. The team syncs CODE, not the index.

Step 7: Validate

```bash
codegraph search "<a known function or symbol in this repo>"
```

Then confirm the agent actually routes through the index: ask it a navigation question ("who calls X?", "where is Y defined?") and verify it calls a `codegraph_*` MCP tool rather than grepping. Summarize:
- index location and rough size;
- which MCP config file was edited;
- which instruction file got the usage rule;
- one successful smoke query.

Step 8: Verify repository state

```bash
git status --short
```

Ensure:
- `.gitignore` ignores `.codegraph/`;
- the `.codegraph/` index is NOT staged;
- the agent instruction file mentions the CodeGraph usage rule;
- no secrets or generated artifacts are staged.

Final report format:

```md
## CodeGraph Setup Result

Status: complete / partial / blocked

Installed:
- CodeGraph version: ...
- Install method: ...

Index:
- Location: `.codegraph/` (local only, gitignored)
- Symbols/nodes: ...

Agent integration:
- MCP config edited: ...
- Usage rule added to: ...

Smoke query:
- query: ...
  result summary: ...
- Index actually used by agent: yes / no

Blocked or deferred:
- ...
```
````
