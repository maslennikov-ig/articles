# Ядро Telegram-поста: ручная AI-оркестрация

## Публичное ядро поста

Выложил новый материал про то, почему я **не хочу делать полностью автономных AI-агентов** даже после всех последних улучшений в Claude Code, Codex и agentic workflow.

Короткий тезис:

**Проблема не в том, что агент может много делать сам. Проблема начинается, когда он сам себе менеджер, сам себе ревьюер и сам объявляет работу завершённой.**

В статье показал, почему я пришёл к другой схеме:
- `AGENTS.md` как главный portable contract
- `stage-orchestrator` для ведения работы по stage
- `orchestration-closeout` для финальных проверок, delivery и cleanup
- manual handoff и manual launch как осознанные контрольные точки, а не “лишняя ручная работа”

Ниже прикрепил **минимальный orchestration bundle**, который можно забрать себе в `Codex` или `Claude Code` и адаптировать под свой проект.

Внутри:
- пример `AGENTS.md`
- пример repo-local orchestration contract
- handoff
- artifact template
- verification / closeout / cleanup scripts

Статья: `[[ARTICLE_URL]]`  
Репозиторий: `[[REPOSITORY_URL]]`  
Канал: `[[TELEGRAM_CHANNEL_URL]]`

Если захотите, позже могу ещё отдельно выложить расширенный bundle со skill-файлами и полным baseline.

---

## Альтернативные варианты короткого поста

### Вариант 1 — жёстче

Я всё меньше верю в идею “полностью автономного AI-разработчика”.

Не потому, что модели слабые. А потому, что мне не нравится схема, где агент:
- сам выбирает, что делать,
- сам запускает работу,
- сам принимает собственный результат,
- сам объявляет stage завершённой.

Это не automation. Это потеря инженерных границ.

В статье разобрал, как я вместо этого устроил ручную AI-оркестрацию с `AGENTS.md`, stage handoff, closeout и cleanup.

Ниже прикрепил минимальный bundle файлов, который можно использовать как стартовую точку у себя.

Статья: `[[ARTICLE_URL]]`  
Репозиторий: `[[REPOSITORY_URL]]`

### Вариант 2 — мягче

Опубликовал материал про следующий этап моей работы с AI workflow.

После `Superpowers + Beads + Template Bridge` стало понятно, что одних плагинов недостаточно: всё ещё нужен тонкий orchestration layer, который отвечает за:
- stage handoff,
- review,
- closeout,
- cleanup,
- подготовку следующей orchestrator session.

В статье разложил, почему manual handoff и manual launch в таких системах часто лучше полной автономии.

Ниже прикрепил минимальный набор файлов, чтобы можно было попробовать это у себя.

Статья: `[[ARTICLE_URL]]`  
Репозиторий: `[[REPOSITORY_URL]]`

---

## Attachment checklist для ручного прикрепления

### Минимальный adoption bundle

В качестве canonical example repo рекомендую использовать `visa-light`, потому что он ближе всего к текущему shared baseline и хорошо показывает форму системы без лишних repo-specific усложнений.

Прикрепить:

- `/home/me/code/visa-light/AGENTS.md`
- `/home/me/code/visa-light/.codex/orchestrator.toml`
- `/home/me/code/visa-light/.codex/handoff.md`
- `/home/me/code/visa-light/.codex/stage-artifact-template.md`
- `/home/me/code/visa-light/scripts/orchestration/run_process_verification.sh`
- `/home/me/code/visa-light/scripts/orchestration/validate_artifact.py`
- `/home/me/code/visa-light/scripts/orchestration/run_stage_closeout.py`
- `/home/me/code/visa-light/scripts/orchestration/cleanup_stage_workspace.py`

### Опционально: skill files

Если захочешь приложить расширенный bundle, можно дополнительно прикрепить:

- `/home/me/.agents/skills/stage-orchestrator/SKILL.md`
- `/home/me/.agents/skills/orchestration-closeout/SKILL.md`
- `/home/me/.agents/skills/orchestration-setup/SKILL.md`

### Что лучше не прикладывать в Telegram напрямую

Чтобы пост не превратился в свалку вложений, лучше не прикладывать:

- все примеры из всех пяти репозиториев сразу
- research-файлы целиком
- исторические handoff/stage archives
- весь baseline целиком, если это уже удобнее читать из репозитория

Это лучше уводить в репозиторий и дать ссылку.

---

## Рекомендуемый порядок публикации

1. Выложить статью.
2. Сразу после этого опубликовать Telegram-пост.
3. В посте дать ссылку на статью и на репозиторий.
4. Прикрепить минимальный adoption bundle.
5. Если аудитории зайдёт тема, отдельным постом выложить extended bundle со skill-файлами.

---

## Напоминания перед публикацией

- Подставить вместо placeholders:
  - `[[ARTICLE_URL]]`
  - `[[REPOSITORY_URL]]`
  - `[[TELEGRAM_CHANNEL_URL]]`
- Проверить, что прикрепляемые файлы действительно те, которые хочешь публично показывать.
- Если какой-то файл слишком привязан к конкретному проекту, заменить его на более безопасный пример из того же baseline.
