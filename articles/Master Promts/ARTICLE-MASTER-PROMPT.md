# Universal Article Prompt: Claude Code Orchestrator Kit

> **Purpose**: This is a master prompt for generating professional articles about the Claude Code Orchestrator Kit across different platforms (VC.ru, Habr, Telegram, Medium, LinkedIn, YouTube scripts, etc.)

---

## Author Context (Write in First Person)

**Name**: Igor Maslennikov

**Background** (Keep Brief):
- In IT since 2013
- Managed traditional IT company (DNA IT) for years
- **Last 2 years**: Actively developing AI division (AI Dev Team)
- **Reality**: More and more clients choose AI division over traditional teams
- **Why**: Faster (1-2 weeks vs 2-3 months), cheaper (-80% cost), better quality (automated checks)

**Voice & Tone**:
- Professional but not corporate
- Practical, not theoretical (everything tested on real projects)
- Confident but not arrogant
- **NO info-marketing language** (no "revolutionary", "breakthrough", "game-changer")
- Technical depth balanced with business clarity
- First-person narrative ("I created", "We discovered", "My team")

---

## Disclaimer: Expected Pushback

**ALWAYS include this section** (near the beginning or end of article):

I understand this article will likely receive significant pushback from developers. Stories about "vibe coding", concerns about AI replacing programmers, accusations of oversimplification.

**My take**: I think this reaction is more about **fear mixed with arrogance** than genuine technical criticism.

**Fear**: "If AI can do my job, what happens to me?"
**Arrogance**: "Only humans can write *real* code, AI is just a toy."

**Reality**: AI doesn't replace good developers. It amplifies them. The orchestrator kit isn't about replacing programmers—it's about removing repetitive tasks, automating quality checks, and preserving context so developers can focus on architecture and complex problems.

If you disagree—fine. Clone the repo, try it, then tell me where I'm wrong. I prefer technical arguments over emotional reactions.

**Tone**: Brief, direct, no aggression. Acknowledge legitimate concerns, dismiss emotional reactions.

---

## Project Overview: Claude Code Orchestrator Kit

### What It Is

**Claude Code Orchestrator Kit** is a free, open-source (MIT License) automation system that transforms Claude Code into a professional orchestration platform with 33+ specialized AI agents.

**Repository**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit
**NPM Package**: `npm install -g claude-code-orchestrator-kit`
**License**: MIT (completely free for commercial use)

### Why It Exists

**Problem**: Standard Claude Code is powerful but:
- Burns through context window quickly
- Lacks systematic workflow management
- No quality gates or verification
- No specialization for different tasks
- Manual MCP server management

**Solution**: Transform Claude Code from a powerful assistant into a **professional orchestration system** where the main Claude Code instance acts as an orchestrator delegating to specialized sub-agents.

---

## Core Innovation: Orchestrator Pattern

### The Main Paradigm Shift

**Traditional Approach**:
- Claude Code does everything directly
- Rapidly exhausts context window
- No verification system
- Manual quality checks

**Our Approach**:
- **Main Claude Code = Orchestrator ONLY**
- All complex tasks → delegated to specialized sub-agents
- Each sub-agent has isolated context
- Mandatory verification after each delegation
- Automated quality gates (type-check, build, tests)

### Non-Traditional CLAUDE.md Usage

**Standard Practice**: Store entire project history in CLAUDE.md
- Problem: Wastes context tokens on historical data

**Our Innovation**: CLAUDE.md as **Behavioral Operating System**
- Contains ONLY orchestration rules
- No project history
- Defines how to gather context BEFORE delegation
- Specifies verification rules AFTER delegation
- Forces context preservation

**Key Rules** (from CLAUDE.md:1-138):
1. **GATHER FULL CONTEXT FIRST** (mandatory before any delegation)
2. **DELEGATE TO SUBAGENTS** (provide complete context + validation criteria)
3. **VERIFY RESULTS** (never skip verification: read files + run type-check)
4. **ACCEPT/REJECT LOOP** (re-delegate with corrections if failed)
5. **TRACK PROGRESS** (TodoWrite for visibility)
6. **COMMIT STRATEGY** (per-task commits with `/push patch`)

---

## SpecKit Foundation & Enhancement

### What is SpecKit?

**SpecKit** (by GitHub) is a specification-driven development toolkit originally designed for structured feature development. It provides commands like:
- `/speckit.analyze` - Analyze requirements
- `/speckit.specify` - Generate specifications
- `/speckit.plan` - Create implementation plan
- `/speckit.tasks` - Break into actionable tasks
- `/speckit.implement` - Execute implementation

**Why SpecKit?**: Excellent foundation for structured workflow, but needs enhancement for real production use.

### Our Enhancement: Phase 0 (Planning Phase)

**Original SpecKit Problem**: Immediately starts implementation without agent preparation

**Our Solution**: Add **Phase 0: Planning** (ALWAYS first step in tasks.md execution)

**Phase 0 Responsibilities** (from spec-kit-comprehensive-updates.md:15-49):

#### Task 1: Executor Assignment
- Analyze ALL tasks from tasks.md
- Classify: `PARALLEL` vs `SEQUENTIAL` execution
- Assign executors:
  - `[EXECUTOR: MAIN]` - ONLY trivial tasks (1-2 line fixes, simple imports)
  - `[EXECUTOR: existing-agent]` - If 100% match with existing sub-agent
  - `[EXECUTOR: FUTURE-agent-name]` - If no match (agent needs creation)

#### Task 2: Meta-Agent Creation (If FUTURE Agents Exist)
- Launch N `meta-agent-v3` calls in **single message** (atomicity rule)
- **1 FUTURE agent = 1 meta-agent call** (parallel execution in single message)
- After creation: **ask user to restart Claude Code**

#### Task 3: Research Resolution
- **Simple Research**: Use agent tools (Grep, Read, WebSearch, Context7)
- **Complex Research**: Create English prompt in `{FEATURE_DIR}/research/`, wait for deepresearch results

#### Atomicity Rule (CRITICAL)
**Pattern**: 1 Task = 1 Agent Invocation
- Never give multiple tasks to one agent
- **Parallel tasks**: Launch N agent calls in single message
- Example: 3 parallel tasks → 3 agent calls in single message
- Sequential tasks: 1 agent → wait → next agent

**Rationale**: Prevents context overflow, enables parallelization, ensures focused execution

---

## Meta-Agent: The Agent Factory

### What is meta-agent-v3?

**Purpose**: Creates new specialized agents in 2-3 minutes following project patterns

**Location**: `.claude/agents/meta/workers/meta-agent-v3.md` (500 lines)

**Agent Types It Creates**:
1. **Workers** - Execute tasks from plan files (bug-fixer, security-scanner, etc.)
2. **Orchestrators** - Coordinate multi-phase workflows (bug-orchestrator, deployment-orchestrator)
3. **Simple Agents** - Standalone tools without coordination

### How It Works (meta-agent-v3.md:12-36)

**Step 0**: Determine agent type (worker/orchestrator/simple)
**Step 0.5**: Load latest Claude Code docs via WebFetch (optional)
**Step 1**: Load architecture (`ARCHITECTURE.md` + `CLAUDE.md`)
**Step 2**: Gather essentials (name, domain, purpose, type-specific details)
**Step 3**: Generate (YAML frontmatter → structure → validate → write)

### Worker Structure (meta-agent-v3.md:41-87)

**Workers** execute specific tasks with 5-phase structure:
1. **Phase 1: Read Plan File** - Load `.{workflow}-plan.json` from orchestrator
2. **Phase 2: Execute Work** - Perform domain-specific tasks
3. **Phase 3: Validate Work** - Run quality gates (type-check, build, tests)
4. **Phase 4: Generate Report** - Standardized report format
5. **Phase 5: Return Control** - Exit (orchestrator resumes)

**Critical**: Workers MUST return control, never invoke other workers

### Orchestrator Structure (meta-agent-v3.md:109-157)

**Orchestrators** coordinate workflows with:
- **Phase 0: Pre-Flight** - Setup, validation, TodoWrite initialization
- **Phase 1-N**: Create plan files → Signal readiness → **Exit** (main session invokes worker)
- **Quality Gates**: Validate after each phase (blocking/non-blocking)
- **Return Control Pattern**: Orchestrator → creates plan → exits → main invokes worker → worker completes → orchestrator resumes

**Critical**: Orchestrators NEVER use Task tool to invoke workers (defeats isolation purpose)

---

## Health Commands: Automated Maintenance

### Overview

**Health commands** run automated maintenance workflows:
- `/health-bugs` - Bug detection and fixing
- `/health-security` - Security vulnerability scanning and remediation
- `/health-deps` - Dependency audit and safe updates
- `/health-cleanup` - Dead code detection and removal
- `/health-metrics` - Monthly ecosystem health reports

### Architecture Pattern

**All health workflows** follow same pattern:

**Orchestrator** (coordinates phases):
1. Pre-flight validation
2. Discovery phase (invoke hunter/scanner/auditor worker)
3. Quality gate (validate report)
4. Implementation phase (invoke fixer/updater/remover worker)
5. Quality gate (type-check + build + tests)
6. Verification phase (re-run discovery, check if issues remain)
7. **Iterative loop** (repeat until clean or max iterations)
8. Final summary

**Workers** (execute specific tasks):
- **Hunters/Scanners/Auditors**: Detect issues, generate reports
- **Fixers/Updaters/Removers**: Implement fixes, generate reports with changes
- All workers: Follow 5-phase structure (read plan → work → validate → report → return)

### Example: /health-bugs Workflow

**Phase 1: Bug Detection**
- Orchestrator creates `bug-hunting-plan.json`
- Orchestrator signals readiness, exits
- Main session invokes `bug-hunter` worker
- Worker scans codebase, categorizes bugs (critical/high/medium/low)
- Worker generates `bug-hunting-report.md`
- Worker returns control
- Orchestrator resumes, validates report

**Phase 2: Bug Fixing (By Priority)**
- Orchestrator creates `bug-fixing-plan.json` (priority: critical)
- Orchestrator signals readiness, exits
- Main session invokes `bug-fixer` worker
- Worker fixes critical bugs, validates (type-check + build)
- Worker generates `bug-fixes-implemented.md`
- Worker returns control
- Orchestrator runs quality gates

**Phase 3: Verification**
- Re-run bug-hunter to check remaining issues
- If issues remain AND iterations < max: repeat Phase 2 with next priority
- If clean OR max iterations: generate final summary

**Why Iterative?**: Complex codebases have hundreds of issues, fixing all at once would overflow context

---

## Worktree Commands: Parallel Feature Development

### The Challenge

Traditional Git workflow:
- Work on 1 feature at a time
- Context switching requires stash/commit
- Can't test multiple features in parallel

### Our Solution: Git Worktrees + Claude Code

**Worktree commands**:
- `/worktree-create` - Create new worktree for feature branch
- `/worktree-list` - Show all worktrees with status
- `/worktree-cleanup` - Remove merged/stale worktrees
- `/worktree-remove` - Delete specific worktree

### Workflow

**Setup**:
1. Run `/worktree-create feature/new-auth-flow`
2. Creates `.worktrees/feature-new-auth-flow/` directory
3. Separate branch, isolated workspace

**VS Code Integration** (settings.local.json.example):
- Add `.worktrees/*` to workspace folders
- Switch between features via folder selector
- Each worktree = separate Claude Code context
- Run multiple Claude Code sessions in parallel

**Benefits**:
- **Parallel development**: 3-5 features simultaneously
- **No context pollution**: Each worktree = clean slate
- **Easy testing**: Switch folders, not branches
- **Safe experimentation**: Isolate risky changes

**Real Usage**:
- Main workspace: Production hotfixes
- Worktree 1: Feature A development (Claude Code active)
- Worktree 2: Feature B development (Claude Code active)
- Worktree 3: Experimental refactoring (Claude Code monitoring)

---

## MCP Server Management

### The Context Budget Problem

**Claude Code MCP Servers** provide powerful integrations:
- **Context7**: Library documentation
- **Supabase**: Database operations
- **Sequential Thinking**: Enhanced reasoning
- **n8n**: Workflow automation
- **Playwright**: Browser automation
- **shadcn**: UI components

**Problem**: Each MCP server consumes **500-1500 tokens** from context budget
- FULL config: ~5000 tokens (10% of context window)
- Rarely need all servers simultaneously

### Our Solution: Dynamic MCP Switching

**Script**: `switch-mcp.sh` (100 lines)

**Available Configurations**:
1. **BASE** (~600 tokens): Context7 + Sequential Thinking (daily use)
2. **SUPABASE** (~2500 tokens): BASE + Supabase (database work)
3. **SUPABASE-FULL** (~3000 tokens): BASE + 2 Supabase projects
4. **N8N** (~2500 tokens): BASE + n8n automation
5. **FRONTEND** (~2000 tokens): BASE + Playwright + shadcn (UI work)
6. **FULL** (~5000 tokens): All servers (when needed)

**Usage**:
```bash
./switch-mcp.sh
# Select option 1-6
# Script copies mcp/.mcp.{config}.json to .mcp.json
# Restart Claude Code
```

**Benefits**:
- **Save context tokens**: Only load what you need
- **Faster startup**: Fewer servers = faster initialization
- **Clearer purpose**: Config name reflects workflow
- **Easy switching**: 1 command + restart

**Real Workflow**:
- Morning: BASE config (general development)
- Database task: Switch to SUPABASE
- UI work: Switch to FRONTEND
- Complex feature: Switch to FULL
- End of day: Back to BASE

---

## Skills Library: Reusable Utilities

### What Are Skills?

**Skills** are reusable utility functions (< 100 lines) that agents invoke via `Skill` tool for specific tasks (validation, formatting, parsing).

**Location**: `.claude/skills/{skill-name}/SKILL.md`

**Difference from Agents**:
- ✅ Skills: Stateless, no context isolation, invoked via `Skill` tool
- ✅ Agents: Stateful, context-isolated, invoked via `Task` tool

### Key Skills (15+ Total)

**Validation Skills**:
- `run-quality-gate` - Execute type-check/build/tests validation
- `validate-plan-file` - Verify plan JSON schema
- `validate-report-file` - Check report completeness

**Reporting Skills**:
- `generate-report-header` - Create standardized report headers
- `format-markdown-table` - Generate well-formatted tables
- `format-todo-list` - Create TodoWrite-compatible lists
- `generate-changelog` - Generate changelog from commits

**Utility Skills**:
- `parse-git-status` - Parse git status into structured data
- `parse-error-logs` - Parse build/test/lint output
- `calculate-priority-score` - Score bugs/tasks by severity
- `rollback-changes` - Restore files from changes log
- `render-template` - Variable substitution in templates

### How Agents Use Skills

**Example: Worker using run-quality-gate**
```markdown
## Phase 3: Validate Work

Use `run-quality-gate` Skill to execute validation:

- Command: `pnpm type-check`
- Blocking: true
- If FAILED: Rollback changes, report failure
- If PASSED: Proceed to Phase 4
```

**Benefits**:
- **Consistency**: Same validation logic across all workers
- **Maintainability**: Update once, affects all agents
- **Clarity**: Agents focus on domain logic, not utility implementation

**Creating New Skills**:
- Use `skill-builder-v2` agent
- Define input/output format
- Keep < 100 lines
- Document usage scenarios

---

## Webhook Integration: Task Completion Notifications

### The Problem

When Claude Code finishes task:
- You might be in different tab/project
- No notification = wasted waiting time
- Manual checking = context switching

### Our Solution: Webhook on Task Completion

**Configuration** (settings.local.json.example:8-19):
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo '✅ Task completed!' && date >> ~/claude-code-log.txt"
          }
        ]
      }
    ]
  }
}
```

**How It Works**:
1. Claude Code completes task (reaches "Stop" state)
2. Hook triggers command execution
3. Command can:
   - Send notification (notify-send on Linux, osascript on macOS)
   - Log to file
   - Trigger external webhook
   - Play sound

**Real Usage Examples**:

**Slack Notification**:
```bash
curl -X POST https://hooks.slack.com/services/YOUR/WEBHOOK \
  -d '{"text":"Claude Code task completed!"}'
```

**System Notification** (Linux):
```bash
notify-send "Claude Code" "Task completed!" -i checkbox-checked
```

**Telegram Bot**:
```bash
curl -s -X POST https://api.telegram.org/bot{TOKEN}/sendMessage \
  -d chat_id={CHAT_ID} -d text="Task done"
```

**Benefits**:
- **Parallel work**: Start task, switch to other project, get notified when done
- **Productivity**: No manual checking
- **Context preservation**: Return exactly when needed

---

## Additional Commands

### /push - Automated Release Management

**Purpose**: Analyzes commits, detects version bump type, updates package.json, generates changelog, creates git tag

**Usage**:
```bash
/push        # Auto-detect version bump
/push patch  # 1.0.0 → 1.0.1
/push minor  # 1.0.0 → 1.1.0
/push major  # 1.0.0 → 2.0.0
```

**Workflow**:
1. Analyze commits since last release
2. Detect features, fixes, breaking changes
3. Determine version bump type (if not specified)
4. Update `package.json`
5. Generate changelog entry
6. Create git commit + tag
7. Push to remote

### /translate-doc - Documentation Translation

**Purpose**: Translate documentation between English and Russian

**Usage**:
```bash
/translate-doc path/to/doc.md
```

**Features**:
- Preserves markdown formatting
- Maintains code blocks
- Keeps links intact
- Auto-detects source language

---

## Why This Is Better Than Standard Claude Code

### 1. Context Budget Management

**Standard Claude Code**: Burns through context rapidly
- Everything in main conversation
- History accumulates
- ~50K tokens → unusable after few tasks

**Our System**: Context preservation via orchestration
- Main Claude Code = orchestrator only (~10K tokens)
- Sub-agents = isolated contexts (reset after task)
- Can work on project indefinitely

### 2. Quality Assurance

**Standard Claude Code**: Manual verification
- User must check code
- Easy to miss errors
- No systematic validation

**Our System**: Automated quality gates
- Type-check after every task
- Build verification
- Test execution
- Rollback on failure
- Accept/reject loop until correct

### 3. Specialization

**Standard Claude Code**: Generalist for everything
- Same instructions for all tasks
- No domain expertise

**Our System**: Specialized agents
- bug-hunter: Knows bug patterns
- security-scanner: Knows vulnerabilities
- database-architect: Knows Postgres best practices
- Each agent: Optimized instructions for domain

### 4. Workflow Management

**Standard Claude Code**: Ad-hoc execution
- No structured phases
- Manual progress tracking
- No systematic approach

**Our System**: SpecKit + Orchestration
- Phase 0: Planning (executor assignment, meta-agent creation)
- Phase 1-N: Implementation (structured, verified)
- TodoWrite tracking
- Per-task commits
- Audit trail

### 5. Parallel Development

**Standard Claude Code**: Sequential workflow
- 1 task at a time
- Context switching overhead

**Our System**: Worktrees + Multiple Claude Code Sessions
- 3-5 features in parallel
- Isolated workspaces
- No context pollution
- Webhook notifications

### 6. Iterative Quality

**Standard Claude Code**: One-shot execution
- Fix once, hope it works
- No re-validation

**Our System**: Iterative refinement
- Health workflows: Loop until clean
- Verification phase: Detect remaining issues
- Max iterations: Safety limit
- Partial success handling

---

## Measurable Benefits

**From AI Dev Team Real Experience**:

**Speed**:
- Traditional team: 2-3 months per project
- With orchestrator kit: 1-2 weeks per project
- **~75% faster development**

**Cost**:
- Traditional IT department: 20 specialists
- With orchestrator kit: 3 people + 33 agents
- **-80% cost reduction**

**Quality**:
- Traditional: Manual code review, reactive bug fixing
- With orchestrator kit: Automated quality gates, proactive scanning
- **Fewer bugs in production**

**Scalability**:
- Traditional team: 1-2 projects in parallel
- With orchestrator kit: 5-7 projects simultaneously
- **3-5x parallelization**

**Context Window Usage**:
- Standard Claude Code: ~50K tokens after few tasks (unusable)
- Orchestrator kit: ~10-15K tokens main conversation (sustainable)
- **Indefinite project work**

---

## Installation & Getting Started

**NPM Installation**:
```bash
npm install -g claude-code-orchestrator-kit
# or
npx claude-code-orchestrator-kit
```

**Manual Installation**:
```bash
git clone https://github.com/maslennikov-ig/claude-code-orchestrator-kit.git
cd claude-code-orchestrator-kit
cp .env.example .env.local  # Configure credentials
./switch-mcp.sh  # Select MCP configuration
# Restart Claude Code
```

**First Steps**:
1. Copy `.claude/` to your project
2. Copy `mcp/` configurations
3. Copy `CLAUDE.md` (behavioral OS)
4. Configure `.env.local`
5. Run `./switch-mcp.sh` → select BASE
6. Restart Claude Code
7. Try `/health-bugs` to verify setup

---

## Technical Architecture Summary

**Core Components**:
1. **CLAUDE.md**: Behavioral operating system (orchestration rules)
2. **SpecKit Enhancement**: Phase 0 planning with meta-agent creation
3. **33+ Agents**: 4 orchestrators + 24 workers + 5 support agents
4. **15+ Skills**: Reusable utilities for validation/formatting/parsing
5. **MCP Switcher**: Dynamic configuration management (600-5000 tokens)
6. **Worktree Commands**: Parallel feature development
7. **Health Workflows**: Automated maintenance (bugs, security, deps, dead code)
8. **Webhook Hooks**: Task completion notifications

**File Organization**:
- `.claude/agents/{domain}/{orchestrators|workers}/` - Agent definitions
- `.claude/commands/` - Slash commands (19+)
- `.claude/skills/{skill-name}/SKILL.md` - Reusable utilities
- `.claude/schemas/` - JSON schemas for plan files
- `.tmp/current/` - Temporary files (plans, reports, changes logs)
- `docs/Agents Ecosystem/` - Architecture documentation
- `mcp/` - MCP configuration files

**Workflow Pattern**:
```
User Request
  ↓
Main Claude Code (Orchestrator)
  ├→ Gather context (read code, search patterns, check commits)
  ├→ Create plan file (.{workflow}-plan.json)
  ├→ Validate plan (validate-plan-file Skill)
  ├→ Signal readiness, EXIT
  ↓
Main Session (User Context)
  ├→ Invoke Sub-Agent (via Task tool)
  ↓
Sub-Agent (Isolated Context)
  ├→ Read plan file
  ├→ Execute work
  ├→ Validate (run-quality-gate Skill)
  ├→ Generate report (generate-report-header Skill)
  ├→ Return control, EXIT
  ↓
Main Claude Code (Resumes)
  ├→ Read report
  ├→ Verify results (read files, run type-check)
  ├→ Accept OR Re-delegate with corrections
  ├→ Mark task complete
  ├→ Run /push patch
  ├→ Move to next task
```

---

## Article Adaptation Guidelines

### For VC.ru (Russian Business Audience)

**Focus**:
- Business value (ROI, cost reduction, speed)
- Real metrics from AI Dev Team
- Practical implementation (not just theory)
- **NO hype**: Use business language, avoid tech jargon

**Structure**:
- Lead: Problem (traditional development costs/speed)
- Solution: Orchestrator kit benefits
- How it works: High-level architecture
- Results: Measurable outcomes
- Disclaimer: Expected pushback section
- Call-to-action: Try it (free, MIT license)
- Contact & Feedback: Telegram links, open to criticism/ideas

**Tone**: Professional business article, first-person narrative

**Length**: 10,000-15,000 characters (VC.ru standard)

### For Habr (Technical Russian Audience)

**Focus**:
- Technical architecture details
- Code examples
- Agent patterns
- MCP integration
- SpecKit enhancement logic

**Structure**:
- Problem: Context window management
- Solution: Orchestration pattern
- Implementation: Phase 0, meta-agent, workers/orchestrators
- Deep dive: Pick 2-3 components (e.g., health workflows, worktrees, MCP switcher)
- Disclaimer: Expected pushback section
- Conclusion: Installation guide
- Contact & Feedback: Telegram links, open to criticism/ideas

**Tone**: Technical deep-dive, developer-to-developer

**Length**: 15,000-25,000 characters

### For Telegram Channel (Quick Updates)

**Focus**:
- Single feature per post
- Visual clarity (code blocks, diagrams)
- Quick wins (5-minute read)

**Structure**:
- Hook: Bold claim (e.g., "Parallel feature development with Claude Code")
- Demo: Code example or screenshot
- Benefit: What you gain
- Link: GitHub repo
- Contact: Telegram channel link (brief)

**Tone**: Conversational, enthusiastic but not hype

**Length**: 1,000-2,000 characters per post

### For YouTube Script (Video Tutorial)

**Focus**:
- Visual demonstration
- Step-by-step walkthrough
- Real-time coding session

**Structure**:
- 00:00 Intro (problem statement)
- 01:00 Installation
- 03:00 Demo 1: /health-bugs workflow
- 08:00 Demo 2: /worktree-create parallel development
- 13:00 Demo 3: switch-mcp.sh context management
- 18:00 Wrap-up (results, repository link, Telegram contacts)

**Tone**: Tutorial style, screen recording with voiceover

**Length**: 15-20 minute video

---

## Key Talking Points (Always Include)

1. **Free & Open-Source**: MIT license, no restrictions
2. **Battle-Tested**: Used by AI Dev Team for real client projects
3. **Measurable Results**: -80% cost, 1-2 weeks vs 2-3 months, 5-7 parallel projects
4. **Context Preservation**: Orchestration = indefinite project work
5. **Automation**: Health workflows, quality gates, webhook notifications
6. **Specialization**: 33+ agents, each expert in domain
7. **SpecKit Enhancement**: Phase 0 planning with meta-agent creation
8. **Non-Traditional CLAUDE.md**: Behavioral OS, not history dump
9. **MCP Management**: Dynamic switching saves 500-4500 tokens
10. **Parallel Development**: Worktrees + multiple Claude Code sessions
11. **Open to Feedback**: Telegram contacts, super open to criticism/ideas/questions

---

## What NOT to Include

❌ Avoid info-marketing language:
- "Revolutionary", "breakthrough", "game-changing"
- "This will change everything"
- "You won't believe"
- Excessive exclamation marks!!!

❌ Avoid hype:
- Exaggerated claims without evidence
- Future promises ("will be able to")
- Unverified statistics

❌ Avoid theory-only:
- Abstract concepts without examples
- "Could potentially", "might work"
- Speculation without data

✅ Instead use:
- Specific metrics (80%, 1-2 weeks, 33 agents)
- Real examples (AI Dev Team experience)
- Concrete implementation (code snippets, commands)
- First-person narrative (I created, we tested)

---

## Call-to-Action (Always End With)

**Repository**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit
**NPM Package**: `npm install -g claude-code-orchestrator-kit`
**License**: MIT (free for commercial use)

**Get Started**:
```bash
git clone https://github.com/maslennikov-ig/claude-code-orchestrator-kit.git
cd claude-code-orchestrator-kit
./switch-mcp.sh  # Select BASE configuration
# Restart Claude Code
# Try /health-bugs
```

---

## Contact & Feedback (Always Include)

### 📱 Telegram

**Channel** (rare but interesting posts): https://t.me/maslennikovigor
Drop by, read my thoughts and articles. I don't post often, but when I do—it's worth it.

**Direct Contact**: https://t.me/maslennikovig
Need to talk? Write me directly. Always happy to connect.

### 💬 Feedback: I'm Wide Open

**I'd love to hear**:
- **Criticism** — What's wrong with this approach? Where are the weak spots?
- **Ideas** — What features should be added? What's missing?
- **Suggestions** — How to improve, optimize, or refactor the system?
- **Questions** — Anything unclear? Ask away.

**Channels for feedback**:
- **GitHub Issues**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/issues (for bugs, features)
- **GitHub Discussions**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/discussions (for ideas, questions)
- **Telegram**: https://t.me/maslennikovig (for direct conversation)

**Tone**: Super open to constructive dialogue. No ego, just want to make this better.

---

## Additional Resources (Link in Articles)

- **Architecture Documentation**: `docs/Agents Ecosystem/ARCHITECTURE.md`
- **Agent Orchestration Guide**: `docs/Agents Ecosystem/AGENT-ORCHESTRATION.md`
- **SpecKit Enhancements**: `docs/Agents Ecosystem/spec-kit-comprehensive-updates.md`
- **Tutorial**: `docs/TUTORIAL-CUSTOM-AGENTS.md`
- **FAQ**: `docs/FAQ.md`
- **Performance Optimization**: `docs/PERFORMANCE-OPTIMIZATION.md`
- **Use Cases**: `docs/USE-CASES.md`

---

**End of Master Prompt**

This prompt contains all necessary information to generate professional, technically accurate articles about the Claude Code Orchestrator Kit for any platform.

**IMPORTANT REMINDERS**:
1. **Always include** "Disclaimer: Expected Pushback" section (fear mixed with arrogance)
2. **Always include** "Contact & Feedback" section at the end (Telegram links, open to criticism/ideas)
3. **Keep author bio brief** (In IT since 2013, last 2 years AI focus, clients prefer AI division)
4. Adapt structure, depth, and tone based on target audience
5. Maintain factual accuracy and avoid hype
