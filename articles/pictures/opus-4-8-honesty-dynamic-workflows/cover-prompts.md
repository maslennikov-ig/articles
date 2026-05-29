# Промпты для обложек: Opus 4.8 — честность и Dynamic Workflows

Промты к статье `articles/habr/opus-4-8-honesty-dynamic-workflows.md` («Сотня параллельных субагентов бесполезна, если они врут. Главная цифра Opus 4.8 — не бенчмарк, а честность»). Поддерживаются Whisk / Midjourney / Imagen — промты на английском, текст НА картинке на русском (кроме имён моделей, дат и идентификаторов).

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/opus-4-8-honesty-dynamic-workflows/`). Анжела возьмёт оттуда нужную для каждой платформы.

**ВАЖНО:** ниже четыре промта. Первые три — варианты ОБЛОЖКИ (выбрать один). Четвёртый (`INLINE-1`) — это НЕ обложка, а перерисовка авторского графика «Разгон линейки Claude Opus» для вставки ВНУТРЬ статьи. Его надо сгенерировать обязательно и сохранить под именем `cadence-acceleration.png` — в теле статьи уже стоит ссылка ровно на это имя.

---

## Prompt 1: Честность делает авто-верификацию возможной ★★★★★

```
A 16:9 editorial tech illustration, flat-vector style with subtle film grain.
Center: one clean abstract geometric AI agent (faceless robot head made of
simple shapes) holding up a small red flag that reads, in Russian, "тут я не уверен".
Around the central agent: a ring of about eight identical but smaller agents,
connected to each other and to the center by thin glowing lines, each inspecting
a small fragment of code or a document through a magnifying glass — clearly a
peer-verification network checking one another's work.
Bold Russian title across the top: "Честность × сотня субагентов".
Smaller Russian caption along the bottom: "проверка работает, только если агент готов сказать «нет»".
Color palette: deep slate background (#0f172a), warm amber/orange accent glow on
the central honest agent, cool cyan lines for the verification network.
No brand logos. No human faces. No photorealism.
```

**Когда использовать:** универсальная обложка для Habr и Telegram-анонса — передаёт главный тезис статьи (честность как фундамент параллельной авто-проверки) одним кадром.

---

## Prompt 2: «В 4 раза реже» — инфографика-контраст ★★★★★

```
A 16:9 minimalist data-visualization card, clean editorial style.
Two vertical bars side by side for comparison.
Left bar: tall, muted gray, labelled below in Russian "Opus 4.7" with a small
icon of a bug; a Russian tag near it reads "незамеченные баги".
Right bar: about four times shorter, glowing green, labelled below "Opus 4.8".
Large Russian headline, top-left, two lines: "В 4 раза реже оставляет
собственные баги незамеченными".
Small Russian footnote at the very bottom: "цифры самой Anthropic — проверяем сами".
Color palette: dark charcoal background, single emerald-green accent, thin light
grid lines, generous whitespace.
Model names "Opus 4.7" and "Opus 4.8" stay in Latin. No logos. No faces.
```

**Когда использовать:** Habr (превью в ленте — цифра останавливает скролл) и TenChat (любит инфографику). Сильна как «главная цифра» статьи.

---

## Prompt 3: Claude сам пишет оркестрацию ★★★★☆

```
A 16:9 conceptual editorial illustration, control-room aesthetic.
An abstract faceless "conductor" robot sits at a glowing console and writes a
single luminous script that branches downward into dozens of parallel tracks,
each track a small worker-agent processing a fragment of a large code migration —
like a mission-control board lighting up with parallel work.
Overlaid Russian title, upper area: "Claude сам пишет оркестрацию".
Smaller Russian caption beneath it: "десятки-сотни субагентов в одной сессии".
In a bottom corner, a subtle token meter ticking upward with a small Russian
label "токенов уходит больше" — a quiet nod to the cost caveat.
Color palette: dark control-room blue, teal and orange accents, soft glow.
No brand logos. No human faces. No photorealism.
```

**Когда использовать:** Pikabu и Telegram — более «сценный», эмоционально-вовлекающий вариант про автономную оркестрацию. Хорош, если хочется визуально подсветить Dynamic Workflows.

---

## INLINE-1: перерисовка графика «Разгон линейки Claude Opus» ★★★★★

> ЭТО НЕ ОБЛОЖКА. Это inline-иллюстрация для вставки в тело статьи (секция «Что вообще вышло»).
> Сохранить готовый файл как **`cadence-acceleration.png`** в этой же папке — в статье уже стоит `![…](./pictures/opus-4-8-honesty-dynamic-workflows/cadence-acceleration.png)`.
> Это перерисовка авторского скриншота `.tmp/photo_2026-05-28_22-47-42.jpg` в чистой редакционной графике. Данные менять НЕЛЬЗЯ — только оформление.

```
A clean 16:9 editorial data-visualization: a single horizontal timeline showing
the accelerating release cadence of the Claude Opus model line. The horizontal
distance between points represents REAL elapsed time between releases (the whole
point of the chart — gaps get visibly shorter toward the right).

Title (top-left, bold, Russian): "Разгон линейки Claude Opus".
Subtitle under it (Russian, lighter weight): "от Opus 4 до Opus 4.8 — расстояние = реальное время".

One horizontal axis with six dots. Labels alternate above / below the axis in
small rounded "chips". Keep model names in Latin and dates in Russian exactly as listed:

  • dot 1 (label ABOVE):  "Opus 4"   / "22 мая"
  • dot 2 (label BELOW):  "Opus 4.1" / "авг 2025"
  • dot 3 (label ABOVE):  "Opus 4.5" / "24 ноя"
  • dot 4 (label BELOW):  "Opus 4.6" / "5 фев"
  • dot 5 (label ABOVE):  "Opus 4.7" / "16 апр"
  • dot 6 (label BELOW):  "Opus 4.8" / "28 мая"   ← highlight this chip with a bold accent border

Between the dots, place the gap labels (Russian) ON the axis, with the spacing
between dots PROPORTIONAL to these values so the acceleration is visible:
  "~3 мес"  →  "~3 мес"  →  "10 нед"  →  "10 нед"  →  "6 нед"
(so the last gap "6 нед" is visually the shortest, the first two the widest.)

Bottom axis ticks (Russian, light gray): "май 2025" … "ноя 2025" … "май 2026".

Style: light/off-white background, terracotta-brown dots and chip borders
(matching the source), thin gray axis, generous whitespace, modern editorial
infographic look. Crisp, legible, no clutter, no logos, no faces.
```

**Когда использовать:** только как inline-вставка в статью (Habr и адаптации). Это «сердце» аргумента про ускорение каденса — нужна именно она, в отличие от обложек, которые взаимозаменяемы.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080. Для INLINE-1 ширина важнее — таймлайн вытянутый.
- **Формат:** PNG (INLINE-1 — обязательно `cadence-acceleration.png`).
- **Стиль:** без фотореализма людей, без лиц, без логотипов реальных компаний.
- **Цветовая палитра:** обложки — тёмный фон + один акцент; INLINE-1 — светлый фон + терракота (как в оригинале).
- **Текст на изображении:** на русском, кроме имён моделей (`Opus 4`…`Opus 4.8`), дат и идентификаторов.

## Что НЕ нужно генерировать

- Логотипы Anthropic / Claude — только generic-роботы и абстракции.
- Лица — ни людей, ни «эмоциональных» роботов с грустными/злыми мордами. Мы разбираем релиз, не критикуем.
- Маркетинговые баннеры с кучей текста.
- Английскую инфографику для русской статьи.
- Любые цифры, которых нет в статье (только: 4×, 6 недель, ×2/×6, 2.5×, даты релизов, 750 000 строк / 11 дней / 99.8%).

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (обложка) + INLINE-1 в теле | 16:9 |
| Pikabu | Prompt 3 | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 | Любой, читается на мобильном |
