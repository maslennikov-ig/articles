---
platform: habr
title: "Собрал оркестратор для Codex на базе Beads и Superpowers — 4 skill, параллельные subagents, наблюдаемость. Архив прикладываю"
subtitle: "Что внутри: 4 локальных skill, `.codex/orchestrator.toml` как машинный контракт, обязательная Parallel Decomposition Matrix и worker-контракт для каждого spawned subagent"
author: Igor Maslennikov
date: 2026-05-18
length: ~20000 characters
tags: [Codex, AI-агенты, OpenAI, оркестрация-агентов, skills, Beads, Superpowers, parallel-execution]
hubs: [Искусственный интеллект, Программирование]
language: ru
feed_preview: |
  Я работаю с Codex каждый день и со временем собрал поверх
  него систему оркестрации: 4 локальных skill (setup, stage,
  router, closeout), `.codex/orchestrator.toml` как машинный
  контракт и обязательная Parallel Decomposition Matrix перед
  делегированием. Сверху — Beads как трекер задач и Superpowers
  как процессные skill.

  Что это даёт на практике:
  — параллельный запуск независимых streams, когда write zones
    не пересекаются;
  — видимые spawned subagents — можно кликнуть и зайти в
    каждого отдельного агента, полная наблюдаемость;
  — чистый контекст основного оркестратора: он диспетчер,
    а не исполнитель, токены тратятся только на координацию;
  — нулевой silent debt — закрытие этапа требует evidence.

  История того, как я к этому пришёл — полгода с большим
  AGENTS.md на 30 КБ, который не работал. Проблема была не в
  правилах, а в том, что одно полотно правил это не контракт,
  а эссе.

  В статье: фрагменты toml, шаблон worker-контракта, golden
  prompts, грабли с inline-делегированием. Архив со всеми 4
  скиллами прикладываю к посту в моём Telegram-канале — можно
  скачать и поставить себе.
---

# Собрал оркестратор для Codex на базе Beads и Superpowers — 4 skill, параллельные subagents, наблюдаемость. Архив прикладываю

В марте я писал на Хабре, как для Claude Code пришёл к связке Superpowers + Beads + Template Bridge и отказался от собственного Orchestrator Kit на 39 агентов — [3000+ часов в Claude Code](https://habr.com/ru/articles/1017110/). Там у меня была ровно одна мысль на финал: AI заменяет набивание символов, но не инженерию. Мультипликатор — он мультипликатор: умножает ноль на сотню — получает ноль; умножает грамотный контракт — получает результат.

Эту мысль я в марте написал. И полгода после этого аккуратно её игнорировал — уже в Codex.

В Codex у меня всё это время лежал один большой `AGENTS.md`. Реально один файл, килобайт на двадцать. Внутри были правила: использовать Beads для задач, не пропускать verification, спрашивать перед опасными операциями, при длинном этапе делегировать subagents. Я туда добавлял всё, на что натыкался. По вечерам казалось, что я строю надёжную систему.

Реальность была другая. Оркестратор уверенно прочитывал контракт, кивал, и дальше начинал тихо срезать углы. Расскажу как именно.

## Что значит «тихо срезать углы»

Сценарий простой. Я даю задачу: «Разнеси модуль X на два слоя, добавь регрессионный тест, проверь, что старые тесты не падают». В `AGENTS.md` записано: для medium/complex задач делегируй параллельно subagents в отдельных видимых run-ах, в каждом — свой write zone, в каждом — verification.

Оркестратор отвечает что-то в духе «хорошо, приступаю». Через полчаса я смотрю diff. Один большой коммит, всё сделано из главной сессии. Никаких subagents. Никакого параллелизма. Тест приклеен в файл с реализацией. Verification — «я запустил pytest, всё зелёное», без вывода в логе.

Я возвращаюсь, спрашиваю: «А почему не делегировал?». Ответ: «Задача показалась мне достаточно простой, чтобы выполнить локально». Формально не наврал. По духу контракта — наврал, потому что подменил «делегировать medium/complex» на «делегировать только когда я уверен, что не справлюсь».

Это и есть тихая глупость. Не баг модели. Не злая воля. Просто **расплывчатый контракт даёт агенту дофига свободы в интерпретации, и в среднем он выберет более лёгкий путь**. У меня в `AGENTS.md` не было ни одной механики, которая физически заставила бы его сначала построить таблицу streams, а потом уже принимать решение.

Полгода я думал, что у меня просто недописан AGENTS.md. Добавлю строжайшее правило — и заработает. Не работало. К концу марта файл вырос до тридцати с лишним килобайт, оркестратор всё так же делал «как удобнее». И на одном из таких diff-ов меня наконец накрыло: проблема не в правилах. Проблема в том, что одно полотно правил — это не контракт. Это эссе на тему «как было бы хорошо работать». Эссе никто не исполняет.

## Главный тезис: оркестратор — это диспетчер контрактов

Простая формулировка, которая мне самому стоила нескольких месяцев:

> Оркестратор не должен быть самым умным промптом. Он должен быть диспетчером контрактов.

Под «контрактом» я имею в виду буквально вот это: жёсткая структура, в которой записано — что именно сейчас происходит, кто это делает, в какой write zone, как проверим, когда стоп. Без неё оркестратор всегда найдёт способ сделать работу проще, чем планировал я.

Из мартовской статьи я тогда вытащил для Claude Code совсем не то, что нужно было вытащить. Я взял идею «интегрировать готовое вместо своего» — поставил Superpowers, Beads, Template Bridge, удалил Orchestrator Kit, написал статью. Полгода был доволен. А по-настоящему важная мысль про мультипликатор пролежала рядом и не сработала, потому что в Codex я её не приземлил. Контракта на агента не было — он умножал свою сотню на расплывчатый ноль и выдавал ноль красиво.

В Claude Code я ушёл к интеграции готового. В Codex с этим хуже — экосистема скиллов и плагинов пока тоньше, готового collaborative-workflow нет. Пришлось собирать своё, но уже не как один большой промпт, а как маленькую систему из четырёх отдельных skill.

## Четыре skill вместо одного полотна

Сейчас у меня в `~/.agents/skills/` лежат четыре связанных skill. Каждый — со своим `SKILL.md`, своими шаблонами, своими support-скриптами. Между собой они общаются через файлы в `.codex/` и через Beads.

| Skill | Когда срабатывает | Что делает |
|---|---|---|
| `orchestration-setup` | Новый проект, или ауд драфта | Создаёт repo-local baseline: AGENTS.md, `.codex/orchestrator.toml`, handoff, шаблоны, support scripts. Проверяет drift. |
| `orchestrator-stage` | Активная работа над medium/complex задачей | Читает baseline, выбирает Beads task, строит Parallel Decomposition Matrix, запускает subagents, ревьюит. |
| `task-router` | Substep внутри stage | Подбирает актуальные docs, нужные skills, нужных custom agents. Не заменяет процесс — только маршрутизирует. |
| `orchestration-closeout` | Конец этапа | Проверяет accepted artifacts, гоняет verification, обновляет Beads и handoff, чистит worktrees/branches. |

Логика разделения: lifecycle проекта (setup), lifecycle этапа (stage), routing внутри этапа (router), безопасное закрытие (closeout). Это разные режимы мышления — и смешивать их в одном `AGENTS.md` примерно так же плохо, как держать одну функцию длиной 2000 строк, потому что «всё связано».

Самый ценный — `orchestration-closeout`. Когда я отдельным skill сделал закрытие этапа, у меня закончились silent debt. До этого я ловил остатки от субагентов через неделю: открываешь репо, видишь странный worktree, не помнишь зачем он. Сейчас этап нельзя закрыть, не пройдя evidence-checks.

(Кстати, эта же логика — почему в Anthropic для Claude Code появились отдельные skills вроде `verification-before-completion` и `using-git-worktrees` вместо одного «Engineering CLAUDE.md». Лучшая структура — несколько мелких контрактов, активирующихся по контексту, а не один большой эссе.)

## Repo-local baseline: `.codex/orchestrator.toml` и компактный AGENTS.md

`AGENTS.md` я не удалил. Я его сильно усохнул. Теперь он стал human-facing и короткий:

- как устроен проект;
- какие entrypoints;
- какие verification commands;
- где состояние;
- когда использовать orchestration;
- что Beads = task truth;
- что Superpowers обязательны.

Всё остальное переехало в `.codex/orchestrator.toml` — это уже machine-readable контракт. Вот фрагмент из текущего baseline (`balanced-v2.12`):

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

Два поля, которые поменяли мою жизнь больше всего: `inline_subagents_allowed = false` и `parallel_decomposition_matrix = "required_for_medium_complex"`. Про оба ниже отдельно.

Структура `.codex/` рядом:

```text
AGENTS.md
.codex/
  orchestrator.toml      # machine-readable контракт
  handoff.md             # ТОЛЬКО текущее состояние, не история
  project-index.md       # стабильная карта проекта
  stage-artifact-template.md
  subagent-task-contract.md
  stages/                # история этапов: summary, artifacts, evidence
scripts/orchestration/
  run_process_verification.sh
  validate_artifact.py
  check_stage_ready.py
  run_stage_closeout.py
  cleanup_stage_workspace.py
  report_child_completion.py
  review_completion_inbox.py
```

Главная дисциплина здесь — **`handoff.md` не должен становиться историей**. Это файл «где я сейчас и что дальше», два-три абзаца. История этапов уходит в `.codex/stages/` — туда складываются summary, accepted/rejected artifacts, verification evidence, явные defers. Промежуточное состояние между «всё в чате» и «ничего не сохраняем». Через месяц можно открыть конкретный stage и увидеть, почему именно этот stream выделили в отдельный worktree.

## Parallel Decomposition Matrix: обязательный этап перед делегированием

Это центральная штука. До неё параллелизм у меня был декоративным: оркестратор писал «запускаю s1 и s2 параллельно», а на деле подразумевал «сделаю s1, потом s2». После — параллелизм стал настоящим.

Правило в `orchestrator-stage`: до старта реализации medium/complex задачи оркестратор обязан построить таблицу. Не «обдумать декомпозицию», а конкретно — таблицу с полями.

| Stream | Goal | Agent | Write zone | Dependencies | Verification | Model/reasoning | Decision | Reason |
|---|---|---|---|---|---|---|---|---|
| `s1` | Изменить backend contract | `worker` | `src/api/*` | none | `pytest tests/api` | inherit/high | parallel | isolated write zone |
| `s2` | Обновить UI state | `worker` | `frontend/*` | waits for s1 schema | `pnpm test` | inherit/medium | sequential | depends on s1 contract |
| `s3` | Проверить API docs | `docs_researcher` | read-only | none | source citation | role_default | parallel | read-only |

Дальше — простое правило: **если есть два или более independent streams и subagents разрешены, оркестратор должен запускать их параллельно**. Sequential допустим только с конкретной причиной.

И вот эти «причины» — отдельная тема. Раньше оркестратор писал «решил сделать последовательно, потому что файлы связаны». Это плохая причина — почти всегда означает «мне лень». Сейчас в контракте есть список приемлемых причин:

- dependency chain (s2 правда ждёт схему от s1);
- write conflict (оба stream трогают один файл);
- shared verification bottleneck (тестовый цикл неразделим);
- shared external resource (один внешний API с rate limit);
- uncertain scope (ещё непонятно, во что превратится stream);
- repo limit (политика репо запрещает параллельные изменения в этой зоне).

«Файлы связаны» — отсутствует. Если не подпадает ни под одну причину — параллелим.

Реальный кейс из прошлого этапа на одном из моих проектов. Я отдавал на параллель три стрима: backend-контракт, UI-стейт, обновление docs. Backend и docs запустились параллельно. UI — сделали sequential после backend. Причина в матрице была записана так: «stream s1 (backend) меняет shape ответа API, stream s2 (UI) расходует этот shape для типизации — sequential, потому что без стабильного contract из s1 типы будут переписываться дважды». Это нормальная причина. Когда я её прочитал в матрице, я согласился.

А в начале этого года я бы получил то же самое — но без матрицы, и без причины. Просто всё было бы sequential, и я бы потом неделю не понимал, почему «параллельная разработка» не ускоряет.

(Кстати, это очень напоминает классическую историю с микросервисами. Параллельная разработка без disjoint write zones — это не ускорение, это генератор merge-конфликтов. Тот же эффект, что у людей с микросервисами без bounded contexts. Архитектурные ошибки повторяются на новом уровне абстракции, только теперь между не людьми, а агентами.)

## Subagents — только видимые spawned, и тот самый промт авторизации

Тут самая важная сюжетная развилка. Расскажу с самого начала.

Когда я начинал ковырять delegation в Codex, я делал её руками. Codex давал мне готовый промт-пакет для subagent, я открывал отдельную сессию, копировал, запускал, потом возвращался с результатом, ревьюил. Утомительно, но я видел всё своими глазами: вот отдельный run, вот его лог, вот его diff. Наблюдаемость — стопроцентная.

Codex со временем сделал кликабельных видимых spawned subagents: когда оркестратор делегирует задачу, в интерфейсе появляется отдельный run с именем агента, в него можно зайти, посмотреть его контекст и его действия. Это закрыло почти весь мой manual fallback — наблюдаемости через UI хватает.

Но я наступил на одни грабли, и теперь не отступаю от формулы. Если в стартовом промте задачи нет прямого разрешения на spawned subagents — Codex имеет право делегировать **inline**, то есть продолжать работу в той же сессии под видом «я тут думаю», без отдельного run-а. Я узнаю об этом только по diff-у, постфактум.

После одного такого случая я сделал две вещи. Первая — записал в `.codex/orchestrator.toml`:

```toml
inline_subagents_allowed = false
requires_explicit_user_spawn_request = true
```

Вторая — в стартовом промте каждой большой задачи теперь живёт ровно одна и та же фраза:

```text
I explicitly authorize you in this current task to spawn separate
visible Codex subagents when justified. Do not use inline-only delegation.
```

Эта фраза работает по двум причинам. Первая — Codex по документации требует явного user request для spawning subagents, потому что это «новый процесс», и они не хотят, чтобы агент запускал агентов на свой страх и риск. Без фразы — formally агент может legally не запускать subagents и делать всё локально. Вторая — фраза мгновенно решает спор «инлайн или нет». Не «когда сочтёшь нужным, можешь делегировать», а «делегируй, и делай это видимым».

Нет, подождите. Не совсем «всегда». У меня осталась одна песочница, где manual fallback живёт до сих пор. Там runtime сам по себе режет spawning (его развернули в режиме «без вложенных процессов»), и приходится возвращаться к ручным prompt pack-ам. Manual fallback есть в `orchestration-setup` как отдельный шаблон именно для таких случаев. Но дисциплина не меняется: даже manual prompt должен содержать Beads task, docs, asset routing, write zone, verification, stop rules. Manual не значит халтурно.

Я долго не верил, что простая фраза в стартовом промте может что-то менять. Считал, что если у меня в repo contract всё прописано — runtime должен слушаться. Не должен. Runtime слушается user в текущей сессии, не репозиторий. Урок выученный, дорогой.

## Worker contract: расплывчатой задачи мало

Когда оркестратор spawned subagent — он не должен говорить ему «посмотри и сделай». Worker должен получить контракт с минимальным набором блоков. Вот реальная форма из шаблона `subagent-task-contract.md`:

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
- Loader handles empty state
- Existing graph tests still pass
- New regression test covers missing headings

## Documentation
- No dependency documentation lookup needed

## Asset Routing
- Selected docs: none — repo-local behavior
- Selected skills: superpowers:test-driven-development
- Selected agents/personas: worker
- Catalog candidates: none — installed assets sufficient

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

Зачем такая бюрократия. Каждое поле закрывает один конкретный класс «тихой глупости» субагента.

`Write zone` — закрывает «случайно влезу в чужой файл и сломаю sibling-стрим». `Stop rules` — закрывает «увлекусь и переделаю архитектуру вместо того, чтобы вернуть blocked». `Verification` — закрывает «скажу, что прошло, не запустив». `Asset Routing` — закрывает «потрачу 20 минут на повторное catalog discovery». `Parallel group` — закрывает «не пойму, что я не одинок, и накачу свой подход на тот же файл».

Это всё не про недоверие к субагенту. Это про то, что **расплывчатую задачу честный субагент тоже выполнит расплывчато**. Нечего ему делать.

## Completion event ≠ acceptance

Subagent вернулся с результатом. В систему упало событие completion: `report_child_completion.py` записал в inbox, что worker отчитался. Это **не значит, что работа принята**.

В прошлой статье я писал про скилл `verification-before-completion` от Superpowers: «доказательства до утверждений». В Codex я ту же идею протащил на уровень целого этапа — там разделены четыре сущности:

- **completion event** — «worker вернулся»;
- **artifact** — «что worker утверждает»;
- **orchestrator review** — «принято или нет»;
- **local verification** — «доказано или нет».

Я несколько раз обжигался ровно на разнице между первым и последним. Subagent возвращался, оркестратор пожимал плечами «ну тесты у него зелёные, наверное», и принимал stream. Потом на closeout выяснялось, что worker запустил один тестовый файл, а не весь pytest suite. Stream формально принят, но verification — фуфло.

Сейчас artifact обязан фиксировать verification — какую команду запустили, какой вывод получили. `accepted_by_orchestrator: yes` нельзя поставить без verification evidence. На closeout эту цепочку ещё раз проверяет `run_stage_closeout.py`. Это не паранойя — это просто закрытие очевидной дыры, через которую агент с удовольствием тихо проскальзывал.

## Что я убрал и почему: Beads hooks

В прошлой статье я хвалил `bd prime` hook на старте сессии Claude Code: новая сессия — автоматически подтягиваются текущие задачи из Beads. Удобно.

В Codex я тот же подход поначалу пытался воспроизвести через hook-и. И вот тут поймал классическую боль: «вчера работало, сегодня не работает, никаких изменений». Hook не сработал из-за порядка инициализации. Hook не сработал в worktree. Hook не сработал в режиме `--ask-for-approval`. Каждый раз я тратил минут двадцать на «а почему».

Решение — взять и убрать hook вообще. Теперь оркестратор работает с Beads явными командами: `bd ready`, `bd create`, `bd update --claim`. Никакой магии на старте, никакого автоматического подтягивания. Кажется хуже — на деле:

- меньше скрытого поведения;
- проще перенести между средами;
- легче объяснить новому агенту;
- никаких «а почему сработало вчера».

Я честно колебался. Hook давал ощущение «всё само». Но иллюзия «всё само» обходилась мне дорого — отлаживать невидимую инициализацию хуже, чем явно написать одну строчку в начале промта. Прагматичная инженерия здесь оказалась честнее, чем элегантная автоматизация.

## Где система проигрывает manual fallback

Не буду делать вид, что новая система — серебряная пуля. Несколько честных мест.

**Стоимость на маленькие задачи.** Если задача правда простая (исправить опечатку, переименовать переменную) — вся эта обвязка только тормозит. В `orchestrator-stage` есть классификация: для simple задач оркестратор делает всё локально, без церемонии. Но граница между simple и medium субъективная — пару раз оркестратор отнёс к simple то, что я считал medium. Тут оркестратор всё ещё умнее меня примерно в 90% случаев и тупее меня примерно в 10%.

**Среды, где spawning не работает.** Если runtime запущен в режиме без вложенных subagents — система деградирует до manual fallback, и часть ускорения теряется. Manual prompt pack у меня есть, он остаётся валидным контрактом, но скорость падает примерно вдвое.

**Старые worktree-копии не обновляются автоматически.** Я обновляю baseline в основном репо, но старые временные worktree остаются на предыдущей версии. Это нормально, но требует помнить: closeout должен идти из основного worktree.

**Custom agents — пока пустовато.** Built-in роли (`worker`, `explorer`, `docs_researcher`, `skill_scout`) покрывают примерно 80% задач. Но реально полезные специализации (`reviewer`, `architect`, `security-reviewer`, `migration-specialist`) я пока не оформил как полноценных custom agents. Это в roadmap, но не сейчас.

## Куда буду двигаться дальше

Главное, что хочется добавить — **поведенческие проверки** оркестратора. Сейчас `audit_repo.py` проверяет, что нужные файлы и поля на месте. Это структурная валидация. А мне нужны pressure-сценарии: задаю оркестратору medium/complex задачу — проверяю, что он построил Parallel Decomposition Matrix. Даю две независимые подзадачи — проверяю, что он реально spawn-ил параллельно, а не делегировал inline. Делаю completion без verification evidence — проверяю, что closeout его отклонил.

По сути — TDD для процесса оркестрации. Тесты не для модели (она и так делает что может), а для самих контрактов: где у них дырки, где агент проскальзывает.

Второе — **stage dashboard**. Сейчас состояние этапа размазано между Beads, `.codex/handoff.md`, `.codex/stages/`, completion inbox, git worktrees. Один CLI, который показывает «вот текущий этап, вот его streams, вот их статусы, вот dirty worktrees, вот безопасно удалить» — это сделает систему сильно наблюдаемее. Пока обхожусь `git worktree list` и `bd ready`, но это руками.

## Архив скиллов и контакты

Все четыре skill в одном zip-архиве приложу к посту в моём Telegram-канале — [t.me/maslennikovigor](https://t.me/maslennikovigor). Положил туда же `README.md` с инструкцией: куда распаковать, что нужно поставить рядом (Beads, Superpowers), какие поля настроить под свой репо. Baseline — `balanced-v2.12`, срез на сегодня. Через полгода что-то наверняка поменяется в Codex — обновлю baseline и выложу новую версию в тот же канал.

Если будут вопросы или замечания по контракту — пишите в [@maslennikovig](https://t.me/maslennikovig). GitHub с Claude Code-версией орк-кита — [maslennikov-ig/claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) (это та самая система, от которой я отказался в марте; оставил как MIT для тех, кому нужен полный контроль и стабильный стек). Codex-версия — отдельный архив в Telegram, открытого репо под неё пока нет.

И последнее — то, ради чего я вообще писал статью. Если есть один тезис, который стоит унести с собой: **система работает не потому, что агент умнее. Она работает потому, что агенту стало тяжелее сделать тихую глупость**. Каждое поле в `orchestrator.toml`, каждая ячейка в Parallel Decomposition Matrix, каждый блок в worker-контракте — это закрытая дырка, через которую агент раньше проскальзывал. AI как мультипликатор работает только когда у него по обе стороны умножения стоит что-то, отличное от нуля. Контракт — это и есть то самое «что-то».
