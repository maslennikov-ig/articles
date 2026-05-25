# Промпты для обложек: CodeGraph vs Graphify

Обложки к статье [`articles/habr/codegraph-vs-graphify.md`](../../habr/codegraph-vs-graphify.md) — сравнение двух систем индексации кода для AI-агентов. Промты на английском (технический язык генераторов), но **текст НА самой картинке — на русском**, кроме имён продуктов и технических идентификаторов. Поддерживаются Whisk / Midjourney / Imagen.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/codegraph-vs-graphify/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Два графа рядом — лёгкий индекс vs карта знаний ★★★★★

```
A clean editorial split-screen illustration, 16:9, dark technical background (deep navy #0d1b2a with subtle grid).

LEFT HALF — labeled in Russian "CodeGraph": a small, tight, glowing node graph of pure code symbols (functions, classes), nodes connected by clean lines, compact and fast-looking, neon cyan. A tiny SQLite/database glyph in the corner. Caption below in Russian: "Лёгкий индекс символов. 100% локально".

RIGHT HALF — labeled in Russian "Graphify": a much larger, richer, sprawling knowledge graph where code nodes mix with document icons (PDF, image, video glyphs), warm amber/gold palette, more sprawling and "knowledge map" feel. Caption below in Russian: "Граф знаний всего проекта".

A thin vertical divider between halves. Top title in Russian: "Один фундамент — разные задачи". Minimal, no faces, no real logos, editorial tech-magazine style, flat vector with soft glow.
```

**Когда использовать:** Универсальная обложка для Хабра — буквально передаёт главный тезис статьи (одинаковый фундамент tree-sitter, но разные инструменты). Лучший выбор для превью в ленте.

---

## Prompt 2: Контраст «веер чтений vs один запрос» (инфографика) ★★★★★

```
A data-viz style editorial illustration, 16:9, dark background (#11151c), neon accents.

LEFT side shows chaos: a robot/AI agent character (generic, friendly, no face details) surrounded by a messy fan of ~20 open file-document icons flying around it, tangled lines, a small counter in Russian reading "20 файлов прочитано" and "много tool calls", reddish-orange overwhelmed mood.

RIGHT side shows order: the same agent calmly pointing at a single clean node graph, one straight glowing line to the answer, a counter in Russian reading "1 запрос к индексу", calm green-cyan mood.

A bold arrow between them. Big title in Russian across the top: "Было / Стало". Small honest footnote in Russian at the bottom: "−57% токенов — цифры авторов CodeGraph". Flat vector infographic, clean, no real logos.
```

**Когда использовать:** TenChat и Хабр — инфографика «было/стало» хорошо заходит как иллюстрация боли. Цифра в футере честно помечена как vendor-цифра, в соответствии с тоном статьи.

---

## Prompt 3: Сценка — агент тонет в файлах ★★★★☆

```
A warm, slightly humorous editorial illustration, 16:9. A small generic robot/AI agent character (cute, no recognizable face) literally drowning in a tall avalanche of paper code files, only its hand reaching out holding a magnifying glass over ONE highlighted function. Above the pile, a glowing clean node-graph "lifeline" rope is being lowered toward it.

Caption in Russian at the bottom: "Поиск по коду без индекса". A small label on the glowing rope in Russian: "граф кода". Muted paper-beige avalanche, neon cyan rope graph as the bright focal point. Soft, story-driven mood, flat illustration, no real logos, no real people.
```

**Когда использовать:** Pikabu и Telegram-анонс — эмоционально-вовлекающая метафора, цепляет узнаваемостью боли («агент тонет в файлах»). Читается на мобильном.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** flat vector / editorial tech-illustration, без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный технический фон (navy/charcoal) + неоновые акценты (cyan для CodeGraph, amber/gold для Graphify)
- **Текст на изображении:** **на русском**, кроме имён продуктов (`CodeGraph`, `Graphify`, `SQLite`) и идентификаторов

## Что НЕ нужно генерировать

- Логотипы реальных компаний — только generic robot/AI characters и абстрактные графы
- Фото реальных людей
- Грустные/растерянные «лица» у систем — мы сравниваем, не критикуем (исключение — добрый юмор в Prompt 3)
- Маркетинговые баннеры с кучей текста
- Английский текст там, где русский естественнее (кроме имён продуктов и `SQLite`/`PDF`)
- Цифры без пометки источника — «−57%» только с подписью «цифры авторов CodeGraph»

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (различие систем) | 16:9 (превью в ленте) |
| Pikabu | Prompt 3 (сценка) | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика было/стало) | 4:3 или 16:9 |
| Telegram анонс | Prompt 3 (метафора, читается на мобильном) | Любой |
