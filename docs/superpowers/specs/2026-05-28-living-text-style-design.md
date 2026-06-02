# Living Text Style — Design Spec

**Date:** 2026-05-28
**Author:** Igor Maslennikov (via Claude brainstorm)
**Status:** Draft (awaiting user approval)
**Trigger:** User found https://github.com/smixs/humanizer-ru and wanted to integrate its
"humanize Russian text" rules into the existing `ai-text-checker` workflow.

---

## 1. Problem

The project has `ai-text-checker` (agent) + `cleanup-ai-noise` (skill) that detect and
clean 28 AI-writing patterns in already-written drafts. It is **reactive**: the article
is generated first, then scrubbed. This means:

- Token cost: full catalog runs on every draft, even when 80% of patterns could have
  been avoided up-front.
- Quality: scrubbing produces "clean but soulless" text. Layer 2 ("restore liveness")
  in the current agent is described in general terms only — no concrete techniques.
- Drift: nothing teaches the LLM-author how to write living text from the start.

`humanizer-ru` offers complementary value:
- A "VOICE & SOUL" block with concrete techniques for live writing (opinions, rhythm,
  complexity, first-person, mess, specific feelings) — exactly what our Layer 2 lacks.
- Канцелярит patterns systematized (nominalizations table, genitive chains, passive→active).
- Hard bans on negative parallelisms and rhetorical questions.

But: `humanizer-ru`'s hard bans on long dash (`—` → `-`) and rhetorical questions
conflict with our platform requirements (Habr/VC use long dash as Russian typographic
standard; rhetorical questions are normal rhetorical devices there).

## 2. Goal

Introduce a **preventive layer** that injects living-writing rules into the LLM-author's
context BEFORE drafting, so the draft comes out living instead of being scrubbed
afterwards. Keep the existing detective layer (`ai-text-checker`) as the safety net for
what slipped through plus platform-specific checks.

Preserve Single Source of Truth: rules live in exactly one file per layer; cross-references
link the two layers so they stay in sync.

## 3. Non-goals

- Do **not** adopt `humanizer-ru`'s hard bans verbatim (long dash, rhetorical questions).
  Adapt them per platform via existing Layer C.
- Do **not** duplicate rules across 8 article-skills. Each rule lives once.
- Do **not** build tooling to auto-sync the two layers. A simple cross-reference
  convention plus a `Maintenance contract` block in both files is enough.
- Do **not** rewrite `cleanup-ai-noise` skill logic. Only its description gets a
  one-line update mentioning the preventive companion.

## 4. Architecture

```
┌─────────────────────────────────┐         ┌────────────────────────────────┐
│  living-text-style/SKILL.md     │ ←─CR──→ │  ai-text-checker.md            │
│  (preventive, ~100 lines)       │         │  (detective, ~440 lines)       │
│                                 │         │                                │
│  • 12 hard "don'ts"             │         │  • Layer A: 32 patterns        │
│  • "Voice & Soul" block         │         │  • Layer B: project stamps     │
│  • Канцелярит table             │         │  • Layer C: per-platform       │
│  • Self-check checklist         │         │  • Edit + backup + report      │
│  • Maintenance contract         │         │  • Maintenance contract        │
└────────────┬────────────────────┘         └──────────────┬─────────────────┘
             │                                             │
             │ invoked by ФАЗА 0.1                         │ invoked by ФАЗА 3
             ↓                                             ↓
        ┌────────────────────────────────────────────────────────┐
        │   article-skill (habr/vc/dzen/pikabu/tenchat/...)      │
        │   = orchestrator that wires both layers into workflow  │
        └────────────────────────────────────────────────────────┘

CR = Cross-Reference (документ-в-документ, без runtime-зависимости)
```

**Single Source of Truth:**
- Preventive rules: `.claude/skills/living-text-style/SKILL.md`
- Detective catalog: `.claude/agents/content/workers/ai-text-checker.md`

**Connection types:**
1. Semantic (1:1 or 1:N mapping). Each `don't` in preventive carries a `↔ A{X}` tag
   pointing to its detective counterpart.
2. Workflow (orchestrator pattern). Article-skills invoke both layers in different
   phases. The skills do not know about each other at runtime.
3. Maintenance ritual. Both files contain a `Maintenance contract` block stating that
   any change on one side requires updating the other and the `↔` tag.

## 5. Components

### 5.1 New file: `.claude/skills/living-text-style/SKILL.md`

**Language convention:** structural/explanatory English; Russian для markers, examples,
tables of replacements, self-check questions, output to the author.

**Sections:**

```markdown
---
name: living-text-style
description: Invoke at ФАЗА 0 of any article-skill BEFORE drafting. Injects 12 hard
don'ts + Voice & Soul techniques + канцелярит replacements into the author's context
so the draft comes out living instead of AI-stamped. Mirror of ai-text-checker
detective rules (cross-referenced).
---

# Living Text Style — Preventive Layer

## When to invoke
ФАЗА 0 of habr-article, vcru-article, dzen-article, pikabu-article, tenchat-article,
telegraph-article, telegram-article, telegram-announcement. BEFORE writing.

## Hard don'ts (top 12 — самые ядовитые AI-маркеры)
| # | Не делай | Почему | ↔ Detector |
|---|----------|--------|------------|
| 1 | «не просто X, а Y» / «не только X, но и Y» | AI-параллелизм | A9 |
| 2 | «является ключевым/важным», «представляет собой» | inflated significance | A1, A8 |
| 3 | «стоит отметить», «важно подчеркнуть», «необходимо учитывать» | filler-frame | A7, A26 |
| 4 | «подчёркивая», «демонстрируя», «способствуя» (деепричастия в хвосте) | participle cliché | A3 |
| 5 | «в современном мире», «в эпоху цифровизации», «в мире/сфере/области X» | template intro | A27, Layer B |
| 6 | «ключевой/важнейший/решающий/поворотный/знаковый» | AI vocabulary | A7 |
| 7 | «будущее выглядит ярко», «впереди захватывающие времена» | template positive ending | A24 |
| 8 | «отличный вопрос», «вы абсолютно правы» | sycophancy | A21 |
| 9 | «надеюсь, это поможет», «дайте знать» | chatbot artifact | A19 |
| 10 | Title Case В Каждом Слове Заголовка | English-style heading | A16 |
| 11 | **Bold** на каждом ключевом слове | bold overuse | A14 |
| 12 | Подряд эмодзи как буллет-маркеры (🚀💡✅) | emoji decoration | A17 |

## Voice & Soul (как добавить голос)
- **Have opinions** — react to facts, don't just report. «Честно, не знаю, как к этому
  относиться» лучше нейтрального списка плюсов и минусов.
- **Vary rhythm** — короткие резкие предложения. Потом длинные, неторопливые. Чередуй.
- **Acknowledge complexity** — «впечатляет, но и тревожит» лучше просто «впечатляет».
- **Use «я»** где уместно — это честнее, не «непрофессиональнее».
- **Leave some mess** — идеальная структура чувствуется алгоритмической. Отступления,
  недооформленные мысли — человеческие.
- **Be specific in feelings** — не «вызывает беспокойство», а «что-то тревожное в
  агентах, работающих в три ночи».

### Example (До → После)
До (sterile): «Эксперимент показал интересные результаты. Агенты сгенерировали 3
миллиона строк кода. Некоторые впечатлены, другие настроены скептически.»
После (alive): «Честно, не знаю, как к этому относиться. 3 миллиона строк кода — пока
люди, видимо, спали. Половина в восторге, половина объясняет, почему это не считается.»

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
| в связи с тем, что | из-за |
| в случае если | если |
| данный | этот |
| осуществлять | делать / проводить |
| в рамках (нелитерально) | (удалить или упростить) |

## Pre-draft self-check (что автор спрашивает у себя)
1. Звучит ли текст естественно вслух?
2. Разнообразен ли ритм предложений (короткие + длинные)?
3. Есть ли конкретика вместо абстракций (цифры, имена, даты)?
4. Есть ли голос (мнение, реакция, ритм, «я»)?
5. Кавычки «ёлочки» (не "лапки")?
6. Заголовки с маленькой буквы (кроме первого слова)?

## Maintenance contract
When adding/removing a don't here, update the matching pattern in
`.claude/agents/content/workers/ai-text-checker.md` (Layer A) and bump the
`↔ Detector` reference column. Drift between preventive and detective layers
degrades the system.

Drift check: every `↔ A{X}` tag here must resolve to an existing pattern ID in
`ai-text-checker.md`. Run `grep '↔ A' SKILL.md` after edits.
```

### 5.2 Updates to `.claude/agents/content/workers/ai-text-checker.md`

**Frontmatter `description`:** add reference to preventive companion.
```
... Mirrors preventive rules in `.claude/skills/living-text-style/SKILL.md`
(cross-referenced via ↔ tags). When patterns change here, update the preventive
counterpart.
```

**Layer A extensions (A29–A32):**

```markdown
**A29. Nominalizations (отглагольные существительные вместо глаголов)**
Symptom: Action frozen into a noun. Bureaucratese inflates "expert" tone.
Markers: `проводить работу`, `осуществлять контроль`, `оказывать помощь`,
`принимать участие`, `вести борьбу`, `производить расчёт`, `давать оценку`,
`совершать ошибку`, `осуществлять предоставление`.
Fix: Use the verb directly.
- `проводить работу` → `работать`
- `осуществлять контроль` → `контролировать`
- `оказывать помощь` → `помогать`
- `осуществлять предоставление услуг` → `оказывать услуги` / `предоставлять`

**A30. Genitive chains (цепочки родительных падежей)**
Symptom: 4+ nouns in genitive case stacked in one phrase — impossible to parse who
relates to whom.
Example marker: `Процесс развития движения за укрепление сотрудничества в области
культуры народов региона`.
Fix: Break into a normal sentence with a verb. `Культурное сотрудничество народов
региона развивается.`

**A31. Passive over active (пассив там, где субъект известен)**
Markers: `было принято решение`, `работа выполняется сотрудниками`, `был обнаружен`,
`будет рассмотрено`.
Fix: Convert to active voice when the subject is known.
- `Решение было принято руководством` → `Руководство решило`
- `Работа выполняется сотрудниками` → `Сотрудники работают`

**A32. Rhetorical questions overuse**
Symptom: More than 2–3 rhetorical questions per article — typical AI imitation of
"engagement". A single rhetorical question is fine; a parade of them is a tell.
Detection: count `?` at end of sentence that is not a literal question to a real
participant.
Fix policy (platform-dependent):
- `habr` / `vc` / `dzen` / `telegraph` / `tenchat`: > 3 per article → flag for
  author. Auto-remove only the most generic ones (e.g. `Не правда ли?`).
- `pikabu` / `telegram`: > 2 per post → auto-remove the weakest; conversational
  format tolerates fewer of them.
- `telegram-announcement`: > 1 → flag.
```

**Renumber the "27 patterns" header to "32 patterns".** Sweep references:
- Frontmatter description: `27 AI-writing signs` → `32 AI-writing signs`.
- Layer A header: `Layer A — 27 patterns` → `Layer A — 32 patterns`.
- Report template row: `A. 27 паттернов (Wikipedia)` → `A. 32 паттерна (Wikipedia + канцелярит)`.

**Layer C updates:**
- `habr` / `vc` / `dzen` / `telegraph` / `tenchat`: add em-dash density rule:
  > 2 em-dashes per paragraph → flag (do **not** auto-replace with `-`).
- `pikabu` / `telegram`: same em-dash flag rule. Rhetorical-question auto-remove
  enabled per A32 policy above.

**Add at the bottom (before `Operating principles`):**

```markdown
## Cross-reference contract

This catalog is the detective layer. Its preventive counterpart lives at
`.claude/skills/living-text-style/SKILL.md`. The two files are intentionally
redundant in opposite directions: preventive teaches what NOT to write; detective
finds and fixes what slipped through.

When changing a pattern here (rename, split, merge, remove), update the
corresponding entry in the preventive file and re-check the `↔ Detector` column
there. Drift between layers degrades the system.
```

### 5.3 Updates to 8 article-skills

For each of `habr-article`, `vcru-article`, `dzen-article`, `pikabu-article`,
`tenchat-article`, `telegraph-article`, `telegram-article`, `telegram-announcement`,
insert at the very start of ФАЗА 0 (before existing content) the following block:

```markdown
### ФАЗА 0.1 — Загрузить правила живого письма

Before any drafting, invoke `Skill('living-text-style')` and keep its rules in
context for ФАЗА 1–2. This is the preventive layer — write right the first time;
the detective layer (`cleanup-ai-noise` in ФАЗА 3) catches what slipped through.

Do not skip this step. Skipping degrades draft quality and inflates ФАЗА 3
cleanup cost.
```

If a particular article-skill already has a `ФАЗА 0` step numbered differently,
adapt the heading to fit local numbering but keep the block content verbatim.

### 5.4 No-changes files

- `.claude/skills/cleanup-ai-noise/SKILL.md`: only the frontmatter `description` gets
  a one-line mention of the preventive companion. Workflow logic stays.

## 6. Drift prevention

The cheapest way to keep two layers in sync without tooling:

1. **Cross-reference tags** (`↔ A{X}`) in every preventive don't.
2. **Maintenance contract** block in both files stating the rule and the grep check.
3. **Optional future linter:** simple shell script that greps `↔ A` tags in
   `living-text-style/SKILL.md` and verifies every ID exists in
   `ai-text-checker.md`. Not required for first iteration.

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Drift between preventive and detective | Cross-reference tags + maintenance contract block; optional future linter. |
| Article-skills forget to invoke `living-text-style` | All 8 updated in one PR, scoped block is identical across skills. |
| Token cost of preventive layer ~100 lines × 8 platforms | Acceptable: preventive runs once per draft, replaces unnecessary detective rewrite cycles. |
| `humanizer-ru` upstream evolves | Spec is a one-time integration of selected ideas, not a sync subscription. Future updates manual. |
| Hard ban on long dash leaks back in | Explicit non-goal documented in Section 3. Layer C flag-only policy. |

## 8. Testing approach

- **Smoke test (preventive):** invoke `Skill('living-text-style')` in isolation; the
  output should be ~100 lines of structured rules, no errors.
- **End-to-end test (one platform):** run `habr-article` with a real topic; verify
  ФАЗА 0.1 loads the preventive rules; verify ФАЗА 3 cleanup-ai-noise finds fewer
  patterns than before (rough comparison against an archived run).
- **Cross-reference validation:** `grep -o '↔ A[0-9]*' living-text-style/SKILL.md`
  must produce only IDs that exist in `ai-text-checker.md`.
- **Platform suite:** sanity-check the ФАЗА 0.1 block in all 8 article-skills via
  `grep -l "Skill('living-text-style')" .claude/skills/*-article/SKILL.md`.

## 9. Out of scope (для следующих итераций)

- Automated drift linter in CI.
- Per-platform variation in the preventive layer. Currently one preventive layer
  serves all platforms; platform-specific tightening stays in Layer C of the
  detective.
- Translating `living-text-style` into a generic English-only writing skill for
  non-Russian content.

## 10. Acceptance criteria

- [ ] `.claude/skills/living-text-style/SKILL.md` exists with all sections from 5.1.
- [ ] `.claude/agents/content/workers/ai-text-checker.md` has A29–A32, updated Layer C,
      Cross-reference contract block, and renumbered references (27→32).
- [ ] All 8 article-skills contain the ФАЗА 0.1 block.
- [ ] `cleanup-ai-noise/SKILL.md` description mentions the preventive companion.
- [ ] Every `↔ A{X}` tag in `living-text-style/SKILL.md` resolves to an existing
      pattern in `ai-text-checker.md`.
- [ ] A trial run on one platform (e.g. `habr-article`) succeeds end-to-end.

---

**Next step after approval:** invoke `writing-plans` skill to break this design
into a 2–5 minute task implementation plan.
