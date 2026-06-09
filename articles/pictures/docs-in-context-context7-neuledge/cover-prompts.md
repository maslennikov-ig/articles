# Промпты для обложек: бенчмарк docs-in-context и бесплатная связка вместо Context7

Обложки к статье [`articles/habr/docs-in-context-context7-neuledge.md`](../../habr/docs-in-context-context7-neuledge.md) — «Context7 — стандарт для доков AI-агента. Я измерил 8 альтернатив и собрал бесплатную связку».

Промты на английском (генераторы лучше понимают), но **весь читаемый текст НА самой картинке — на русском**, кроме имён инструментов (`Context7`, `@neuledge`, `Ref`, `GitMCP`), идентификаторов кода (`z.email()`, `L1`, `L2`) и чисел/единиц (`5 мс`, `~3000 мс`, `1000/мес`, `$0`). Поддерживаются Whisk / Midjourney / Imagen.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/docs-in-context-context7-neuledge/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Двухуровневая связка — платишь один раз за либу ★★★★★

```
A clean two-tier "plumbing" diagram on a dark background, editorial tech illustration, 16:9.
Top: a wide stream of documentation queries (small glowing doc icons) flows DOWN into a large
local cube labeled "@neuledge — L1" glowing green, stamped with a Russian caption "локальный · 5 мс · $0".
Most queries resolve instantly inside this green cube (a small Russian label below: "0% fallback").
A thin overflow stream of only NEW unknown libraries spills over into a smaller amber meter labeled
"Context7 — L2", with a gauge reading "1000/мес" and a Russian caption "fallback · только новые либы".
A looping arrow takes each new library from the amber L2 tier and drops it permanently down into the
green L1 cube — with a short Russian caption on the arrow: "добавил один раз — больше не платишь".
Big bold Russian title at the top: "Бесплатная связка: локальный L1 + Context7 как fallback".
Color palette: dark navy background, neon teal/green for the free local tier, warm amber for the metered tier.
No company logos, no faces, no text in English except the identifiers @neuledge / Context7 / L1 / L2.
```

**Когда использовать:** главная обложка статьи (Habr, превью в ленте) и Telegram-анонс. Передаёт ключевой insight — двухуровневую связку и механизм «платишь один раз за новую либу».

---

## Prompt 2: Локальная молния — 5 мс против 3 секунд ★★★★★

```
A speed-contrast editorial illustration, dark background, 16:9.
LEFT side: a small local cube on a developer's desk labeled "@neuledge" emitting a bright lightning bolt,
with a large glowing Russian-friendly readout "5 мс" and a Russian caption underneath "локально, без сети, без лимитов".
RIGHT side: distant slow cloud servers lagging behind, a dim spinner, a readout "~3000 мс" and a Russian
caption "облако: ждёшь каждый вызов". A progress label morphs from a dim "57%" into a bright "100%" near
the local cube, with three tiny bug icons being swept away. Big bold Russian title across the top:
"В сотни раз быстрее — и агент сверяется с доками постоянно".
Visual mood: warm on-device glow on the left, cold sluggish cloud on the right; emphasize the speed gap.
Color palette: dark background, electric blue + teal accents. No logos, no faces, no English except @neuledge / мс identifiers.
```

**Когда использовать:** Habr+TenChat как вторая обложка (акцент на скорость — то, что автор отдельно подчёркивает). Хорошо заходит в Telegram как короткий «вау»-кадр.

---

## Prompt 3: Одна линейка, а не лендинги — 8 инструментов на замере ★★★★★

```
A row of eight different "documentation delivery machines" of varied shapes and sizes, each feeding glowing
tokens into a single AI agent's context window, dark editorial tech illustration, 16:9.
A single unified measuring ruler / gauge runs horizontally across all eight machines, emphasizing one common
scale. Each machine has a small Russian-friendly name tag: "Ref", "Context7", "@neuledge", "GitMCP", "WebFetch".
In the corner, discarded glossy "vendor landing-page" billboards with inflated numbers ("90%!") lie crossed
out on the floor. Big bold Russian title at the top: "Мерил одной линейкой, а не цифрами с лендингов".
A small Russian sub-caption: "8 способов кормить доки AI-агенту — на одном токенайзере".
Color palette: dark background, neon teal accent for the ruler, muted greys for the discarded billboards.
No company logos, no faces, no English text except the tool names and "90%".
```

**Когда использовать:** обложка для углов «исследование / методология / сравнение». Подходит Habr и VC, где ценят дисциплину измерения. Передаёт сам жанр статьи — честный бенчмарк.

---

## Prompt 4 (бонус): Виноват был мой вызов — детектив ★★★★☆

```
A noir-tech detective scene, dark background, 16:9.
A generic robot character labeled "ctx7 CLI" stands under a spotlight with a Russian sign "79% — подозреваемый".
A magnifying glass reveals the real culprit: a mislabeled input wire that the engineer himself connected wrong
(a small Russian tag on the wire: "весь вопрос ушёл в поле имени"). The verdict flips to a glowing Russian
banner "93% — невиновен". Big bold Russian caption at the bottom: "Дважды я винил инструмент — дважды виноват был мой вызов".
Color palette: dark noir, electric-blue spotlight, single amber accent on the magnifying glass.
Self-aware, slightly humorous mood. No logos, no human faces (engineer only as hands/silhouette), no confused robot faces.
English only in the identifier "ctx7 CLI" and the percentages.
```

**Когда использовать:** Pikabu и Telegram — эмоционально-вовлекающая, самоироничная версия. Хороша там, где заходит признание фейла, а не сухой бенчмарк.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** editorial / data-viz иллюстрация, без фотореализма людей, без распознаваемых лиц
- **Цветовая палитра:** тёмный фон + неоновые акценты (teal/green для бесплатного локального слоя, amber для платного)
- **Текст на изображении:** **на русском**, кроме имён инструментов (`Context7`, `@neuledge`, `Ref`, `GitMCP`, `ctx7`), идентификаторов (`L1`, `L2`, `z.email()`) и чисел/единиц (`5 мс`, `~3000 мс`, `1000/мес`, `$0`, `79%`, `93%`, `100%`)

## Что НЕ нужно генерировать

- Логотипы реальных компаний (Upstash, Vercel, Anthropic) — только generic-машины и абстрактные кубы
- Фото реальных людей (автора не визуализируем; инженер — только руки/силуэт)
- Confused / sad faces у роботов-инструментов — мы анализируем, не унижаем
- Маркетинговые баннеры с кучей текста
- Английский текст там, где русский естественнее (русская статья, русская аудитория)

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (связка) или Prompt 3 (линейка) | 16:9 (превью в ленте) |
| Pikabu | Prompt 4 (детектив) | Квадрат или 16:9 |
| TenChat | Prompt 2 (скорость) или Prompt 1 | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 (связка) или Prompt 2 (скорость) | Любой, главное — читается на мобильном |
