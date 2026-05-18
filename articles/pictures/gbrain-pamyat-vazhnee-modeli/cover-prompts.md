# Промпты для обложек: gbrain — память важнее модели

Обложки к статье `articles/habr/gbrain-pamyat-vazhnee-modeli.md`. Тема — архитектурный разбор open-source системы памяти gbrain от CEO Y Combinator + позиция «контекст важнее модели». Поддерживаются Whisk, Midjourney v6/v7, Imagen 3, FLUX.

После генерации — складываем готовые PNG в эту же папку. Анжела возьмёт отсюда нужную для каждой платформы.

---

## Prompt 1: «Память важнее модели» (главный insight) ★★★★★

```
A wide editorial illustration, 16:9, in a clean modern tech-magazine style.
Two side-by-side scenes separated by a thin vertical line.

Left scene (labeled "Слабая модель + правильный контекст"):
A small, modest-looking robot in matte gray sitting calmly with confidence.
Connected to it is a rich, glowing knowledge graph — many nodes (some labeled
"person", "company", "concept" in cyrillic), neat colored edges, organized
structure. The robot looks small but the graph is luminous and deep.
Small label below: "Точный ответ".

Right scene (labeled "Сильная модель + мусорный контекст"):
A huge, bulky robot in chrome/metallic finish, looking powerful but confused.
Around it: a chaotic cloud of disconnected data fragments, broken edges,
scattered orphan nodes, faded text. The robot is large but lost in noise.
Small label below: "Шумный ответ".

Above the whole composition, a centered headline in cyrillic:
"Контекст важнее модели"

Color palette: deep navy background, cyan + amber accents for the graph,
muted gray for the chaos side. No real people. No real company logos.
Style: editorial illustration with subtle gradient lighting, clean lines,
no photorealism.
```

**Когда использовать:** Универсал для Хабра + анонс в Telegram. Передаёт центральный тезис статьи без раскрытия деталей gbrain. Хорошо работает в ленте Хабра — глаз цепляется за контраст и за слоган «Контекст важнее модели».

---

## Prompt 2: Гибридный поиск + цифра бенчмарка ★★★★★

```
A clean technical data-visualization illustration, 16:9, dark editorial style.

Center: a horizontal stacked bar chart titled in cyrillic:
"Precision@5 на 240-страничном корпусе — gbrain"

Three bars from top to bottom:
1. Top bar (longest, glowing gold-amber with subtle shimmer): label "gbrain
   (hybrid + graph)" — value "49.1%"
2. Middle bar (medium length, neutral cyan): label "vector-only RAG" — value
   "~18%"
3. Bottom bar (shortest, muted gray): label "ripgrep + BM25" — value "~17%"

Above the chart, a small inset diagram showing three signal sources flowing
into one fusion box:
  - Box 1 labeled "Vector (HNSW)"
  - Box 2 labeled "BM25 / tsvector"
  - Box 3 labeled "Backlink boost"
  All three arrows flow into a central box labeled "RRF"
  One arrow exits to the right, labeled in cyrillic "Финальный ранг"

Below the bar chart, a single line in cyrillic:
"Графовый слой даёт +31 пункт P@5 над vector-only"

Color palette: very dark navy / near-black background, glowing accent colors
(amber, cyan, magenta), clean monospace-like sans-serif font. Style:
information-design / dashboard aesthetic, NOT cartoon. No people. No logos.
```

**Когда использовать:** Хабр (главная обложка — сразу обещает технику и цифры) + VC.ru. Менее эмоциональная, но более «давай по делу» — Хабр такое уважает.

---

## Prompt 3: Самоплетущийся граф знаний ★★★★☆

```
A wide cinematic illustration, 16:9, semi-abstract editorial style.

Center composition: a large, complex knowledge graph that appears to be
"weaving itself" — animated motion-blur lines spreading from a few seed nodes
outward, creating new typed edges between them. The motion suggests
self-organization, no human hand visible.

Nodes are labeled (in latin script, technical identifiers):
- Person nodes: "Pedro Franceschi", "Bob McGrew", "Jordan"
- Company nodes: "Brex", "Anthropic", "Acme AI"
- Concept nodes: "Founder Mode", "Do Things That Dont Scale"

Edges between them carry typed labels in monospace font (latin, technical):
"works_at", "founded", "invested_in", "attended", "advises"

The graph has a clear "growing" sense — partial edges still forming on the
right side of the frame, faint dashed lines suggesting future links.

In the top-left corner, a small clean text panel in cyrillic:
"Граф плетёт себя сам. Без единого вызова LLM."

In the bottom-right corner, smaller monospace text in latin:
"intent classifier: 87% deterministic"

Color palette: dark navy/space background, electric cyan and warm amber
lines, faint pinkish glow around active nodes. Style: data-art / generative
network visualization, like Refik Anadol but cleaner. No real people's faces.
No real company logos rendered visually — only labels as text.
```

**Когда использовать:** Альтернативная обложка для Хабра (если первая или вторая не зайдут) + Telegraph + TenChat. Передаёт самую крутую техническую фишку статьи — self-wiring graph без LLM. Работает на аудиторию, которая видит много обложек с «AI-роботами» и хочет увидеть что-то про сам граф.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG, sRGB
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон (navy/чёрный) + неоновые акценты (cyan, amber, magenta), один сильный акцентный цвет на иллюстрацию
- **Текст на изображении:** **на русском** для слоганов и заголовков; на латинице — только имена сущностей (`works_at`, `Brex`, `Anthropic`), цифры (`P@5`, `49.1%`, `17K`), технические идентификаторы (`RRF`, `HNSW`, `tsvector`)

## Что НЕ нужно генерировать

- Логотипы реальных компаний — только generic robot/AI characters / abstract designs
- Фото Garry Tan или других реальных людей (даже если упомянуты в статье)
- Confused / sad faces у роботов — мы анализируем, не критикуем
- Маркетинговые баннеры со словами «революция», «прорыв», «изменит мир»
- Текст на английском там, где русский был бы естественнее
- Иконки YC / Y Combinator (это товарный знак)

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 2 (data viz) или Prompt 1 (insight) | 16:9 (превью в ленте) |
| Telegram анонс | Prompt 1 (слоган «Контекст важнее модели») | 16:9 или квадрат, читается на мобильном |
| Telegraph | Prompt 3 (граф) | 16:9 |
| TenChat | Prompt 2 (data viz) | 4:3 или 16:9 |
| VC.ru | Prompt 2 (data viz) | 16:9 |
