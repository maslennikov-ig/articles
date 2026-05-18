# Промпты для обложек: Codex Orchestration Skills

Обложки для статьи `articles/habr/codex-orchestration-skills.md` — про систему из четырёх локальных skill для Codex (orchestration-setup / orchestrator-stage / task-router / orchestration-closeout) и почему один большой AGENTS.md не работает.

Поддерживаемые генераторы: Whisk, Midjourney, Imagen. После генерации — складываем готовые PNG в эту же папку (`articles/pictures/codex-orchestration-skills/`). Анжела возьмёт отсюда нужную для каждой платформы.

Текст на изображениях — **на русском** (кроме имён скиллов на латинице, идентификаторов и `AGENTS.md`).

---

## Prompt 1: Before/After — одно полотно vs четыре skill ★★★★★

```
A horizontal split editorial illustration, 16:9, dark navy background
with subtle blueprint grid lines.

LEFT HALF: a single huge crumpled scroll of paper labeled "AGENTS.md"
hanging from above, covered in dense Russian text fragments
("правила", "verification", "Beads", "subagents", "delegation"),
tilted, overflowing the frame. A small confused robot stands next to it
holding a magnifying glass. Tag below in Russian: "Одно полотно правил".

RIGHT HALF: four neat, glowing rectangular cards arranged in a 2x2 grid,
each card with a distinct accent color (teal, amber, magenta, lime).
Cards labeled in clean monospaced type:
  Card 1 (teal):    "orchestration-setup"  / subtitle in Russian: "baseline проекта"
  Card 2 (amber):   "orchestrator-stage"   / subtitle in Russian: "ведение этапа"
  Card 3 (magenta): "task-router"          / subtitle in Russian: "выбор инструментов"
  Card 4 (lime):    "orchestration-closeout" / subtitle in Russian: "закрытие этапа"
Thin neon lines connect the four cards to indicate they form a system.
Tag below in Russian: "Четыре skill вместо полотна".

Center divider: a thin vertical arrow pointing left-to-right.
Top title across both halves in Russian: "Оркестратор — диспетчер контрактов".

Style: editorial vector illustration, flat, slight grain texture,
high contrast, technical but warm. No photorealism, no real logos.
```

**Когда использовать:** Главная обложка для Хабра и Pikabu. Передаёт ключевой тезис статьи в одном кадре — отказ от единого полотна правил в пользу четырёх отдельных skill-контрактов. Универсальная.

---

## Prompt 2: Parallel Decomposition Matrix (data viz) ★★★★★

```
A clean technical diagram illustration, 16:9, deep charcoal background
with subtle dotted grid.

Center: a table styled like a Notion or Linear interface (rounded corners,
soft drop shadow) with the header in Russian:
"Parallel Decomposition Matrix".

Table columns headers in Russian (small monospaced caps):
"Stream | Цель | Write zone | Зависимости | Verification | Решение"

Three rows visible:
  Row 1 (highlighted green): "s1 | backend contract | src/api/* | нет | pytest | параллельно"
  Row 2 (highlighted amber): "s2 | UI state         | frontend/* | ждёт s1 | pnpm test | последовательно"
  Row 3 (highlighted green): "s3 | проверка docs    | read-only | нет | citation | параллельно"

To the right of the table — three minimalistic isometric "worktree" boxes
floating in space, each connected to the corresponding row by thin glowing
threads (green for s1 and s3, amber for s2 with a small wait icon).
Box 1 labeled "worktree-s1", box 2 "worktree-s2", box 3 "worktree-s3".

Bottom tag in Russian:
"Если write zones не пересекаются — параллелим."

Top-right corner small badge: "balanced-v2.12" in monospaced type.

Style: technical infographic, vector, minimalistic, slight neon glow on
the threads, no photorealism, no people, no real company logos.
```

**Когда использовать:** Хабр (превью в ленте — мгновенно сообщает «это серьёзный технический разбор»), TenChat (бизнес-аудитория ценит data viz). Идеальная иллюстрация для блока про Parallel Decomposition Matrix.

---

## Prompt 3: Диспетчер контрактов (метафора-сценка) ★★★★☆

```
A stylized isometric scene, 16:9, warm dark background (charcoal +
deep purple), soft cinematic lighting.

Center: a tall robot-conductor figure (clean geometric design, no human
face, friendly silhouette) standing behind a control desk made of glowing
glass panels. The conductor is holding a stack of four neat folders,
each folder labeled with a Russian word on its spine:
  Folder 1: "Цель"
  Folder 2: "Write zone"
  Folder 3: "Verification"
  Folder 4: "Stop"

In front of the conductor — three smaller robot figures (each a different
color: teal, amber, magenta), lined up to receive folders. Each smaller
robot has a small name-tag floating above it in Russian:
  Robot 1: "subagent s1"
  Robot 2: "subagent s2"
  Robot 3: "subagent s3"

Above the conductor in glowing soft type, Russian title:
"Диспетчер контрактов, не умный промпт".

Subtle floor pattern: a faint grid that fades to dark. No real company
logos, no real human faces, no text in English except agent IDs (s1/s2/s3).

Style: editorial isometric illustration, vector, modern flat-with-depth,
slight grain texture, warm color palette, evokes "production line of work"
not "scary AI takeover".
```

**Когда использовать:** Pikabu (любит метафорические сцены), Telegram-анонс (сразу передаёт суть без чтения подписи). Хорош для тех, кто скроллит ленту — метафора считывается за секунду.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080.
- **Формат:** PNG или JPG.
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью, без настоящих логотипов компаний (включая OpenAI/Anthropic).
- **Цветовая палитра:** тёмный фон (charcoal / deep navy / deep purple) + неоновые акценты (teal, amber, magenta, lime) — соответствует developer-tooling эстетике.
- **Текст на изображении:** **на русском**, кроме имён скиллов на латинице (`orchestration-setup`, `orchestrator-stage`, `task-router`, `orchestration-closeout`), идентификаторов (`s1/s2/s3`, `balanced-v2.12`, `AGENTS.md`, `pytest`, `pnpm test`) и технических терминов-калек (`worktree`, `write zone`, `verification` — но только если в контексте).

## Что НЕ нужно генерировать

- Логотипы OpenAI, Anthropic, Codex (как продукта) — только generic robot-фигуры.
- Фото реальных людей.
- Confused/sad/angry faces у роботов — мы анализируем систему, не критикуем агентов.
- Маркетинговые баннеры с кучей текста.
- Сцены «AI заменяет программиста» — позиция статьи WITH community, а не AGAINST.
- Текст на английском там, где русский был бы естественнее.

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (полотно vs 4 skill) | 16:9 для ленты |
| Habr (внутри статьи как иллюстрация Parallel Matrix) | Prompt 2 (data viz) | 16:9 |
| Pikabu | Prompt 3 (диспетчер) | 16:9 или 4:3 |
| TenChat | Prompt 2 (data viz) | 4:3 или 16:9 |
| Telegram-анонс к посту с zip-архивом | Prompt 1 или Prompt 3 | Любой, главное — читается на мобильном |
