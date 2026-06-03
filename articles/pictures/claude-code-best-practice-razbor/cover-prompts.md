# Промпты для обложек: разбор claude-code-best-practice

Генерируем обложки к статье [«Топ-советы по Claude Code от Бориса Черни и не только»](../../habr/claude-code-best-practice-razbor.md). Поддерживаются Whisk / Midjourney / Imagen / любой text-to-image. Текст на самих картинках — на русском (кроме имён продуктов и идентификаторов).

Обложки генерирует сам автор (Игорь). Готовые PNG складываются в эту же папку (`articles/pictures/claude-code-best-practice-razbor/`) — Анжела берёт оттуда нужную для каждой платформы.

---

## Prompt 1: Карта территории и исследователь ★★★★★

```
A wide editorial illustration, 16:9. A vast glowing topographic map spread across
the frame, drawn like an old explorer's atlas but made of circuit traces and code
lines. Distinct labeled regions/nodes are connected by glowing paths. Node labels
are in Russian, clearly legible: «Оркестрация», «Индексация кода», «Память агентов»,
«Поиск», «Скиллы», «Хуки». A single small lone explorer figure (generic silhouette,
no recognizable face) stands on the map holding a lantern, with a trail of footprints
showing the paths actually walked. Title text at top, in Russian: «Карта экосистемы
Claude Code». Deep navy background, warm gold and amber glowing lines, subtle paper
texture. Mood: discovery, depth, quiet confidence. No company logos, no real faces,
no marketing banners.
```

**Когда использовать:** универсальная обложка для Habr (превью в ленте) и Telegram-анонса. Прямо передаёт главную рамку статьи — «репо это карта, по которой я ходил». Самый «спокойный» и при этом цепляющий вариант.

---

## Prompt 2: grep + структура = один гибрид ★★★★★

```
A clean editorial data-viz illustration, 16:9, dark background. Center: two stylized
search icons merging into one. On the left, a magnifying glass labeled «grep»; on the
right, a connected node-graph labeled «Graphify». They join in the middle into a single
glowing symbol, like two halves becoming one. Below them, a minimal horizontal bar chart
with two bars showing growth, labeled in Russian: «точность поиска: 60% → 85% (гибрид)».
A small caption ribbon in Russian reads: «RAG не умер — просто ставили не туда». Identifiers
grep, Graphify, RAG, BM25 stay in latin/as-is; all human-readable labels in Russian.
Palette: dark slate + electric blue + amber accent. Precise, technical, no clutter,
no faces, no logos.
```

**Когда использовать:** для тех, кто хочет «инженерную» обложку — отлично заходит как иллюстрация к кульминации (спор про поиск). Подходит для Habr и для TenChat-инфографики. Делает заголовок-статью наглядным одним кадром.

---

## Prompt 3: Архитектуру выбрали «по ощущениям» ★★★★☆

```
A wry editorial illustration, 16:9. A huge, serious, monumental server/decision machine
(generic, no brand, no logos) dominates the frame, covered in dials and a single giant
lever. On the lever hangs one tiny bright-yellow sticky note with handwritten Russian text:
«по ощущениям». A small generic robot character stands beside the lever, shrugging, slightly
sheepish — not sad, not mocking, just honest. Title text at top in Russian: «Архитектуру
выбрали „по ощущениям"». Dark industrial background, dramatic spotlight on the sticky note,
warm amber highlight. Tone: ironic but affectionate, not ridiculing. No real faces,
no company logos.
```

**Когда использовать:** самый «человеческий» и вирусный кадр — для Pikabu и как альтернативный вариант для Telegram-анонса. Бьёт по эмоции «серьёзный гигант решает по ощущениям», которую любят шерить.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон (navy/slate) + тёплые золото/амбер + акцент электрик-блю
- **Текст на изображении:** **на русском**, кроме имён продуктов/идентификаторов (`grep`, `Graphify`, `RAG`, `BM25`, `Claude Code`)

## Что НЕ нужно генерировать

- Логотипы реальных компаний (Anthropic, GitHub и т.п.) — только generic-объекты
- Фото реальных людей (включая Бориса Черни — не визуализируем)
- Грустные/унижающие лица у роботов — мы анализируем, а не высмеиваем
- Маркетинговые баннеры с кучей текста
- Текст на английском там, где русский естественнее

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (карта) или Prompt 2 (гибрид) | 16:9 (превью в ленте) |
| Telegram анонс | Prompt 1 или Prompt 3 | Любой, читается на мобильном |
| Pikabu | Prompt 3 (метафора «по ощущениям») | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
