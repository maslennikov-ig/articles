# Evidence-Graded Briefing: Suppressing Unsourced Product-Fact Assertions in a Production LLM Sales Assistant Without Degrading It Into a Hedging/Refusing Bot

_Compiled 5 August 2026. Context: B2B office-furniture sales assistant (WhatsApp/Telegram; EN/AR/RU), tool-calling over catalog + CRM + quotation generator; three observed failure modes — (a) asserting free-text attributes absent from retrieved rows, (b) invoking the quotation tool after the customer declined, (c) an LLM judge penalising a labelled assumption while missing a vaguer unsourced claim. Source labels: **[PE]** practitioner-experience, **[AC]** academic, **[VM]** vendor-marketing, **[UN]** unverified/likely-AI-generated._

**Sourcing honesty note (read first).** The brief ranked Reddit (r/LLMDevs, r/AI_Agents, r/MachineLearning, r/LocalLLaMA, r/ExperiencedDevs) and Hacker News as the highest-priority sources. Hacker News was reachable only in part: item pages returned HTTP 429 rate-limits on most attempts, and only one thread (id=41541053, "LLMs Will Always Hallucinate") was fully retrievable with verbatim comments; two others yielded only the OP or top comment, and one (id=44654135) is a deleted item with no discussion. **Reddit was entirely unreachable this session** across direct, old.reddit, and search-engine paths. Per the brief, where a Reddit practitioner thread is specifically required I mark it **"no substantive Reddit evidence found (source unreachable, not absent)"** rather than substitute a vendor blog. The remaining evidence base skews academic and vendor; this is flagged in Q2 and the Stop note. Verbatim HN comments are quoted in Q3 and Q8.

---

### Q1 — Approaches used in production 2024–2026

**Per-claim citation / provenance (mechanical).** Require the model to cite the retrieved span (catalog row id or `[file:start-end]`) for each asserted attribute; a deterministic post-step checks the cited interval actually overlaps retrieved context (interval arithmetic rather than trusting the model). Position: post-generation, pre-send. **ELIMINATES** a class only when verification is mechanical. Limit: models "postrationalize" — attaching superficially related passages they did not rely on — so citation presence ≠ grounding (arXiv 2512.12117; 2603.19532). [AC]

**Structured "fields I relied on" + code verification.** Model emits structured output (schema / tool-call args) naming the catalog fields used; code verifies each value against the tool row. Position: generation-time + post-step. **ELIMINATES** numeric/enumerable errors "by construction" when the answer has a known shape (schema, enum, valid SKU set) — exactly what the requester already does for numbers/SKUs/prices/stock. Limit: free-text attributes ("breathable mesh back") are not enumerable, so this does not cover failure mode (a). [AC/VM]

**State-machine tool gating.** An allowlist hides tools in certain states. Position: request path, pre-model. **ELIMINATES** illegal tool invocation *if the state transition is correct* — the direct fix for failure mode (b). Academic support: allowing users to "specify which strings are acceptable in specific states" can eliminate certain hallucination classes (arXiv 2406.02630). Limit: gating is only as good as state detection; the observed (b) failure — saying "I won't prepare one" while calling the quote tool — indicates the state machine did not transition on the decline. [AC]

**Second-pass groundedness checking.** A separate check (LLM judge, NLI model, or trained verifier) scores whether each sentence is supported; unsupported spans are regenerated or flagged. Position: post-generation. **DETECTS only** — a filter with false negatives/positives. Vendor implementations: Amazon Bedrock Guardrails contextual grounding checks, Datadog Agent Observability hallucination detection, NeMo Guardrails fact-checking rails. [VM]

**Ensemble / disagreement checking.** Sample multiple generations; inconsistency flags fabrication (SelfCheckGPT). Position: post-generation. **DETECTS only**; costs n× inference. Weak fit here because the catalog *is* the source. [AC]

**Knowledge-graph verification.** Verify entities/relations against a graph or triplet store; post-process with knowledge triplets or dual-decoder guided generation (arXiv 2411.07870). Can **ELIMINATE** entity-level errors when the graph is complete. Limit: requires a maintained graph — overkill for a flat product catalog. [AC]

**Constrained decoding.** Grammar/schema-constrained token generation (Outlines, jsonformer, llm-structured-output). Generation-time; **ELIMINATES** malformed/out-of-enum output by construction. Limit: cannot make a free-text claim *true* — only constrains form. [AC/PE]

**Fine-tuning for abstention.** Train/prompt the model to say "I don't know" under uncertainty (conformal abstention, `[IDK]` token, RLVR abstention reward). Reduces fabrication with a tunable accuracy↔abstention tradeoff (arXiv 2405.01563; 2404.10960). Limit: over-abstention is the over-refusal failure of Q3. [AC]

**Confidence: medium** — because mechanisms and their eliminate-vs-detect character are well documented across arXiv and vendor docs, but almost none is measured on a furniture-catalog / free-text-attribute setting.

---

### Q2 — Quantitative evidence

- **Baseline RAG hallucination rate.** Verbatim from Auto-GDA (arXiv 2410.03461, 2024): "even when modern LLMs are used with RAG, hallucination rates of 15% - 30% (Chen et al., 2023a) or more than one hallucination per 100 output tokens can occur (Niu et al., 2024)." [AC, measured]
- **Legal-citation grounding:** 13–21% of generated citations hallucinated across five systems; best RAG-augmented system CG=0.873 (arXiv 2606.00898). [AC, measured]
- **BBC/EBU news studies.** The BBC's February 2025 study (ChatGPT, Copilot, Gemini, Perplexity; 100 BBC articles) found "51 percent of all AI answers to questions about the news were judged to have significant issues," "19% of AI answers which cited BBC content introduced factual errors," and "13% of the quotes sourced from BBC articles were either altered … or didn't actually exist in that article." The follow-on EBU/BBC "News Integrity in AI Assistants" study (21 Oct 2025; 22 public-media organisations, 18 countries, 14 languages, >3,000 responses) found "45% of all AI answers had at least one significant issue," 20% had "major accuracy problems," with Gemini worst at 76%. [AC/PE, measured]
- **Cheap verifier:** MiniCheck (Tang, Laban & Durrett, EMNLP 2024, arXiv 2404.10774): "we show how to build small fact-checking models that have GPT-4-level performance but for 400x lower cost … Our best system MiniCheck-FT5 (770M parameters) outperforms all systems of comparable size and reaches GPT-4 accuracy" on the LLM-AggreFact benchmark. [AC, measured]
- **SelfCheckGPT cost:** n× inference (6× API calls at 5 samples); ~$20 (ChatGPT) vs ~$200 (GPT-3) to check 1,908 sentences × 20 samples (arXiv 2303.08896). [AC, measured]
- **Over-refusal is measurable:** OR-Bench (80,000 prompts, ~1,000 hard; arXiv 2405.20947) and FalseReject (16k queries, 29 SOTA models; arXiv 2505.08054) both show over-refusal persists across all tested models. Caveat: these measure *safety* refusals, not groundedness refusals. [AC, measured]
- **Practitioner throughput (anecdotal):** a Fortune-500 RAG chatbot builder reports "90% five-star user approval internally," 50M+ records, 10–30s latency (HN Ask HN, id=43420170, Mar 2025) [PE]; an RB2B practitioner reports "AI handles 74.8% of support tickets" after guardrail design (robbclarke.substack.com) [PE].
- **Added latency / cost-per-message / engineering effort for a groundedness second pass in this kind of assistant: no substantive evidence found** with directly comparable measured numbers; vendors assert "real-time" but publish no per-message figures for a catalog agent.

**Confidence: medium** — rate ranges and verifier-cost ratios are peer-reviewed, but per-message latency/cost/effort for the specific deployment are absent and operational numbers are single-team anecdotes.

---

### Q3 — The over-constraint problem

Evidence that guards degrade assistants exists, but **mostly in the safety-refusal literature, not the groundedness-refusal literature** — a distinction the brief's situation sits inside.

- OR-Bench documents "a crucial trade-off: most models achieve safety … at the expense of over-refusal, rarely excelling in both" (arXiv 2405.20947). [AC]
- Tuan et al. (cited in arXiv 2512.01037) show "prioritizing safety can significantly depress user engagement and perceived helpfulness." [AC]
- The RAG-trustworthiness paper formalises the two symmetric failures we care about — **"Over-Responsiveness"** (answering when it should refuse) and **"Excessive Refusal"** (refusing an answerable question) — as distinct hallucination types (arXiv 2409.11242). This is the cleanest framework for measuring both halves. [AC]
- Practitioner evidence of degradation is direct. One DEV author deliberately disables grounding guards: "This allows us to explicitly turn off hallucination guard rails, such that if the context doesn't explicitly provide an answer, GPT4's base knowledge will take over" (polterguy, dev.to). [PE] A Register-forum commenter names the inverse failure — anti-refusal prompting causing fabrication: "Throw that question at a bot told to never say it doesn't know the answer and to pick the most likely result, you'll often get the answer yes" (doublelayer, forums.theregister.com, Apr 2025). [PE]

Detection/measurement: false-refusal eval sets (OR-Bench, FalseReject, XSTest, OKTest, PHTest) plus in-house "answerable-but-refused" counts and the RAG paper's Excessive-Refusal metric. **Commercial impact from a named company running a sales assistant (conversion/CSAT delta): no substantive evidence found** — the degradation direction is asserted but not quantified for a selling context.

**Confidence: medium** — the trade-off is robust for safety refusals and a clean two-sided metric exists, but groundedness-specific over-refusal degradation and its commercial impact in sales are only anecdotal.

---

### Q4 — The labelled-assumption pattern

This is a **well-established *sales* practice** but has **no established *LLM-eval* practice** that scores it correctly as distinct from hedging.

- **Sales methodology:** the assumptive/presumptive close explicitly teaches stating an assumption and moving to a confirming question ("Would you like me to arrange delivery on Monday?") instead of asking whether the customer wants to buy (sellingsignals.com; socoselling.com; Indeed). The **two-step assumptive close** pairs a value statement with an assumption-laden confirming question. [VM/PE] **Dissent shown, not averaged:** for complex B2B deals, SPIN-selling sources argue "traditional closing techniques — trial closes, assumptive closes, urgency plays — actually hurt win rates" (prospeo.io). So the pattern is endorsed for transactional selling and contested for complex, multi-stakeholder deals.
- **Agent-UX / prompt-framework documentation of "state a visible assumption then confirm" as a hallucination-avoidance move (vs a sales-closing move): no substantive evidence found.** The nearest literature is abstention / "ask a clarifying question," which does not treat a *labelled* assumption as a first-class scored category.
- **Distinguishing a labelled assumption from a hedge in evaluation: no substantive evidence found.** This is precisely failure mode (c): no rubric located separates "visible, falsifiable assumption offered for confirmation" from "vague unsourced hedge."
- **Customer response to an *AI* stating a labelled assumption in a selling context: no substantive evidence found** — assumptive-close efficacy is asserted by trainers for human sellers only.

**Confidence: low** — the sales-side pattern is well documented; the LLM-evaluation side has no substantive evidence.

---

### Q5 — Verifier reliability (a second LLM checking the first)

Evidence is mixed, and the brief's instinct — a narrow "is this sentence supported by this passage" task — is supported.

**For.** LLM judges reach high human agreement on well-scoped binary tasks: 2026 arXiv appendices report Cohen's κ 0.72–0.90 and 86–95% agreement with humans for narrow support/deception/grounding judgments (κ=0.85 / 92.3%, D3-Gym; κ=0.72 / 86%, DolusChat; 92.67% accuracy, AMA-Bench). A narrow trained verifier is both cheaper and competitive: MiniCheck (arXiv 2404.10774) shows "GPT-4-level performance but for 400x lower cost," with MiniCheck-FT5 (770M) reaching GPT-4 accuracy on LLM-AggreFact (a benchmark unifying ~10 datasets with sentence-level human-annotated errors). NLI/entailment verification targets grounding "directly, which is the right objective" (arXiv 2607.04223).

**Against / failure modes.** Judges show position, verbosity, and self-enhancement biases and run-to-run inconsistency (survey: arXiv 2508.18076, "Neither Valid nor Reliable?"). "No Free Labels" (arXiv 2503.05061) finds judges agree with experts "only on questions the judges were able to correctly answer themselves" — a critical limit for a judge over specialist furniture attributes. MT-Bench's ~80% human agreement is single-turn; on multi-turn dialogue it drops to ~65% (vadim.blog, practitioner summary). In a legal-QA groundedness benchmark, "complex prompt chaining approaches like RefChecker and SelfCheckGPT underperformed"; similarity methods were fast but weak; NLI improved accuracy at higher latency; on-corpus fine-tuning helped most (arXiv 2410.08764) — **direct evidence that a narrow, fine-tuned sentence-support verifier beats holistic and elaborate chained scoring**, matching failure mode (c).

**Comparison.** SelfCheck-style sampling works with no source but costs n× and can "amplify early errors" as a blanket policy (arXiv 2510.21557); NLI/entailment is cheaper and source-anchored but "brittle over long, multi-sentence context" (arXiv 2607.04223); mechanical/retrieval verification eliminates rather than scores; conformal/uncertainty methods bound error rates theoretically (arXiv 2405.01563). **Model-size/cost tradeoff:** a 770M fine-tuned checker (MiniCheck) or a DeBERTa-v3-large NLI model is far cheaper than a frontier judge and often more reliable on the narrow task.

**Confidence: medium-high** — supporting agreement numbers, failure modes, and the narrow-beats-holistic finding are all documented; the gap is that none is on furniture attributes.

---

### Q6 — Data prerequisite (catalog / PIM attribute completeness)

- PIM vendors treat **completeness scoring** (percent of required attributes filled) as a core metric with published **thresholds of 90–95%** and batch-drop alerts (Pimberly; Bluestone PIM; WISEPIM; Nanopim). One source notes aggregate completeness of ~92% can mask localized-variant completeness of ~65% (Nanopim) — highly relevant to an EN/AR/RU trilingual catalog, where the Arabic/Russian attribute fields are the likely thin spots and thus the likely source of failure mode (a). [VM]
- Completeness↔conversion link: vendors claim complete attribute sets "convert at rates 30–50% higher" than thin listings (odoopim.com) — **vendor-claimed, treat with caution.** [VM]
- **Whether guarding is reported ineffective below a completeness threshold: no substantive evidence found.** The mechanism is plausible (a strict guard on a sparse catalog forces refusal/abstention on most attribute questions) but I found no measured study naming a floor.
- **Attributes that genuinely do not exist in the catalog:** the honest answer is abstention — "not specified" (arXiv 2404.10960; conformal abstention 2405.01563) or route to a human/CRM; the labelled-assumption pattern (Q4) is the graceful middle path but is unmeasured for AI.

**Confidence: low-medium** — PIM completeness metrics/thresholds are well documented (though vendor-sourced); the causal "guarding fails below X% completeness" claim has no substantive evidence.

---

### Q7 — Evaluation practice (failure → durable regression suite)

- **Format:** production failures are captured as eval cases ("Convert production failures into evaluation cases" — Maxim; Datadog/Arthur describe capturing failing traces as fixtures). [VM]
- **Judge rubrics:** practitioners warn the "most common mistake is vague criteria"; good judge prompts specify per-dimension criteria with chain-of-thought, ideally use a judge from a *different* model family than the generator, and prefer binary/discrete over fine numeric scores (vadim.blog [PE]; Arize [VM/PE]). Human-labelled validation sets of ~50–300 items, two+ annotators, and Cohen's κ reporting are the 2026 norm (D3-Gym n=52; DolusChat n=50; AMA-Bench n=300; stereotype study n=150 with judge self-consistency re-runs). [AC]
- **Named RAG corpora for regression:** RAGTruth (~18,000 word-level annotated responses; arXiv 2401.00396) and LLM-AggreFact (arXiv 2404.10774). [AC]
- **Judge-criteria drift:** handled via self-consistency (re-run at temp 0; 96.5% classification agreement in one study, disagreement concentrated at threshold boundaries — arXiv 2604.02669) and cross-family agreement (Qwen3-32B within 8.1 points of four other judges — arXiv 2602.22769). [AC]
- **Does anyone report judge errors of the kind in (c)?** The closest analogues are "No Free Labels" (judges reliable only on what they can answer) and "One Token to Fool LLM-as-a-Judge" (arXiv 2507.08794, judges gameable by surface features). **A judge specifically mis-ranking a labelled assumption vs a vague hedge: no substantive evidence found** — the requester's observation appears to be an under-reported failure mode, not a known-and-solved one.

**Confidence: medium** — eval-suite mechanics, set sizes, drift checks, and RAG corpora are well documented; the exact (c) judge-error is undocumented.

---

### Q8 — Anti-recommendations (reported not working / counterproductive)

- **System-prompt-only bans ("never make things up").** Ineffective: a bot instructed to never say it doesn't know will fabricate a confident "yes" (doublelayer, Register forums, Apr 2025) [PE]; RLHF may teach models to "prefer properly formatted fake output over truthful refusals" (durumu, HN id=41541834, Sep 2024): "you ask an LLM for some sources, with ISBNs, and it just makes up random titles and ISBNs … I wonder if this is because RLHF teaches the LLM that humans in practice prefer properly formatted fake output over truthful refusals?" [PE]
- **Temperature reduction to 0.** A myth for hallucination: "Setting the temperature to 0 often increases hallucination by removing the model's flexibility of escaping high-probability low-relevance phrasal assemblies … temperature only controls how deterministic the output is" (GDELT Project blog) [PE]; the same source notes "even top consulting firms falsely claim … temperature to 0.0 … can entirely eliminate hallucination." Determinism is not even guaranteed at temp 0 due to batch-invariance (Mikulski). [PE]
- **Hard output blocking.** Blunt blockers raise over-refusal (OR-Bench trade-off, arXiv 2405.20947) and produce the robotic/blander assistant the brief wants to avoid. [AC]
- **Long rule lists.** No direct measured study located; practitioner consensus (HN id=41541053) favours architecture over prose — "It's unsolvable inside the LLM. It's 100% solvable within the product" (more_corn, Sep 2024). A companion dissent frames the whole target: "A 'hallucination' is not a malfunction of the model, it's a value judgement we assign to the resulting text" (lolinder). [PE]
- **"Zero hallucination" vendor claims.** Treat as marketing. Mem0 markets "95%+" reduction (mem0.ai) [VM]; NeMo Guardrails' own repo disclaims it is "not meant for use in production applications" [VM]; a content-farm listicle names a vendor as "the reference standard" and resolves to a product pitch (mexc.com — no named author, promotional; content-farm signal) [UN]. Academic consensus: hallucination "cannot be fully eliminated" (arXiv 2410.03461 and multiple 2024–25 surveys). [AC] Dissent worth surfacing: one HN commenter argues even RAG/CoT are "band-aid approaches" that cannot fix hallucination (top comment, HN id=38563040) [PE] — a minority view, but a useful corrective to over-promising.

**Confidence: high** — the ineffectiveness of prompt-only bans, temperature-0, hard blocking, and zero-hallucination claims is corroborated across practitioner and academic sources with converging conclusions.

---

### Q9 — Ranked recommendation for the exact Context

**1. Do first (highest impact, low effort): fix the state machine for failure mode (b).** The quote-tool-after-decline bug is a tool-gating/state-transition defect, not a model-hallucination problem, and state gating *eliminates* the error class. Add an explicit `quote_declined` state that removes the quotation tool from the allowlist for the rest of the turn (and until re-requested), and assert in code that no quote tool-call co-occurs with a "won't prepare one" utterance. **Effort: days.** Deterministic, no model change. (Basis: Q1 state-gating; arXiv 2406.02630.)

**2. Do second (high impact, medium effort): a narrow sentence-level groundedness verifier for free-text attributes (failure mode a).** Numbers/SKUs/prices/stock are already code-verified; target the uncovered gap — free-text attribute claims ("breathable mesh back", "synchronised tilt"). Use a small fine-tuned checker (MiniCheck-FT5-class, 770M, "GPT-4-level performance but for 400x lower cost" — arXiv 2404.10774) or a DeBERTa-v3 NLI model doing "is this sentence supported by this catalog row?" per asserted attribute; regenerate or flag unsupported spans. Prefer the narrow binary task over holistic judge scoring (Q5). **Effort: 1–3 weeks incl. building a labelled regression set from your 60-response comparison.** **Threshold that changes the plan:** if the verifier's over-block (false-positive) rate on a held-out set exceeds your tolerance — the legal-QA study (arXiv 2410.08764) warns NLI adds latency and similarity methods over-flag — switch from hard-block to flag-for-review.

**3. Do third (medium impact, medium effort): fix the judge (failure mode c) and adopt a labelled-assumption rubric.** Rewrite the rubric to score three distinct categories: (i) grounded claim with citation → pass; (ii) **labelled, falsifiable assumption offered for confirmation** ("assuming roughly ten workstations per desk — or would you prefer a different split?") → *acceptable, not a hallucination*; (iii) vague unsourced claim ("its verified catalog features include adjustable elements and supportive seating") → *failure*. Validate the judge against a human-labelled set (n≈100–300, two annotators, report κ), cross-check with a second model family, and re-run at temp 0 for self-consistency (Q7). This directly addresses the point-(c) error, which is otherwise undocumented.

**Deliberately DO NOT:** (1) rely on system-prompt bans, temperature-0, or "never say you don't know" instructions — they backfire (Q8); (2) hard-block on a holistic groundedness score — it inflates over-refusal and produces the robotic assistant you want to avoid; (3) add a full knowledge-graph verifier or n× ensemble sampling for a flat catalog — cost/complexity unjustified vs a narrow checker; (4) trust "zero hallucination" tooling as a drop-in; (5) suppress the labelled-assumption behaviour — it is a legitimate assumptive-close move and the graceful alternative to both fabrication and refusal, provided the assumption is visible and confirmable. Separately, **audit trilingual catalog completeness** (Q6): if Arabic/Russian attribute fields are sparse, the verifier will (correctly) force abstention or labelled assumptions there — treat that as a data-enrichment backlog, not a guard to loosen.

**Confidence: medium-high** — the ranking follows from which mechanisms eliminate vs merely detect (well-evidenced) and from the specific failure modes; the labelled-assumption rubric is a reasoned extrapolation given the absence of direct eval evidence (Q4).

---

### Source table

| URL | Date | Type | Reliability |
|---|---|---|---|
| https://arxiv.org/abs/2404.10774 | 2024 (EMNLP) | AC | Peer-reviewed; 770M checker = GPT-4 accuracy at 400× lower cost; strong, directly relevant. |
| https://arxiv.org/pdf/2410.03461 | 2024 | AC | Peer-reviewed; verbatim source for 15–30% RAG hallucination range. |
| https://arxiv.org/pdf/2409.11242 | 2024 | AC | Defines Over-Responsiveness vs Excessive-Refusal; clean two-sided framing. |
| https://arxiv.org/abs/2405.20947 | 2024 (ICML'25) | AC | 80k-prompt over-refusal benchmark; safety-refusal scope — note the gap. |
| https://arxiv.org/pdf/2505.08054 | 2025 | AC | FalseReject; 16k queries, 29 models; over-refusal persists; safety scope. |
| https://arxiv.org/abs/2503.05061 | 2025 | AC | "No Free Labels" — judges reliable only on what they can answer; key limit. |
| https://arxiv.org/html/2508.18076 | 2025 | AC | "Neither Valid nor Reliable?" — catalogues judge biases; credible, critical. |
| https://arxiv.org/html/2410.08764 | 2024 | AC | Legal-QA groundedness; NLI beats chained SelfCheck/RefChecker; narrow-beats-holistic. |
| https://arxiv.org/pdf/2303.08896 | 2023 | AC | SelfCheckGPT; n× cost numbers and prompt-variant costs. |
| https://arxiv.org/abs/2405.01563 | 2024 | AC | Conformal abstention; theoretical bound on hallucination rate. |
| https://arxiv.org/html/2401.00396 | 2024 | AC | RAGTruth; ~18k word-level annotated RAG hallucination corpus. |
| https://arxiv.org/pdf/2406.02630 | 2024 | AC | State/string constraints can eliminate some hallucination classes. |
| https://arxiv.org/pdf/2411.07870 | 2024 | AC | Knowledge-triplet / dual-decoder grounding for production KBs. |
| https://arxiv.org/pdf/2607.04223 | 2026 | AC | NLI targets grounding directly but brittle on long context. |
| https://arxiv.org/pdf/2507.08794 | 2025 | AC | "One Token to Fool LLM-as-a-Judge" — judges gameable by surface features. |
| https://www.ebu.ch (News Integrity in AI Assistants) | 21 Oct 2025 | AC/PE | EBU/BBC study, 22 orgs; 45% of answers with a significant issue; Gemini 76%. |
| https://web.stanford.edu/class/cs224v/lectures/l-freetext.pdf | 2024/25 | AC | Course slides citing the BBC Feb-2025 51%/19%/13% figures. |
| https://news.ycombinator.com/item?id=41541053 | Sep 2024 | PE | Fully retrieved HN thread; "100% solvable within the product" vs "always hallucinate." |
| https://news.ycombinator.com/item?id=38563040 | 2023 | PE | Only top comment recovered (429 on full thread); RAG-as-"band-aid" dissent. |
| https://news.ycombinator.com/item?id=43420170 | Mar 2025 | PE | OP only; 50M records, 90% five-star, 10–30s latency (anecdotal). |
| https://forums.theregister.com/forum/all/2025/04/18/cursor_ai_support_bot_lies/ | Apr 2025 | PE | Practitioner forum; "never say I don't know" → fabrication. |
| https://dev.to/polterguy/ai-chatbots-to-hallucinate-or-not-to-hallucinate-1dmf | n.d. | PE | Practitioner disabling guardrails to avoid over-refusal. |
| https://robbclarke.substack.com/p/stop-blaming-the-ai-your-hallucination | n.d. | PE | "74.8% of tickets"; guardrails-as-system-property (anecdotal). |
| https://blog.gdeltproject.org/understanding-hallucination-in-llms-a-brief-introduction/ | n.d. | PE | Temp-0 myth debunked with mechanism; credible technical author. |
| https://vadim.blog/llm-as-judge/ | n.d. | PE | MT-Bench 80%→~65% multi-turn agreement; judge-rubric guidance. |
| https://arxiv.org/pdf/2604.02669 | 2026 | AC | Judge self-consistency 96.5%; drift concentrated at thresholds. |
| https://arxiv.org/pdf/2602.22769 | 2026 | AC | Cross-family judge agreement (Qwen3-32B within 8.1 pts). |
| https://pimberly.com/blog/what-is-pim-data/ | n.d. | VM | PIM completeness scoring; vendor but industry-standard metric. |
| https://nanopim.com/post/dimensions-of-data-quality | n.d. | VM | 92% aggregate vs 65% localized completeness; trilingual relevance. |
| https://odoopim.com/blog/ecommerce-product-management/ | n.d. | VM | "30–50% higher conversion" — vendor-claimed; caution. |
| https://sellingsignals.com/assumptive-close/ | n.d. | VM/PE | Assumptive/presumptive close mechanics. |
| https://prospeo.io/s/spin-selling | 2026 | VM/PE | Dissent: closing techniques hurt complex-B2B win rates. |
| https://www.getmaxim.ai/articles/llm-hallucination-detection-and-mitigation-best-techniques/ | n.d. | VM | Vendor playbook; useful taxonomy, resolves to product. |
| https://mem0.ai/blog/reducing-hallucinations-llms-with-grounded-memory | n.d. | VM | "95%+" reduction claim — marketing, uncorroborated. |
| https://www.mexc.com/it-IT/news/649772 | Feb 2026 | UN | Content-farm listicle; no named author; resolves to vendor pitch. |
| https://www.datadoghq.com/blog/llm-observability-hallucination-detection/ | n.d. | VM | Vendor feature; contextual grounding detection. |
| https://www.arthur.ai/blog/best-practices-for-building-agents-guardrails | n.d. | VM | Pre-/post-LLM guardrail patterns; vendor but concrete. |
| https://aws.amazon.com/blogs/machine-learning/reducing-hallucinations-in-large-language-models-with-custom-intervention-using-amazon-bedrock-agents | n.d. | VM | Bedrock Guardrails contextual grounding checks. |

**Stop-condition assessment.** The search did not collapse into pure marketing — a substantial academic spine (MiniCheck, OR-Bench, FalseReject, RAGTruth, No Free Labels, Auto-GDA, conformal abstention) and verifiable practitioner comments (HN id=41541053, Register forums, GDELT) were obtained. **However, the brief's single highest-priority source class — Reddit practitioner threads — produced no substantive evidence because Reddit was unreachable, and two of five target HN threads yielded only partial content.** The most important missing evidence is therefore: (1) Reddit practitioner postmortems with numbers on groundedness-guard over-refusal in a *sales* context; (2) any measured per-message latency/cost/effort for a groundedness second pass in a comparable assistant; (3) any measured commercial (conversion/CSAT) impact of over-constraint in selling; and (4) any documented eval rubric or customer-response data for the labelled-assumption pattern from an AI. These four gaps are marked "no substantive evidence found" in Q2–Q4 rather than padded.