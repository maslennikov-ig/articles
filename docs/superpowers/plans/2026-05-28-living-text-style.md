# Living Text Style Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add preventive writing layer (`living-text-style` skill) and extend detective layer (`ai-text-checker` agent A29–A32 + Layer C policy updates) so the LLM-author writes living text at draft time and the detective only catches what slipped through.

**Architecture:** Two-layer system. Preventive layer = `.claude/skills/living-text-style/SKILL.md`, invoked in ФАЗА 0.1 of each article-skill, injects 12 hard don'ts + Voice & Soul techniques + канцелярит replacement table into author context BEFORE drafting. Detective layer = existing `.claude/agents/content/workers/ai-text-checker.md`, extended with 4 new patterns (nominalizations, genitive chains, passive over active, rhetorical questions) and per-platform policy in Layer C. Cross-reference via `↔ A{X}` tags in both files. `Maintenance contract` block in both files prevents drift without tooling.

**Tech Stack:** Markdown skill/agent definitions; Claude Code Skill tool; Bash for verification (grep, ls).

**Reference spec:** `docs/superpowers/specs/2026-05-28-living-text-style-design.md`

---

## File Structure

**Create:**
- `.claude/skills/living-text-style/SKILL.md` — new preventive skill (~100 lines)

**Modify:**
- `.claude/agents/content/workers/ai-text-checker.md` — A29–A32, Layer C policy, frontmatter description, Layer A header renumber (27→32), report template row, Cross-reference contract block
- `.claude/skills/cleanup-ai-noise/SKILL.md` — one-line addition to frontmatter description
- `.claude/skills/habr-article/SKILL.md` — insert ФАЗА 0.1 block at start of ФАЗА 0
- `.claude/skills/vcru-article/SKILL.md` — same
- `.claude/skills/dzen-article/SKILL.md` — same
- `.claude/skills/pikabu-article/SKILL.md` — same
- `.claude/skills/tenchat-article/SKILL.md` — same
- `.claude/skills/telegraph-article/SKILL.md` — same
- `.claude/skills/telegram-article/SKILL.md` — same
- `.claude/skills/telegram-announcement/SKILL.md` — same

---

### Task 1: Create `living-text-style` skill

**Files:**
- Create: `.claude/skills/living-text-style/SKILL.md`

- [ ] **Step 1: Verify skill does not yet exist**

Run: `ls .claude/skills/living-text-style/ 2>/dev/null && echo "EXISTS" || echo "OK_TO_CREATE"`
Expected: `OK_TO_CREATE`

- [ ] **Step 2: Create directory**

Run: `mkdir -p .claude/skills/living-text-style`
Expected: no output, exit 0.

- [ ] **Step 3: Write `SKILL.md` with full content**

Write to `.claude/skills/living-text-style/SKILL.md`:

````markdown
---
name: living-text-style
description: Invoke at ФАЗА 0 of any article-skill BEFORE drafting (habr-article, vcru-article, dzen-article, pikabu-article, tenchat-article, telegraph-article, telegram-article, telegram-announcement). Injects 12 hard don'ts + Voice & Soul techniques + канцелярит replacement table into the author's context so the draft comes out living instead of AI-stamped. Mirror of `ai-text-checker` detective rules, cross-referenced via ↔ A{X} tags.
---

# Living Text Style — Preventive Layer

This skill is the preventive companion to `ai-text-checker` (detective). The
detective catalogs 32 AI-writing patterns and cleans drafts after the fact.
This skill teaches the author to avoid the worst 12 patterns up-front and to
write with voice instead of producing a sterile, scrub-able text.

## When to invoke

ФАЗА 0 of `habr-article`, `vcru-article`, `dzen-article`, `pikabu-article`,
`tenchat-article`, `telegraph-article`, `telegram-article`,
`telegram-announcement`. BEFORE writing.

Do not skip. Skipping degrades draft quality and inflates ФАЗА 3 cleanup cost.

## Hard don'ts (top 12 — самые ядовитые AI-маркеры)

| # | Не делай | Почему | ↔ Detector |
|---|----------|--------|------------|
| 1 | «не просто X, а Y» / «не только X, но и Y» | AI-параллелизм | A9 |
| 2 | «является ключевым/важным», «представляет собой» | inflated significance | A1, A8 |
| 3 | «стоит отметить», «важно подчеркнуть», «необходимо учитывать» | filler-frame | A7, A26 |
| 4 | «подчёркивая», «демонстрируя», «способствуя» (деепричастия в хвосте) | participle cliché | A3 |
| 5 | «в современном мире», «в эпоху цифровизации», «в мире/сфере/области X» | template intro | A27, Layer B |
| 6 | «ключевой / важнейший / решающий / поворотный / знаковый» | AI vocabulary | A7 |
| 7 | «будущее выглядит ярко», «впереди захватывающие времена» | template positive ending | A24 |
| 8 | «отличный вопрос», «вы абсолютно правы» | sycophancy | A21 |
| 9 | «надеюсь, это поможет», «дайте знать», «конечно!» | chatbot artifact | A19 |
| 10 | Title Case В Каждом Слове Заголовка | English-style heading | A16 |
| 11 | **Bold** на каждом ключевом слове | bold overuse | A14 |
| 12 | Подряд эмодзи как буллет-маркеры (🚀💡✅) | emoji decoration | A17 |

## Voice & Soul (как добавить голос)

A clean text without voice is still obviously AI. After avoiding the 12 don'ts
above, apply these techniques so the result sounds like a living person:

- **Have opinions** — react to facts, don't just report them. «Честно, не знаю,
  как к этому относиться» reads more human than a neutral list of pros and cons.
- **Vary rhythm** — короткие резкие предложения. Потом длинные, неторопливые.
  Чередуй.
- **Acknowledge complexity** — «впечатляет, но и тревожит» лучше просто
  «впечатляет». Mixed feelings are human.
- **Use «я»** где уместно — first person is honest, not unprofessional.
  «Меня не отпускает мысль…», «Вот что меня цепляет…»
- **Leave some mess** — perfect structure feels algorithmic. Asides, inserts,
  half-finished thoughts are human.
- **Be specific in feelings** — not «вызывает беспокойство», but «что-то
  тревожное в агентах, работающих в три ночи».

### Example (До → После)

До (sterile, clean but AI):
> Эксперимент показал интересные результаты. Агенты сгенерировали 3 миллиона
> строк кода. Некоторые разработчики впечатлены, другие настроены скептически.

После (alive):
> Честно, не знаю, как к этому относиться. 3 миллиона строк кода — пока люди,
> видимо, спали. Половина сообщества в восторге, половина объясняет, почему это
> не считается. Правда, наверное, где-то посередине.

## Канцелярит → живой язык (таблица замен)

| Канцелярит | Живой язык |
|------------|------------|
| проводить работу | работать |
| осуществлять контроль | контролировать |
| оказывать помощь | помогать |
| принимать участие | участвовать |
| является эффективным | работает / эффективен |
| представляет собой | это |
| выступает в роли | работает как |
| было принято решение | решили |
| для того чтобы | чтобы |
| в связи с тем, что | из-за того, что / из-за |
| в случае если | если |
| данный (= этот) | этот |
| осуществлять | делать / проводить |
| в рамках (нелитерально) | (удалить или упростить) |
| на данный момент | сейчас |
| в целях X | чтобы X |

## Pre-draft self-check (что автор спрашивает у себя ПЕРЕД сдачей)

1. Звучит ли текст естественно вслух?
2. Разнообразен ли ритм предложений (короткие + длинные)?
3. Есть ли конкретика вместо абстракций (цифры, имена, даты)?
4. Есть ли голос (мнение, реакция, ритм, «я»)?
5. Кавычки «ёлочки» (не "лапки")?
6. Заголовки с маленькой буквы (кроме первого слова)?

## Platform reminders (короткие)

Platform-specific tightening (anglicisms, em-dash density, rhetorical questions)
lives in `ai-text-checker` Layer C. The preventive layer is platform-agnostic:
the 12 don'ts above apply everywhere.

## Maintenance contract

When adding/removing a don't here, update the matching pattern in
`.claude/agents/content/workers/ai-text-checker.md` (Layer A) and bump the
`↔ Detector` reference column. Drift between preventive and detective layers
degrades the system.

Drift check after edits:

```bash
grep -oE '↔ A[0-9]+' .claude/skills/living-text-style/SKILL.md \
  | sort -u | while read ref; do
    id=${ref#↔ }
    grep -q "^\*\*${id}\." .claude/agents/content/workers/ai-text-checker.md \
      || echo "MISSING: $ref"
  done
```

Every `↔ A{X}` tag here must resolve to an existing pattern ID in `ai-text-checker.md`.
````

- [ ] **Step 4: Verify file exists with expected structure**

Run:
```bash
test -f .claude/skills/living-text-style/SKILL.md && \
grep -c '^## ' .claude/skills/living-text-style/SKILL.md
```
Expected: file exists, section count `>= 7` (When to invoke, Hard don'ts, Voice & Soul, Канцелярит, Pre-draft self-check, Platform reminders, Maintenance contract).

- [ ] **Step 5: Verify cross-reference tags can be enumerated**

Run:
```bash
grep -oE '↔ A[0-9]+' .claude/skills/living-text-style/SKILL.md | sort -u
```
Expected output (set):
```
↔ A1
↔ A14
↔ A16
↔ A17
↔ A19
↔ A21
↔ A24
↔ A26
↔ A27
↔ A3
↔ A7
↔ A8
↔ A9
```

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/living-text-style/SKILL.md
git commit -m "feat(skills): add living-text-style preventive layer

12 hard don'ts + Voice & Soul + канцелярит table + self-check.
Mirrors ai-text-checker detective rules via ↔ A{X} cross-references."
```

---

### Task 2: Extend `ai-text-checker` with A29–A32 patterns

**Files:**
- Modify: `.claude/agents/content/workers/ai-text-checker.md` — insert four new patterns after A28

- [ ] **Step 1: Verify A29 does not yet exist**

Run:
```bash
grep -c '^\*\*A29\.' .claude/agents/content/workers/ai-text-checker.md
```
Expected: `0`

- [ ] **Step 2: Read existing A28 block to know exact insertion anchor**

Read `.claude/agents/content/workers/ai-text-checker.md`. Find the end of the A28 section (last line before `### Layer B — Project-specific stamps`). The insertion happens between A28's last paragraph (`Fix policy: auto-replace overkill anglicisms...`) and the `### Layer B` heading.

- [ ] **Step 3: Insert A29–A32 via Edit tool**

Use Edit on `.claude/agents/content/workers/ai-text-checker.md`. Replace:

```
Fix policy: auto-replace overkill anglicisms that have an unambiguous Russian equivalent; flag for the author only when the English term is a borderline-established calque where the choice is stylistic.

### Layer B — Project-specific stamps (extracted from existing article-skills)
```

with:

```
Fix policy: auto-replace overkill anglicisms that have an unambiguous Russian equivalent; flag for the author only when the English term is a borderline-established calque where the choice is stylistic.

**A29. Nominalizations (отглагольные существительные вместо глаголов)**
Symptom: Action frozen into a noun, often via `проводить / осуществлять / оказывать` + noun. Bureaucratese inflates "expert" tone but reads heavy.
Markers: `проводить работу`, `осуществлять контроль`, `оказывать помощь`, `принимать участие`, `вести борьбу`, `производить расчёт`, `давать оценку`, `совершать ошибку`, `осуществлять предоставление`.
Fix: Use the verb directly.
- `проводить работу` → `работать`
- `осуществлять контроль` → `контролировать`
- `оказывать помощь` → `помогать`
- `осуществлять предоставление услуг` → `оказывать услуги` / `предоставлять`

**A30. Genitive chains (цепочки родительных падежей)**
Symptom: 4+ nouns in genitive case stacked in one phrase — impossible to parse who relates to whom.
Example: `Процесс развития движения за укрепление сотрудничества в области культуры народов региона`.
Fix: Break into a normal sentence with a verb. `Культурное сотрудничество народов региона развивается.`
Detection heuristic: 4 or more consecutive nouns in genitive within one nominal phrase → flag (do not auto-rewrite — restructuring depends on author intent).

**A31. Passive over active (пассив там, где субъект известен)**
Markers: `было принято решение`, `работа выполняется сотрудниками`, `был обнаружен`, `будет рассмотрено`, `решение принимается руководством`.
Fix: Convert to active voice when the subject is known.
- `Решение было принято руководством` → `Руководство решило`
- `Работа выполняется сотрудниками` → `Сотрудники работают`
Keep passive when the subject is genuinely unknown or irrelevant (`Здание построено в 1812 году`).

**A32. Rhetorical questions overuse**
Symptom: More than 2–3 rhetorical questions per article — typical AI imitation of "engagement". A single rhetorical question is fine; a parade of them is a tell.
Detection: count `?` at end of sentence where the question is not addressed to a real participant.
Fix policy (platform-dependent — see Layer C below):
- `habr` / `vc` / `dzen` / `telegraph` / `tenchat`: > 3 per article → flag for author. Auto-remove only the most generic ones (e.g. `Не правда ли?`, `Согласны?`).
- `pikabu` / `telegram`: > 2 per post → auto-remove the weakest; conversational format tolerates fewer of them.
- `telegram-announcement`: > 1 → flag.

### Layer B — Project-specific stamps (extracted from existing article-skills)
```

- [ ] **Step 4: Verify A29–A32 now present**

Run:
```bash
for id in A29 A30 A31 A32; do
  grep -c "^\\*\\*${id}\\." .claude/agents/content/workers/ai-text-checker.md
done
```
Expected: four `1`s, one per line.

- [ ] **Step 5: Commit**

```bash
git add .claude/agents/content/workers/ai-text-checker.md
git commit -m "feat(agents): ai-text-checker A29-A32 (канцелярит + риторика)

A29 nominalizations, A30 genitive chains, A31 passive over active,
A32 rhetorical questions overuse. Platform policy in A32 per Layer C."
```

---

### Task 3: Update `ai-text-checker` frontmatter description and Layer A header

**Files:**
- Modify: `.claude/agents/content/workers/ai-text-checker.md`

- [ ] **Step 1: Update frontmatter `description`**

Use Edit on `.claude/agents/content/workers/ai-text-checker.md`. Replace:

```
description: Use proactively for detecting and rewriting AI-generated text patterns in article drafts before publication. Specialist for 27 AI-writing signs (inflated significance, participle clichés, hedging, bureaucratic phrases, em-dash overuse) plus platform-specific checks for Habr/VC/Dzen/Pikabu/Telegraph/TenChat/Telegram. Reads article from .tmp/current/articles/, applies two-layer remediation (remove patterns then restore liveness), saves backup, edits in-place, returns structured diff report with Needs-human-decision items.
```

with:

```
description: Use proactively for detecting and rewriting AI-generated text patterns in article drafts before publication. Specialist for 32 AI-writing signs (inflated significance, participle clichés, hedging, bureaucratic phrases, em-dash overuse, канцелярит, rhetorical questions) plus platform-specific checks for Habr/VC/Dzen/Pikabu/Telegraph/TenChat/Telegram. Reads article from .tmp/current/articles/, applies two-layer remediation (remove patterns then restore liveness), saves backup, edits in-place, returns structured diff report with Needs-human-decision items. Detective companion to preventive skill `living-text-style` (cross-referenced via ↔ A{X} tags).
```

- [ ] **Step 2: Update Layer A header (27 → 32)**

Edit: replace
```
### Layer A — 27 patterns (adapted from Wikipedia "Signs of AI writing", Russian-localized)
```
with
```
### Layer A — 32 patterns (adapted from Wikipedia "Signs of AI writing", Russian-localized, extended with канцелярит and rhetoric)
```

- [ ] **Step 3: Update report template row (27 → 32)**

Edit: replace
```
| A. 27 паттернов (Wikipedia) | {N} | {N} | {N} |
```
with
```
| A. 32 паттерна (Wikipedia + канцелярит + риторика) | {N} | {N} | {N} |
```

- [ ] **Step 4: Verify no stale "27" references remain in catalog context**

Run:
```bash
grep -nE '27 patterns|27 паттерн|27 AI' .claude/agents/content/workers/ai-text-checker.md
```
Expected: no output (exit code 1). If any line matches, edit it manually.

- [ ] **Step 5: Commit**

```bash
git add .claude/agents/content/workers/ai-text-checker.md
git commit -m "chore(agents): renumber ai-text-checker catalog 27 → 32

Frontmatter, Layer A header, and report template row updated to
reflect A29-A32 additions. Mention preventive companion in description."
```

---

### Task 4: Update Layer C in `ai-text-checker` for em-dash density and rhetorical questions

**Files:**
- Modify: `.claude/agents/content/workers/ai-text-checker.md`

- [ ] **Step 1: Edit `habr` Layer C block — add em-dash and rhetoric rules**

Use Edit. Replace the entire `habr` block:
```
**`habr`** — Habr trust & verification (extracted from habr-article skill):
- Unverifiable company metrics (team size, ROI, %s without evidence) → flag for author
- Habr's "каша из топора" pattern: results attributed to AI when significant human work was involved → flag
- Citing AI-CEO (Amodei, Shumer) as neutral expert without bias disclosure → flag
- "Кодер" used interchangeably with "инженер" / "разработчик" → suggest distinction
- Hidden marketing of own services without proportional reader value → flag
- Position AGAINST community ("программисты не нужны") — even if unintended → flag
```

with:
```
**`habr`** — Habr trust & verification (extracted from habr-article skill):
- Unverifiable company metrics (team size, ROI, %s without evidence) → flag for author
- Habr's "каша из топора" pattern: results attributed to AI when significant human work was involved → flag
- Citing AI-CEO (Amodei, Shumer) as neutral expert without bias disclosure → flag
- "Кодер" used interchangeably with "инженер" / "разработчик" → suggest distinction
- Hidden marketing of own services without proportional reader value → flag
- Position AGAINST community ("программисты не нужны") — even if unintended → flag
- Em-dash density: > 2 em-dashes per paragraph → flag (NEVER auto-replace `—` with `-`; em-dash is the Russian typographic standard on Habr)
- Rhetorical questions: > 3 per article → flag (A32)
```

- [ ] **Step 2: Edit `vc` Layer C block — add em-dash and rhetoric rules**

Use Edit. Replace:
```
**`vc`** — VC.ru:
- ROI / growth claims without methodology → flag
- Missing critique of limitations / alternatives → flag
- Marketing tone without business substance → flag
```
with:
```
**`vc`** — VC.ru:
- ROI / growth claims without methodology → flag
- Missing critique of limitations / alternatives → flag
- Marketing tone without business substance → flag
- Em-dash density: > 2 em-dashes per paragraph → flag (do NOT auto-replace; em-dash is Russian standard)
- Rhetorical questions: > 3 per article → flag (A32)
```

- [ ] **Step 3: Edit `dzen` Layer C block — add em-dash and rhetoric rules**

Use Edit. Replace:
```
**`dzen`** — Yandex Dzen:
- Faceless intro that risks completion-rate drop in first 2 paragraphs → flag
- Missing first-paragraph hook → flag
- Information density too low for the algorithm → flag
- Anglicisms (A28) — STRICT: broad audience; translate jargon with a clear equivalent
```
with:
```
**`dzen`** — Yandex Dzen:
- Faceless intro that risks completion-rate drop in first 2 paragraphs → flag
- Missing first-paragraph hook → flag
- Information density too low for the algorithm → flag
- Anglicisms (A28) — STRICT: broad audience; translate jargon with a clear equivalent
- Em-dash density: > 2 em-dashes per paragraph → flag (do NOT auto-replace)
- Rhetorical questions: > 3 per article → flag (A32)
```

- [ ] **Step 4: Edit `pikabu` Layer C block — add em-dash density flag and stricter rhetoric policy**

Use Edit. Replace:
```
**`pikabu`** — Pikabu:
- Symmetric / predictable rhythm ("dead intros") → flag
- Missing self-irony or character → flag
- Elitist tone → flag
- Anglicisms (A28) — STRICT: translate everything except proper nouns / unavoidable abbreviations
```
with:
```
**`pikabu`** — Pikabu:
- Symmetric / predictable rhythm ("dead intros") → flag
- Missing self-irony or character → flag
- Elitist tone → flag
- Anglicisms (A28) — STRICT: translate everything except proper nouns / unavoidable abbreviations
- Em-dash density: > 2 em-dashes per paragraph → flag (do NOT auto-replace)
- Rhetorical questions: > 2 per post → auto-remove the weakest (A32 — conversational format tolerates fewer)
```

- [ ] **Step 5: Edit `telegraph` Layer C block — add em-dash and rhetoric rules**

Use Edit. Replace:
```
**`telegraph`** — Telegraph (Telegram long-form):
- 70/30 prose-to-format ratio violated (stricter than the 60/40 default) → flag
- Long unbroken paragraphs that hurt mobile readability → flag
```
with:
```
**`telegraph`** — Telegraph (Telegram long-form):
- 70/30 prose-to-format ratio violated (stricter than the 60/40 default) → flag
- Long unbroken paragraphs that hurt mobile readability → flag
- Em-dash density: > 2 em-dashes per paragraph → flag (do NOT auto-replace)
- Rhetorical questions: > 3 per article → flag (A32)
```

- [ ] **Step 6: Edit `tenchat` Layer C block — add em-dash and rhetoric rules**

Use Edit. Replace:
```
**`tenchat`** — TenChat (B2B):
- Missing real business context (Zeus algorithm needs concreteness) → flag
- Profile / positioning gaps → flag
- Anglicisms (A28) — STRICT: business audience prefers Russian; translate jargon with a clear equivalent
```
with:
```
**`tenchat`** — TenChat (B2B):
- Missing real business context (Zeus algorithm needs concreteness) → flag
- Profile / positioning gaps → flag
- Anglicisms (A28) — STRICT: business audience prefers Russian; translate jargon with a clear equivalent
- Em-dash density: > 2 em-dashes per paragraph → flag (do NOT auto-replace)
- Rhetorical questions: > 3 per article → flag (A32)
```

- [ ] **Step 7: Edit `telegram` Layer C block — add em-dash density flag and stricter rhetoric**

Use Edit. Replace:
```
**`telegram`** — Telegram short posts:
- Missing personal detail (at least one per post) → flag
- Marketing tone instead of conversational → flag
- Repeated CTA / signature phrasing across posts → flag
```
with:
```
**`telegram`** — Telegram short posts:
- Missing personal detail (at least one per post) → flag
- Marketing tone instead of conversational → flag
- Repeated CTA / signature phrasing across posts → flag
- Em-dash density: > 2 em-dashes per paragraph → flag (do NOT auto-replace)
- Rhetorical questions: > 2 per post → auto-remove the weakest (A32 — conversational format)
```

- [ ] **Step 8: Edit `telegram-announcement` Layer C block — add rhetoric rule**

Use Edit. Replace:
```
**`telegram-announcement`** — Telegram article announcements:
- Retelling the source article instead of providing a hook → flag
- Missing original-platform context → flag
```
with:
```
**`telegram-announcement`** — Telegram article announcements:
- Retelling the source article instead of providing a hook → flag
- Missing original-platform context → flag
- Rhetorical questions: > 1 → flag (A32 — short format, one is the maximum)
```

- [ ] **Step 9: Verify Layer C updates landed**

Run:
```bash
grep -c 'Em-dash density' .claude/agents/content/workers/ai-text-checker.md
grep -c 'Rhetorical questions:' .claude/agents/content/workers/ai-text-checker.md
```
Expected: `7` (em-dash mentioned in 7 platform blocks — all except telegram-announcement) and `8` (rhetoric mentioned in all 8 platform blocks).

- [ ] **Step 10: Commit**

```bash
git add .claude/agents/content/workers/ai-text-checker.md
git commit -m "feat(agents): Layer C em-dash density + rhetoric policy per platform

Em-dash density flag-only across all platforms (long dash is Russian standard).
Rhetorical questions thresholds per platform (A32): strict on
conversational (pikabu/telegram, auto-remove >2), relaxed flag on
long-form (habr/vc/dzen/telegraph/tenchat, >3)."
```

---

### Task 5: Add Cross-reference contract block to `ai-text-checker`

**Files:**
- Modify: `.claude/agents/content/workers/ai-text-checker.md`

- [ ] **Step 1: Verify the block does not yet exist**

Run:
```bash
grep -c '^## Cross-reference contract' .claude/agents/content/workers/ai-text-checker.md
```
Expected: `0`

- [ ] **Step 2: Insert Cross-reference contract block before Operating principles**

Use Edit. Replace:
```
## Operating principles (summary)
```
with:
```
## Cross-reference contract

This catalog is the detective layer. Its preventive counterpart lives at
`.claude/skills/living-text-style/SKILL.md`. The two files are intentionally
redundant in opposite directions: preventive teaches what NOT to write;
detective finds and fixes what slipped through.

When changing a pattern here (rename, split, merge, remove), update the
corresponding entry in the preventive file and re-check the `↔ Detector`
column there. Drift between layers degrades the system.

Drift check after edits:

```bash
grep -oE '↔ A[0-9]+' .claude/skills/living-text-style/SKILL.md \
  | sort -u | while read ref; do
    id=${ref#↔ }
    grep -q "^\*\*${id}\." .claude/agents/content/workers/ai-text-checker.md \
      || echo "MISSING: $ref"
  done
```

Every `↔ A{X}` tag in the preventive file must resolve to a pattern ID here.

---

## Operating principles (summary)
```

- [ ] **Step 3: Verify block landed and drift check produces no output**

Run:
```bash
grep -c '^## Cross-reference contract' .claude/agents/content/workers/ai-text-checker.md
```
Expected: `1`

Then run the drift check itself:
```bash
grep -oE '↔ A[0-9]+' .claude/skills/living-text-style/SKILL.md \
  | sort -u | while read ref; do
    id=${ref#↔ }
    grep -q "^\*\*${id}\." .claude/agents/content/workers/ai-text-checker.md \
      || echo "MISSING: $ref"
  done
```
Expected: no `MISSING:` lines.

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/content/workers/ai-text-checker.md
git commit -m "docs(agents): ai-text-checker cross-reference contract with living-text-style

Explicit drift-check ritual + grep snippet. No tooling required —
maintenance is manual whenever either catalog changes."
```

---

### Task 6: Update `cleanup-ai-noise` description

**Files:**
- Modify: `.claude/skills/cleanup-ai-noise/SKILL.md`

- [ ] **Step 1: Update frontmatter description**

Use Edit. Replace:
```
description: Use at the end of any article-writing skill (habr-article, vcru-article, dzen-article, pikabu-article, telegraph-article, tenchat-article, telegram-article, telegram-announcement) before publication. Saves the draft to .tmp/current/articles/, invokes the ai-text-checker agent with platform context, presents the cleanup report and Needs-human-decision items to the author.
```
with:
```
description: Use at the end of any article-writing skill (habr-article, vcru-article, dzen-article, pikabu-article, telegraph-article, tenchat-article, telegram-article, telegram-announcement) before publication. Saves the draft to .tmp/current/articles/, invokes the ai-text-checker agent with platform context, presents the cleanup report and Needs-human-decision items to the author. Detective companion to the preventive skill `living-text-style` (invoked at ФАЗА 0 before drafting).
```

- [ ] **Step 2: Verify edit landed**

Run:
```bash
grep -c 'living-text-style' .claude/skills/cleanup-ai-noise/SKILL.md
```
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/cleanup-ai-noise/SKILL.md
git commit -m "docs(skills): cleanup-ai-noise mentions preventive companion"
```

---

### Task 7: Insert ФАЗА 0.1 block into all 8 article-skills

**Files:**
- Modify (each): `.claude/skills/habr-article/SKILL.md`, `vcru-article/SKILL.md`, `dzen-article/SKILL.md`, `pikabu-article/SKILL.md`, `tenchat-article/SKILL.md`, `telegraph-article/SKILL.md`, `telegram-article/SKILL.md`, `telegram-announcement/SKILL.md`

The standard block to insert at the start of ФАЗА 0 (BEFORE its existing content):

```markdown
### ФАЗА 0.1 — Загрузить правила живого письма

Before any drafting, invoke `Skill('living-text-style')` and keep its rules in
context for ФАЗА 1–2. This is the preventive layer — write right the first time;
the detective layer (`cleanup-ai-noise` in ФАЗА 3) catches what slipped through.

Do not skip this step. Skipping degrades draft quality and inflates ФАЗА 3
cleanup cost.
```

For each of the 8 skills, perform the steps below. If a skill's local ФАЗА numbering uses different headings (e.g., `## ФАЗА 0` vs `### Phase 0`), adapt the heading style to match the surrounding file but keep the block body verbatim.

- [ ] **Step 1: Verify none of the 8 skills already contain the marker**

Run:
```bash
grep -l "Skill('living-text-style')" \
  .claude/skills/habr-article/SKILL.md \
  .claude/skills/vcru-article/SKILL.md \
  .claude/skills/dzen-article/SKILL.md \
  .claude/skills/pikabu-article/SKILL.md \
  .claude/skills/tenchat-article/SKILL.md \
  .claude/skills/telegraph-article/SKILL.md \
  .claude/skills/telegram-article/SKILL.md \
  .claude/skills/telegram-announcement/SKILL.md \
  2>/dev/null
```
Expected: no output. If any file already contains the marker, skip that file in the inserts below.

**Standard insertion procedure (used by Steps 2–9 below):**

1. Read the target SKILL.md file fully.
2. Locate the first ФАЗА 0 heading (search pattern `ФАЗА 0` near the top — usually `## ФАЗА 0 — …` or `### ФАЗА 0 — …`). Capture the local heading style (`##` vs `###`) — match it in the inserted heading.
3. Identify the heading line + the next 1–2 lines of body content. This becomes the unique anchor.
4. Use the `Edit` tool with `old_string` = the heading line + the next 1–2 lines verbatim, and `new_string` = the same content + a blank line + the standard ФАЗА 0.1 block above (adjust the `###` of the ФАЗА 0.1 heading to match local style).
5. If the file uses `##` for ФАЗА headings, change `### ФАЗА 0.1` → `## ФАЗА 0.1` in the inserted block.

- [ ] **Step 2: Insert into `habr-article/SKILL.md`**

Apply the Standard insertion procedure above to `.claude/skills/habr-article/SKILL.md`.

- [ ] **Step 3: Insert into `vcru-article/SKILL.md`**

Apply the Standard insertion procedure above to `.claude/skills/vcru-article/SKILL.md`.

- [ ] **Step 4: Insert into `dzen-article/SKILL.md`**

Apply the Standard insertion procedure above to `.claude/skills/dzen-article/SKILL.md`.

- [ ] **Step 5: Insert into `pikabu-article/SKILL.md`**

Apply the Standard insertion procedure above to `.claude/skills/pikabu-article/SKILL.md`.

- [ ] **Step 6: Insert into `tenchat-article/SKILL.md`**

Apply the Standard insertion procedure above to `.claude/skills/tenchat-article/SKILL.md`.

- [ ] **Step 7: Insert into `telegraph-article/SKILL.md`**

Apply the Standard insertion procedure above to `.claude/skills/telegraph-article/SKILL.md`.

- [ ] **Step 8: Insert into `telegram-article/SKILL.md`**

Apply the Standard insertion procedure above to `.claude/skills/telegram-article/SKILL.md`.

- [ ] **Step 9: Insert into `telegram-announcement/SKILL.md`**

Apply the Standard insertion procedure above to `.claude/skills/telegram-announcement/SKILL.md`.

- [ ] **Step 10: Verify all 8 skills now contain the marker**

Run:
```bash
grep -lc "Skill('living-text-style')" \
  .claude/skills/habr-article/SKILL.md \
  .claude/skills/vcru-article/SKILL.md \
  .claude/skills/dzen-article/SKILL.md \
  .claude/skills/pikabu-article/SKILL.md \
  .claude/skills/tenchat-article/SKILL.md \
  .claude/skills/telegraph-article/SKILL.md \
  .claude/skills/telegram-article/SKILL.md \
  .claude/skills/telegram-announcement/SKILL.md
```
Expected: each file reports `1` (one match per file). If any file reports `0`, redo its insertion.

- [ ] **Step 11: Verify ФАЗА 0.1 heading present everywhere**

Run:
```bash
grep -c 'ФАЗА 0.1 — Загрузить правила живого письма' \
  .claude/skills/habr-article/SKILL.md \
  .claude/skills/vcru-article/SKILL.md \
  .claude/skills/dzen-article/SKILL.md \
  .claude/skills/pikabu-article/SKILL.md \
  .claude/skills/tenchat-article/SKILL.md \
  .claude/skills/telegraph-article/SKILL.md \
  .claude/skills/telegram-article/SKILL.md \
  .claude/skills/telegram-announcement/SKILL.md
```
Expected: each file reports `1`.

- [ ] **Step 12: Commit**

```bash
git add .claude/skills/habr-article/SKILL.md \
        .claude/skills/vcru-article/SKILL.md \
        .claude/skills/dzen-article/SKILL.md \
        .claude/skills/pikabu-article/SKILL.md \
        .claude/skills/tenchat-article/SKILL.md \
        .claude/skills/telegraph-article/SKILL.md \
        .claude/skills/telegram-article/SKILL.md \
        .claude/skills/telegram-announcement/SKILL.md
git commit -m "feat(skills): article-skills invoke living-text-style at ФАЗА 0.1

All 8 platforms (habr/vc/dzen/pikabu/tenchat/telegraph/telegram/announcement)
now load preventive rules before drafting. Detective layer in ФАЗА 3
still handles cleanup of what slipped through."
```

---

### Task 8: End-to-end validation

**Files:** none (validation only)

- [ ] **Step 1: Drift check**

Run:
```bash
grep -oE '↔ A[0-9]+' .claude/skills/living-text-style/SKILL.md \
  | sort -u | while read ref; do
    id=${ref#↔ }
    grep -q "^\*\*${id}\." .claude/agents/content/workers/ai-text-checker.md \
      || echo "MISSING: $ref"
  done
```
Expected: no `MISSING:` output.

- [ ] **Step 2: Catalog count check**

Run:
```bash
grep -cE '^\*\*A[0-9]+\.' .claude/agents/content/workers/ai-text-checker.md
```
Expected: `32`.

- [ ] **Step 3: All article-skills wired check**

Run:
```bash
count=$(grep -l "Skill('living-text-style')" .claude/skills/*-article/SKILL.md .claude/skills/telegram-announcement/SKILL.md 2>/dev/null | wc -l)
echo "$count of 8 skills wired"
test "$count" = "8" && echo "OK"
```
Expected: `8 of 8 skills wired` then `OK`.

- [ ] **Step 4: No stale "27 patterns" references in ai-text-checker**

Run:
```bash
grep -nE '27 (patterns|паттерн|AI)' .claude/agents/content/workers/ai-text-checker.md
```
Expected: no output (exit 1).

- [ ] **Step 5: Smoke-load preventive skill in isolation**

In a fresh Claude Code session, invoke `Skill('living-text-style')` directly. The skill should load and surface the 12 don'ts + Voice & Soul + канцерярит table. No error.

(This is a manual verification step. Record the result in the commit if you proceed to the final commit.)

- [ ] **Step 6: No commit for this task** — validation only. If any of Steps 1–4 failed, return to the relevant earlier task and re-execute its fix steps.

---

## Out of plan (next iteration)

- CI linter for cross-reference drift (Bash + GitHub Action).
- Per-platform variation of the preventive layer (currently one-size-fits-all).
- End-to-end test: run an actual `habr-article` flow against a known prompt,
  compare ФАЗА 3 cleanup-ai-noise statistics against an archived pre-change run.
