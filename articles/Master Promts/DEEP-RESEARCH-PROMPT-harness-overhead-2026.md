# Deep Research Prompt: Are elaborate AI-coding harnesses still worth it in 2026?

> Назначение: промпт для deep research к будущей статье на Хабр («харнесс vs поумневшие модели»).
> Запуск: один и тот же текст в двух инструментах для сравнения — Claude Research (Opus) и ChatGPT Deep Research.
> Проверка: `orch-prompts prompt-check --runtime claude --profile universal --kind prompt-card` → pass, 5127/6000 chars (2026-07-07).
> Копировать всё, что ниже разделителя.

---

# Deep Research Brief: Are elaborate AI-coding harnesses still worth it in 2026?

Goal: Produce an evidence-based report on what practitioners currently think (weight December 2025 - July 2026 most heavily) about heavyweight "harnesses" around AI coding agents - custom skills, subagent fleets, orchestration frameworks, memory systems, code knowledge graphs, prompt libraries, MCP tool stacks - now that frontier models (Claude Opus 4.x and Claude 5, GPT-5.x, Gemini 3) have absorbed much of what this scaffolding used to provide. Core question: is elaborate scaffolding still a net win, or has it become overhead that smarter models no longer need?

Who is asking: a practitioner running a heavily augmented setup on Claude Code and Codex CLI: Superpowers (process skills: brainstorming, TDD, systematic debugging), Beads (agent-native issue tracker), a code knowledge graph, spec-driven development (spec-kit), ~45 custom skills, dozens of custom subagents, multiple MCP servers, a custom orchestration console with per-model prompt profiles, and a two-tier docs pipeline. He is writing an analytical article and needs the real state of community opinion, not marketing.

Research questions:
1. Current sentiment split among practitioners actively using Claude Code / Codex CLI / Cursor / other agentic tools: what share of voiced opinion treats heavy scaffolding as (a) essential, (b) situational, (c) obsolete overhead? Support with threads, not vibes.
2. The "bitter lesson for scaffolding" argument: who makes it, in what form, with what evidence (each model generation breaks or absorbs harness features; RL-trained agentic behavior replaces orchestration)? Who pushes back, with what evidence?
3. Category-by-category verdict as discussed in the community - still paying for itself vs quietly abandoned: (a) many MCP servers / tool sprawl; (b) large custom-subagent fleets; (c) skill/prompt libraries; (d) multi-agent orchestration frameworks; (e) external memory / code knowledge graphs; (f) spec-driven development; (g) hooks, deterministic guardrails, verification gates.
4. Vendor absorption: which harness capabilities got built into products in the last year (Claude Code native memory, plan mode, agent teams, skills; Codex equivalents; Cursor), and how did users of DIY equivalents react?
5. Concrete costs people measure: context-window bloat from MCP tool definitions, instruction-following degradation from long CLAUDE.md files, token overhead of orchestration, maintenance burden as models update. Find posts with actual numbers or experiments.
6. Counter-trends: (a) the minimalist camp ("all you need is a CLAUDE.md and a plan") and its notable voices; (b) the industrialization camp (agent fleets, 24/7 pipelines, Gastown-style setups). What outcomes does each camp report?
7. Current positions of named practitioners, with dates: Simon Willison, Steve Yegge, Jesse Vincent (obra, Superpowers), Armin Ronacher, Boris Cherny or other Anthropic engineers, Thorsten Ball. Anyone who publicly changed their mind in the last 12 months is especially valuable.

Sources, in priority order: Reddit first - r/ClaudeAI, r/ClaudeCode, r/ChatGPTCoding, r/cursor, r/LocalLLaMA, r/ExperiencedDevs, r/programming - roughly the last 9 months. Then: Hacker News threads (hn.algolia.com), GitHub issues and discussions of popular harness repos (superpowers, beads, spec-kit, awesome-claude-code, claude-flow), engineering blogs and X threads by named practitioners, Anthropic and OpenAI official guidance where it confirms or contradicts community practice.

Quality bar:
- Every claim about "what people think" needs at least one link to a primary discussion, with date and rough engagement (upvotes, comments) when visible.
- Quote representative opinions verbatim (2-4 sentences each, with author handle and link) - exact wording matters because these will be quoted in an article.
- Separate three things explicitly: measured evidence, experienced-practitioner judgment, and vibes.
- Actively look for disconfirming evidence for both camps; if the community is split, report the split rather than averaging it.
- Treat vendor marketing, listicles, and SEO content as noise, not sentiment evidence.
- Flag anything older than mid-2025 as historical context, not current sentiment.

Preemptive clarifications (no need to ask): report language - English; length - as long as evidence requires, depth over brevity; audience - the practitioner above, writing for senior developers; skip paywalled sources; focus on coding agents, not general chatbot use.

Output: English report structured by research questions 1-7, then: a timeline of how sentiment shifted over the last 12 months; a table of harness categories x community verdict x strongest evidence link; the 10-15 best verbatim quotes with links; a closing section with the 5 most article-worthy findings (surprising, contrarian, or well-evidenced). Include a dated source list. Where evidence for a question is thin, say so explicitly instead of padding.
Stop: deliver the report in one pass; list unresolved gaps at the end rather than asking follow-up questions.
