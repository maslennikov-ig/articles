# Как у нас устроены Codex orchestration skills

Материал для статьи. Дата среза: 2026-05-18.

Этот документ описывает нашу локальную систему orchestration skills: какие skills есть, зачем они разделены, как они взаимодействуют с `AGENTS.md`, Beads, Superpowers, Codex subagents, routing, worktrees, verification и closeout. Его можно использовать как исходник для статьи, поста или внутреннего README.

## Короткая версия

Мы построили не один большой "магический промпт", а маленькую систему контрактов:

- `AGENTS.md` задает компактные правила репозитория.
- `orchestration-setup` инициализирует и проверяет baseline.
- `orchestrator-stage` управляет сложным этапом работы.
- `task-router` помогает выбрать документацию, skills и agents.
- `orchestration-closeout` закрывает этап: verification, delivery, cleanup.
- Beads остается источником правды по задачам.
- Superpowers остаются обязательными процессными skills.
- Codex subagents используются только как отдельные видимые spawned agent threads/runs, не inline.
- Для medium/complex задач оркестратор обязан сделать Parallel Decomposition Matrix и запускать независимые streams параллельно, если пользователь явно разрешил subagents.
- Модель и reasoning subagents выбираются policy-driven: по умолчанию inherit, для риска/сложности повышается reasoning, явный model override требует текущего разрешения пользователя или четкой причины.

Текущий repo baseline: `balanced-v2.12`.

## Основные ссылки

### Наши orchestration skills

- [`orchestration-setup`](/home/me/.agents/skills/orchestration-setup/SKILL.md) - инициализация, audit и reconcile repo-local baseline.
- [`orchestrator-stage`](/home/me/.agents/skills/orchestrator-stage/SKILL.md) - управление medium/complex этапом, routing, decomposition, subagents, review, verification.
- [`orchestration-closeout`](/home/me/.agents/skills/orchestration-closeout/SKILL.md) - закрытие этапа, delivery и workspace cleanup.
- [`task-router`](/home/me/.agents/skills/task-router/SKILL.md) - routing substep для docs, skills, custom agents и local catalog.

### Главный глобальный контракт

- [`/home/me/.codex/AGENTS.md`](/home/me/.codex/AGENTS.md) - глобальные правила Codex workflow: русский язык, triage, delegation, Beads, Superpowers, delivery boundaries.

### Основные templates и support files

- [`baseline.toml`](/home/me/.agents/skills/orchestration-setup/templates/baseline.toml) - текущая версия baseline и managed surface.
- [`subagent-task-contract.md`](/home/me/.agents/skills/orchestration-setup/templates/subagent-task-contract.md) - контракт для worker/subagent stream.
- [`subagent-spawn-template.md`](/home/me/.agents/skills/orchestration-setup/templates/subagent-spawn-template.md) - шаблон задачи для отдельного spawned subagent.
- [`stage-artifact-template.md`](/home/me/.agents/skills/orchestration-setup/templates/stage-artifact-template.md) - формат tracked artifact для delegated stream.
- [`manual-agent-prompt-template.md`](/home/me/.agents/skills/orchestration-setup/templates/manual-agent-prompt-template.md) - legacy/fallback ручной prompt pack.
- [`run_process_verification.sh`](/home/me/.agents/skills/orchestration-setup/templates/scripts/run_process_verification.sh) - process verification baseline.
- [`report_child_completion.py`](/home/me/.agents/skills/orchestration-setup/templates/scripts/report_child_completion.py) - запись completion event от subagent.
- [`review_completion_inbox.py`](/home/me/.agents/skills/orchestration-setup/templates/scripts/review_completion_inbox.py) - просмотр completion inbox.
- [`run_stage_closeout.py`](/home/me/.agents/skills/orchestration-setup/templates/scripts/run_stage_closeout.py) - stage closeout entrypoint.
- [`cleanup_stage_workspace.py`](/home/me/.agents/skills/orchestration-setup/templates/scripts/cleanup_stage_workspace.py) - safe cleanup worktrees/branches.
- [`audit_repo.py`](/home/me/.agents/skills/orchestration-setup/support/audit_repo.py) - audit repo against baseline.
- [`sync_support_files.py`](/home/me/.agents/skills/orchestration-setup/support/sync_support_files.py) - sync template-managed files into repo.

### Superpowers, которые важны для системы

- [`using-superpowers`](/mnt/c/Users/user/.codex/superpowers/skills/using-superpowers/SKILL.md) - базовая дисциплина использования skills.
- [`brainstorming`](/mnt/c/Users/user/.codex/superpowers/skills/brainstorming/SKILL.md) - перед новым поведением/творческой работой.
- [`writing-plans`](/mnt/c/Users/user/.codex/superpowers/skills/writing-plans/SKILL.md) - для многошаговой реализации.
- [`executing-plans`](/mnt/c/Users/user/.codex/superpowers/skills/executing-plans/SKILL.md) - выполнение плана.
- [`test-driven-development`](/mnt/c/Users/user/.codex/superpowers/skills/test-driven-development/SKILL.md) - TDD для feature/bugfix.
- [`systematic-debugging`](/mnt/c/Users/user/.codex/superpowers/skills/systematic-debugging/SKILL.md) - баги и неожиданные failures.
- [`verification-before-completion`](/mnt/c/Users/user/.codex/superpowers/skills/verification-before-completion/SKILL.md) - нельзя заявлять "готово" без проверки.
- [`subagent-driven-development`](/mnt/c/Users/user/.codex/superpowers/skills/subagent-driven-development/SKILL.md) - разработка через независимые subagent tasks.
- [`dispatching-parallel-agents`](/mnt/c/Users/user/.codex/superpowers/skills/dispatching-parallel-agents/SKILL.md) - параллельные агенты для независимых задач.
- [`using-git-worktrees`](/mnt/c/Users/user/.codex/superpowers/skills/using-git-worktrees/SKILL.md) - изоляция работы в worktrees.
- [`writing-skills`](/mnt/c/Users/user/.codex/superpowers/skills/writing-skills/SKILL.md) - как создавать и проверять skills.

### Официальные Codex docs, на которые мы опираемся

- [Codex skills](https://developers.openai.com/codex/skills) - skills как reusable bundles с progressive disclosure.
- [Codex customization](https://developers.openai.com/codex/concepts/customization) - `SKILL.md`, metadata и local customization.
- [Codex subagents](https://developers.openai.com/codex/subagents) - subagents, spawned workflows, built-in/custom agents, explicit user request.

## Почему skills разделены именно так

Главная идея: не смешивать lifecycle проекта, lifecycle этапа и routing в один большой workflow.

### `orchestration-setup`

`orchestration-setup` отвечает за baseline проекта:

- создать минимальную repo-local структуру;
- проверить drift;
- синхронизировать support scripts и templates;
- поднять baseline версию;
- оставить `AGENTS.md` компактным;
- не встраивать весь workflow в один большой файл.

Это skill для "подготовить репозиторий к нормальной agentic работе", а не для ежедневной реализации задач.

### `orchestrator-stage`

`orchestrator-stage` отвечает за активную работу над medium/complex задачей:

- прочитать repo contract;
- выбрать Beads task;
- сделать routing docs/skills/agents;
- применить нужные Superpowers;
- построить Parallel Decomposition Matrix;
- решить, что делать локально, что отдать subagents, что запускать параллельно;
- сформулировать задачи subagents;
- проверить и принять результат;
- обновить handoff/stage artifacts.

Это skill для "вести этап как инженерный оркестратор".

### `task-router`

`task-router` не является самостоятельным главным workflow. Это routing substep:

- когда нужны актуальные docs;
- когда нужно выбрать installed skill;
- когда нужно выбрать custom agent;
- когда нужно посмотреть local catalog;
- когда потенциально нужен `skill_scout` или `asset_vetter`.

Важно: routing не заменяет Superpowers. После routing оркестратор все равно применяет `brainstorming`, `writing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion` и другие процессные skills по ситуации.

### `orchestration-closeout`

`orchestration-closeout` нужен в конце:

- проверить stage truth;
- проверить accepted delegated artifacts;
- запустить verification;
- решить delivery по repo policy;
- обновить Beads/handoff;
- почистить safe worktrees/branches;
- не оставить silent debt.

Это отдельный skill, потому что закрытие этапа - другой режим мышления: не "как быстрее сделать", а "как безопасно доказать, что готово и ничего не забыто".

## Как устроен repo-local baseline

В каждом основном проекте baseline живет в `.codex/` и рядом с ним:

```text
AGENTS.md
.codex/
  orchestrator.toml
  handoff.md
  project-index.md
  stage-artifact-template.md
  subagent-task-contract.md
  subagent-spawn-template.md
  manual-agent-prompt-template.md   # только fallback/manual repos
  stages/
scripts/
  orchestration/
    run_process_verification.sh
    validate_artifact.py
    check_stage_ready.py
    run_stage_closeout.py
    cleanup_stage_workspace.py
    report_child_completion.py
    review_completion_inbox.py
```

### `AGENTS.md`

`AGENTS.md` - human-facing контракт. Он должен быть компактным:

- как устроен проект;
- какие entrypoints важны;
- какие verification commands canonical;
- где состояние;
- какие delivery boundaries;
- когда использовать orchestration;
- что Beads - task truth;
- что Superpowers обязательны;
- что subagents должны быть separate spawned, если делегируем.

Мы сознательно не превращаем `AGENTS.md` в длинный учебник. Он должен быстро загружаться и не раздувать контекст.

### `.codex/orchestrator.toml`

Это machine-readable контракт. В нем хранится:

- baseline profile;
- repo topology;
- delegation policy;
- subagent model policy;
- verification commands;
- delivery policy;
- paths to handoff/artifacts/scripts;
- stage limits;
- completion inbox config.

Пример ключевых полей текущего baseline:

```toml
[baseline]
profile = "balanced-v2.12"
source_skill = "orchestration-setup"

[delegation]
launcher = "codex_subagents"
subagent_visibility = "separate_spawned_threads"
inline_subagents_allowed = false
requires_explicit_user_spawn_request = true
parallel_decomposition_matrix = "required_for_medium_complex"
parallel_execution_default = "spawn_all_independent_streams"
sequential_requires_reason = true

[subagent_model_policy]
default_model = "inherit_orchestrator"
default_reasoning_effort = "inherit_orchestrator"
reasoning_policy = "complexity_based"
model_override_requires_current_user_authorization = true
record_model_reasoning_rationale = true
```

### `.codex/handoff.md`

Это current-state файл. Он не должен становиться историей проекта.

Он отвечает на вопросы:

- где мы сейчас;
- какой следующий stage id;
- что делать дальше;
- какой starter prompt дать следующему оркестратору;
- какие explicit defers есть.

История переносится в `.codex/stages/`, а не копится в handoff.

### `.codex/project-index.md`

Это стабильная навигационная карта проекта:

- runtime shape;
- primary entrypoints;
- core subsystems;
- integrations/source of truth;
- verification;
- conventions/boundaries.

В нем не должно быть текущих blockers, deployment logs, stage history или handoff sections.

### `.codex/stages/`

Здесь живет история этапов:

- summary stage;
- artifacts delegated streams;
- accepted/rejected evidence;
- verification status;
- explicit defers.

Это компромисс между "все в чате" и "ничего не сохраняем": важные решения остаются в repo-local structured files.

## Основной workflow

### 1. Новый проект

Старт:

```text
Use $orchestration-setup in /home/me/code/<repo>.
Initialize or audit the repo-local orchestration baseline.
Use auto-subagents mode by default.
Keep Beads, Superpowers, Asset Routing, Documentation, verification, and no-silent-debt rules.
```

Что делает `orchestration-setup`:

1. Определяет topology и delivery mode.
2. Создает/проверяет `AGENTS.md`.
3. Создает/проверяет `.codex/orchestrator.toml`.
4. Создает/проверяет handoff, project index, templates.
5. Копирует support scripts.
6. Запускает process verification.
7. Возвращает `aligned`, `aligned_with_exceptions` или `drifted`.

### 2. Новый этап в уже настроенном проекте

Старт:

```text
Use $orchestrator-stage in /home/me/code/<repo>.
Start a new stage for: <goal>.

I explicitly authorize you in this current task to spawn separate visible Codex subagents when justified.
Do not use inline-only delegation.
You may choose subagent reasoning level by task complexity; explicit model override only with a clear reason.
```

Дальше оркестратор:

1. Классифицирует задачу: simple или medium/complex.
2. Для simple делает сам, без ceremony.
3. Для medium/complex читает `AGENTS.md`, `orchestrator.toml`, `handoff.md`, `project-index.md`, Beads.
4. Создает или выбирает Beads task.
5. Делает routing: docs, skills, agents, catalog.
6. Применяет нужные Superpowers.
7. Строит Parallel Decomposition Matrix.
8. Запускает independent streams параллельно, если это безопасно и разрешено.
9. Проверяет результаты subagents.
10. Обновляет artifacts, Beads, handoff.

### 3. Закрытие этапа

Старт:

```text
Use $orchestration-closeout in /home/me/code/<repo>.
Close stage <stage-id> according to repo contract.
Run required verification, update Beads/handoff, and clean safe local stage leftovers.
```

Closeout не доверяет словам "готово". Он требует evidence:

- artifact accepted;
- verification passed или blocker explicit;
- no silent debt;
- delivery state matches policy;
- cleanup completed или blocked with reason.

## Parallel Decomposition Matrix

Это один из центральных элементов текущей версии.

Для каждой medium/complex задачи оркестратор обязан до реализации построить компактную матрицу:

| Stream | Goal | Agent | Write zone | Dependencies | Verification | Model/reasoning | Decision | Reason |
|---|---|---|---|---|---|---|---|---|
| `s1` | Изменить backend contract | `worker` | `src/api/*` | none | `pytest ...` | inherit/high | parallel | isolated write zone |
| `s2` | Обновить UI state | `worker` | `frontend/*` | waits for contract shape | `pnpm test` | inherit/medium | sequential | depends on s1 schema |
| `s3` | Проверить docs API | `docs_researcher` | read-only | none | source citation | role_default | parallel | read-only |

Правило: если есть два или больше independent streams, и subagents явно разрешены пользователем, оркестратор должен запускать их параллельно.

Sequential/local допустимо только с конкретной причиной:

- dependency chain;
- write conflict;
- shared verification bottleneck;
- shared external resource;
- uncertain scope;
- repo limit.

Плохая причина: "файлы связаны". Хорошая причина: "stream A и B оба меняют `src/graph/state.ts`, а тестовый цикл `tests/graph.spec.ts` неразделим; сначала стабилизируем state contract, потом запускаем UI worker".

## Subagents: только separate spawned threads/runs

Мы специально запретили inline-only delegation.

Причина: пользователю важно видеть отдельных агентов:

- у них есть роли/имена;
- в них можно зайти;
- можно смотреть ход работы;
- проще проверять, кто что сделал;
- проще отлаживать orchestration.

Текущий контракт:

```toml
subagent_visibility = "separate_spawned_threads"
inline_subagents_allowed = false
requires_explicit_user_spawn_request = true
```

Это соответствует текущей документации Codex: subagent workflows видны в Codex app/CLI, но запускаются только когда пользователь явно попросил/разрешил subagents.

Практическое следствие: repo contract сам по себе недостаточен. В стартовом prompt текущей задачи надо писать явное разрешение:

```text
I explicitly authorize you in this current task to spawn separate visible Codex subagents when justified.
Do not use inline-only delegation.
```

Если этого нет, осторожный агент имеет право спросить разрешение вместо того, чтобы silently spawn.

## Контракт задачи subagent

Subagent не получает расплывчатое "посмотри и сделай". Оркестратор обязан сформулировать задачу сам.

Минимальные блоки:

- `Task ID` / Beads reference;
- `Stage ID`;
- `Agent Type`;
- visibility;
- model/reasoning/rationale;
- goal;
- success criteria;
- documentation;
- asset routing;
- context and ownership;
- branch/worktree;
- parallel group;
- write zone;
- verification;
- output contract;
- stop rules.

Пример формы:

```md
Task ID: mc2-db696.3
Stage ID: mc2-db696
Agent Type: worker
Visibility: separate spawned Codex agent/thread/run; inline-only delegation is not allowed
Model: inherit_orchestrator
Reasoning Effort: high
Model/Reasoning Rationale: cross-module graph/state change with regression risk

## Goal
Implement group 3 loader flow without touching judge/regenerator code.

## Success Criteria
- Loader handles empty state.
- Existing graph tests still pass.
- New regression test covers missing headings.

## Documentation
- No dependency documentation lookup needed.

## Asset Routing
- Selected docs: none - repo-local behavior
- Selected skills: superpowers:test-driven-development
- Selected agents/personas: worker
- Catalog candidates: none - installed assets sufficient

## Context And Ownership
- Workspace root: /home/me/code/mc2
- Branch/worktree: dedicated worktree required
- Parallel group: stream s3; siblings s4 judge, s5 assembler
- Write zone: src/graph/loader.ts, tests/loader.spec.ts

## Verification
- Run: pnpm test -- loader

## Stop Rules
Return blocked if state contract changes require touching sibling streams.
```

## Model/reasoning policy

Мы не хотим, чтобы оркестратор произвольно выбирал дорогую или другую модель. Поэтому политика такая:

- default model: inherit orchestrator;
- default reasoning: inherit orchestrator;
- reasoning policy: complexity-based;
- explicit model override requires current user authorization or a clear task-specific reason;
- every choice must be recorded.

High reasoning triggers:

- architecture;
- security;
- data migration;
- cross-module change;
- critical bug;
- review;
- ambiguous requirements.

Практический смысл:

- простой `explorer` может идти на inherited/medium;
- критический `reviewer` или risky `worker` может получить high/xhigh reasoning;
- custom agent может иметь свой configured model/reasoning;
- explicit model override лучше писать в prompt явно, если пользователь хочет дать оркестратору право выбирать.

Хорошая фраза в prompt:

```text
You may choose subagent reasoning level by task complexity.
Use higher reasoning for architecture, security, migrations, cross-module changes, reviews, and ambiguous requirements.
Use inherited model by default; set explicit model only if there is a clear task-specific reason.
```

## Beads как task truth

Beads - единственный task ledger.

Правило:

- file-changing work;
- delegated work;
- работа дольше примерно 15 минут;
- handoff-prone work;

должны иметь Beads task или выбранный существующий task.

Мы убрали зависимость от hooks. Это важно: hooks были неявной магией и ломались. Теперь агент должен явно работать с Beads через команды, а не надеяться на startup injection.

Почему это лучше:

- меньше скрытого поведения;
- проще переносить между средами;
- легче объяснить другому агенту;
- меньше "а почему это сработало вчера и не сработало сегодня".

## Superpowers остаются обязательными

Routing не заменяет процесс.

Если задача новая/творческая - нужен `brainstorming`.

Если задача многошаговая - `writing-plans`.

Если баг - `systematic-debugging`.

Если feature/bugfix - `test-driven-development` когда уместно.

Перед "готово" - `verification-before-completion`.

Это принципиально: `task-router` выбирает инструменты и источники, но не решает инженерную дисциплину.

## Asset Routing

Каждый delegated prompt должен иметь `Asset Routing`:

- Selected docs;
- Selected skills;
- Selected agents/personas;
- Catalog candidates.

Если ничего не подходит, пишется `none - reason`, а не блок пропускается.

Зачем:

- subagent понимает, какие активы уже выбраны;
- worker не тратит время на повторное catalog discovery;
- orchestrator централизует решение;
- проще проверить, почему выбран именно этот skill/agent.

Subagent может делать fresh asset discovery только если выбранные assets недоступны или появился specialist blocker.

## Completion inbox и artifacts

Subagent return не равен acceptance.

Система разделяет:

- completion event - "worker вернулся";
- artifact - "что worker утверждает";
- orchestrator review - "принято или нет";
- local verification - "доказано или нет".

`report_child_completion.py` пишет событие в inbox. Но событие не означает, что работа принята.

Artifact должен фиксировать:

- task id;
- stage id;
- agent type;
- model/reasoning;
- write zone;
- selected assets;
- parallel group;
- verification;
- changed files;
- explicit defers;
- cleanup status;
- accepted by orchestrator: yes/no.

Это дает audit trail: можно понять не только что изменилось, но и почему stream был выделен, кому он был отдан, с каким уровнем reasoning и как был проверен.

## Worktrees и isolation

Write-heavy workers по умолчанию работают в dedicated branch/worktree.

Зачем:

- меньше конфликтов;
- можно параллелить streams;
- проще принять/отклонить поток;
- легче убрать leftovers;
- primary worktree не превращается в свалку.

Read-only agents (`explorer`, `docs_researcher`, `skill_scout`) могут работать без отдельного worktree, если не меняют файлы.

## Manual fallback

Manual prompt packs остались, но только как fallback:

- subagents недоступны;
- runtime предлагает только inline delegation;
- repo явно требует `manual_user_launch`;
- пользователь сам просит ручной prompt pack.

Важно: manual fallback не ослабляет правила.

Даже manual prompt должен иметь:

- Beads task;
- docs;
- asset routing;
- write zone;
- verification;
- stop rules;
- output contract;
- branch/worktree policy.

## Почему это работает

### 1. Progressive disclosure

Skills не должны грузить весь мир в контекст сразу. Codex сначала видит name/description/path, потом читает `SKILL.md`, потом только нужные references/scripts/templates.

Это совпадает с официальной идеей Codex skills: reusable bundles с progressive disclosure.

Практический эффект:

- меньше контекста;
- меньше случайных инструкций;
- проще обновлять отдельные skills;
- больше шансов, что агент прочитает именно нужный workflow.

### 2. Orchestrator-first, но не delegation-first

Оркестратор сначала думает:

- задача простая?
- нужна ли изоляция?
- есть ли реальный параллелизм?
- нужен ли специалист?
- можно ли проверить результат?

Простые задачи он делает сам. Это важно: иначе orchestration превращается в бюрократию.

### 3. Parallelism как default для независимых streams

Если можно распараллелить безопасно, надо распараллеливать.

Но безопасный parallelism требует:

- disjoint write zones;
- независимые проверки;
- понятные dependencies;
- dedicated worktrees;
- нормальные artifacts.

Поэтому Parallel Decomposition Matrix стала обязательной.

### 4. Видимые spawned agents вместо inline

Inline delegation плохо подходит нашему workflow, потому что пользователь не видит отдельного агента как отдельный workstream.

Separate spawned agents дают:

- наблюдаемость;
- управляемость;
- возможность зайти в run;
- понятное разделение ответственности.

### 5. Verification before trust

Ни worker summary, ни completion event, ни зеленые слова "done" не являются proof.

Proof - это:

- diff review;
- artifact review;
- local verification;
- repo process verification;
- closeout checks.

## Хорошие стартовые prompt'ы

### Новый проект

```text
Use $orchestration-setup in /home/me/code/<repo>.
Initialize or audit the repo-local orchestration baseline.
Use codex_subagents mode by default.
Keep Beads, Superpowers, Asset Routing, Documentation, verification, worktree isolation, and no-silent-debt rules.
Report whether the repo is aligned, aligned_with_exceptions, or drifted.
```

### Новый сложный этап

```text
Use $orchestrator-stage in /home/me/code/<repo>.
Start a new stage for: <goal>.

I explicitly authorize you in this current task to spawn separate visible Codex subagents when justified.
Do not use inline-only delegation.

Before implementation, build a Parallel Decomposition Matrix.
Spawn all independent streams in parallel when safe.
If you keep work local or sequential, state the concrete dependency/write-conflict/verification/repo-limit reason.

You may choose subagent reasoning level by task complexity.
Use higher reasoning for architecture, security, migrations, cross-module changes, critical bugs, reviews, and ambiguous requirements.
Use inherited model by default; explicit model override only with a clear task-specific reason.
```

### Закрытие этапа

```text
Use $orchestration-closeout in /home/me/code/<repo>.
Close stage <stage-id>.
Verify accepted artifacts, run repo-local verification, update Beads and handoff, and clean safe stage worktrees/branches.
Do not treat completion events as acceptance by themselves.
```

## Что можно подчеркнуть в статье

Идеи для narrative:

1. "Мы перестали писать один огромный AGENTS.md и разложили агентную работу на skills."
2. "Оркестратор не должен быть самым умным промптом; он должен быть диспетчером контрактов."
3. "Subagents ускоряют разработку только когда у них есть boundaries."
4. "Параллельность без write zones - это не ускорение, а генератор конфликтов."
5. "Completion event - не acceptance."
6. "Hooks казались удобными, но явные команды надежнее."
7. "Beads дает task truth, а `.codex/stages` дает engineering evidence."
8. "Routing не заменяет engineering process."
9. "Модель subagent должна быть policy, а не случайным выбором."
10. "Система работает не потому, что агент умнее, а потому что ему сложнее сделать тихую глупость."

## Ограничения и честные caveats

- Codex runtime требует явный user request для spawning subagents. Поэтому разрешение должно быть в текущем prompt.
- Некоторые роли могут иметь fixed reasoning profile; их нельзя всегда переопределить.
- Старые временные worktrees могут иметь старый baseline. Мы обновляем primary repo baseline, а не исторические worktree-копии.
- Manual fallback сохраняется, потому что subagents могут быть недоступны в конкретной среде.
- Beads hooks удалены; Beads надо вести явно.
- Parallelism не должен быть декоративным: если streams конфликтуют по write zone, их надо делать последовательно.

## Текущий статус системы

На момент этого среза:

- current baseline: `balanced-v2.12`;
- primary repo-local orchestration projects синхронизированы на `balanced-v2.12`;
- baseline требует separate spawned subagents, не inline;
- baseline требует Parallel Decomposition Matrix для medium/complex work;
- baseline требует subagent model/reasoning policy;
- process verification проверяет ключевые contract fields;
- `quick_validate.py` проходит для основных orchestration skills;
- `run_process_verification.sh` проходит в основных repo-local проектах.

## Что планируем улучшать дальше

Система уже работает как проверяемый инженерный процесс, но следующий уровень - проверять не только наличие файлов и contract fields, а поведение оркестратора на реальных сценариях.

### 1. Scenario tests для orchestration behavior

Сейчас `audit_repo.py` и `run_process_verification.sh` проверяют baseline: версии, файлы, обязательные поля, handoff, project index, completion inbox. Это хорошо, но это structural validation.

Следующий шаг - behavioral validation:

- medium/complex task -> оркестратор обязан построить Parallel Decomposition Matrix;
- есть 2+ independent streams + user authorization -> оркестратор обязан spawn separate subagents;
- нет explicit subagent authorization -> оркестратор обязан спросить разрешение, а не молча делать все сам;
- write-heavy stream -> dedicated branch/worktree;
- delegated prompt -> содержит Beads task, Asset Routing, Documentation, write zone, verification, stop rules;
- subagent result -> не принимается без artifact/diff/verification review.

Идея: сделать небольшой набор "pressure scenarios" для orchestration skills. Это будет TDD для процесса: сначала проверяем, где агент срезает углы, потом закрываем loophole в skill/contract/script.

### 2. Catalog custom agents

Сейчас у нас есть хорошая policy для выбора built-in agents (`worker`, `explorer`, `docs_researcher`, `skill_scout`) и возможность custom agents. Но база специализированных agents еще может стать сильнее.

Полезные custom agents:

- `reviewer` - correctness/security/regression/missing tests;
- `architect` - cross-module design, boundaries, migration path;
- `test-engineer` - regression tests, flaky tests, fixtures;
- `migration-specialist` - schema/data/runtime migrations;
- `frontend-ux-worker` - UI implementation with visual/interaction checks;
- `security-reviewer` - auth, permissions, secrets, data exposure;
- `release-engineer` - delivery, CI, changelog, PR/readiness.

Для каждого agent стоит задать:

- `name`;
- `description`;
- `developer_instructions`;
- model/reasoning defaults;
- sandbox mode;
- optional `nickname_candidates` для читаемых spawned agent names.

### 3. Stage dashboard

Сейчас состояние распределено между:

- Beads;
- `.codex/handoff.md`;
- `.codex/stages/`;
- completion inbox;
- git worktrees/branches;
- process verification.

Следующий шаг - один CLI/report, например:

```bash
scripts/orchestration/stage_dashboard.py --stage <stage-id>
```

Он мог бы показывать:

- active stage;
- linked Beads tasks;
- spawned streams;
- stream status: launched/returned/accepted/blocked;
- artifact path;
- verification status;
- cleanup status;
- dirty worktrees;
- branches safe/unsafe to delete;
- explicit defers.

Это сделает систему более наблюдаемой и снизит риск забытых веток, worktrees или accepted-but-not-cleaned streams.

### 4. Более жесткие quality gates для artifacts

Сейчас artifact template уже требует много полей, но validator можно усилить.

Будущие проверки:

- `agent_type` заполнен;
- `subagent_model`, `reasoning_effort`, `model_reasoning_rationale` заполнены;
- `write_zone` не пустой для write-heavy worker;
- `parallel_group`, `parallel_decision`, `depends_on_streams` согласованы с matrix;
- `verification` содержит реальные команды и результат;
- `explicit_defers` либо `none`, либо Beads-linked reason;
- `accepted_by_orchestrator: yes` нельзя поставить без verification evidence;
- `cleanup_status: pending` запрещен для stage closeout.

Это превратит artifact из "отчета по форме" в настоящий acceptance contract.

### 5. Golden prompts

Нужен набор коротких, проверенных стартовых prompt'ов:

- новый проект;
- audit/reconcile baseline;
- новый сложный stage;
- parallel implementation stage;
- docs-sensitive stage;
- risky migration;
- review-only stage;
- closeout;
- cleanup/recovery.

Golden prompts важны, потому что Codex runtime требует explicit user request для spawning subagents. Если правильная фраза не попала в стартовый prompt, агент может легально не spawn'ить subagents.

Главная фраза для сложного этапа:

```text
I explicitly authorize you in this current task to spawn separate visible Codex subagents when justified. Do not use inline-only delegation.
```

### 6. Better worktree lifecycle accounting

Параллельная разработка ускоряет работу, но создает operational debt: ветки, worktrees, частично принятые изменения, abandoned streams.

Нужно усилить учет:

- какой stream создал какой worktree;
- принят ли stream;
- был ли merge/cherry-pick/manual integration;
- можно ли удалить branch;
- есть ли dirty files;
- почему cleanup blocked.

Часть этого уже есть в `cleanup_stage_workspace.py` и artifact fields, но можно сделать сильнее через dashboard и stricter closeout checks.

### 7. Evaluation layer для skills

Идеальный следующий слой - evals для самих orchestration skills:

- synthetic repo;
- fake Beads tasks;
- scripted user prompts;
- expected orchestration behavior;
- assertions по produced matrix, prompt blocks, routing, artifact fields.

Это позволит регрессионно проверять: не начал ли новый skill text снова провоцировать агента делать все локально, пропускать Beads или забывать Asset Routing.

### 8. Публикуемая версия системы

Если делать из этого публичный материал или open-source template, нужно отделить:

- private local paths;
- project-specific assumptions;
- Beads-specific integration;
- Superpowers-specific integration;
- Codex-specific subagents policy;
- generic concepts.

Тогда можно сделать две версии:

- internal: полный рабочий контракт;
- public: объяснение архитектуры + адаптируемые templates.

## Возможная структура готовой статьи

1. Проблема: агенты быстро превращаются в хаос.
2. Почему один большой `AGENTS.md` не спасает.
3. Skills как progressive disclosure.
4. Четыре уровня: setup, stage, router, closeout.
5. Repo-local contract: `AGENTS.md`, `.codex/orchestrator.toml`, handoff, project index, stages.
6. Beads и Superpowers: task truth и process truth.
7. Subagents: только видимые spawned runs.
8. Parallel Decomposition Matrix как механизм ускорения.
9. Worker contract: как правильно ставить задачу агенту.
10. Review/acceptance: почему summary не равно done.
11. Model/reasoning policy.
12. Что убрать: hooks, implicit magic, giant prompts.
13. Roadmap: scenario tests, custom agents, dashboard, stricter artifact gates, golden prompts.
14. Итог: agentic development как система контрактов, а не вера в одного умного агента.
