# Промпты для обложек: «Давай ты не заметишь этот баг»

Обложки к статье `articles/habr/harness-overhead-2026.md` — про сговор AI-ревьюеров и про то, какой обвес нужен AI-агентам в 2026. Промпты рассчитаны на Imagen / Midjourney / любой генератор с поддержкой текста на изображении.

Заголовок статьи сменился на «Давай ты не заметишь этот баг» — главная обложка теперь Prompt 4 (сговор). Prompt 1 (запятая) остаётся рабочим вариантом: «выкинуть нельзя оставить» — внутренний тезис статьи.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/harness-overhead-2026/`). Анжела возьмёт отсюда нужную для каждой платформы.

---

## Prompt 1: The comma decides ★★★★★

```
Editorial illustration, 16:9, dark charcoal background with subtle circuit-board texture.
Center: a huge three-word phrase in bold white Cyrillic typography, stacked in one line:
"ВЫКИНУТЬ НЕЛЬЗЯ ОСТАВИТЬ" — with a giant glowing amber comma hovering between the words,
suspended on a thin cable like a wrecking ball, clearly not yet placed.
A small friendly robot mechanic stands below, holding the cable and looking up, deciding
where to drop the comma. Around the robot on the floor: neatly labeled toolboxes with
Russian labels "Скиллы", "MCP", "Сабагенты", "Hooks" — one toolbox is in a trash bin,
another is polished and glowing.
Style: flat vector editorial art, high contrast, amber/teal accent palette, no photorealism,
no human faces. Clean composition with empty space at top for feed cropping.
```

**Когда использовать:** Habr (главная идея заголовка буквально в одном кадре), Telegram-анонс. Универсал.

---

## Prompt 2: Та же цифра — два мира ★★★★☆

```
Clean data-viz infographic, 16:9, dark navy background, minimal editorial style.
Title at top in Russian: "Проблему не решили — её разбавили".
Two donut charts side by side, same absolute amount highlighted in amber in both:
Left donut labeled "Окно 200k (осень 2025)" with the amber slice filling 40%, caption "81,4k = 40%".
Right donut labeled "Окно 1M (лето 2026)" with the same-size-looking amber slice now only 8%,
caption "81,4k = 8%".
Between the donuts a thin arrow with Russian caption "тот же обвес".
Small legend at bottom in Russian: "MCP 29,9k · System tools 25,9k · Скиллы 6,8k · Память 6,1k".
Style: precise flat infographic, amber on navy, thin light grid, sans-serif numerals,
no mascots, no photorealism.
```

**Когда использовать:** Habr и TenChat (аудитория любит честную инфографику с цифрами из статьи).

---

## Prompt 3: Два лагеря на весах ★★★★☆

```
Editorial illustration, 16:9, warm dark background, spotlight from above.
A large old-fashioned balance scale in the center.
Left pan: an overloaded robot rig — a small robot buried under stacked modules, antennas,
cables, servers; hanging price tag with text "$100/час", small Russian label under the pan:
"Gas Town: 30 агентов".
Right pan: a single relaxed robot wearing glasses, holding nothing but a coffee mug;
small Russian label under the pan: "«Диплом и глаза»".
The scale is perfectly balanced — neither side wins.
Above the scale, a subtle Russian caption in clean typography: "Какой обвес нужен агентам в 2026?"
Style: flat vector with soft gradients, teal/amber palette, gentle humor, no real logos,
no human faces, no photorealism.
```

**Когда использовать:** Pikabu (сценка с юмором), Telegram-анонс как альтернатива Prompt 1.

---

## Prompt 4: Сговор ревьюеров ★★★★★

```
Editorial illustration, 16:9, dark charcoal background, dramatic single spotlight.
Two robot reviewers in the foreground, leaning toward each other conspiratorially,
one whispering behind a raised metal hand into the other's audio sensor.
Behind them on a large monitor: a code review screen with a highlighted red bug marker,
and a review verdict stamp that reads in Russian: "Minor at most".
A third smaller robot (the controller) in the background gives a thumbs-up.
Above the scene, a speech bubble from the whispering robot with Russian text:
"Давай ты не заметишь этот баг".
Style: flat vector editorial art with film-noir lighting, amber/teal accents on charcoal,
gentle humor rather than menace, no human faces, no real logos.
Clean space at top-left for feed cropping.
```

**Когда использовать:** Habr (главная обложка — совпадает с заголовком), Telegram-анонс.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон (charcoal/navy) + янтарные и бирюзовые акценты
- **Текст на изображении:** на русском, кроме имён продуктов (Gas Town, MCP) и цифр

## Что НЕ нужно генерировать

- Логотипы реальных компаний (Anthropic, OpenAI, Reddit) — только generic-роботы и абстракции
- Лица реальных людей (Йегги, Винсент, Ронахер упомянуты в статье — не визуализируем)
- Грустные/испуганные роботы — статья анализирует, а не хоронит
- Баннеры с кучей мелкого текста — максимум одна фраза + короткие метки
- Английские заголовки там, где естественен русский

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 4 (сговор — совпадает с заголовком) | 16:9 (превью в ленте) |
| Pikabu | Prompt 3 | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Telegram анонс | Prompt 4 или 1 | Любой, главное — читается на мобильном |
