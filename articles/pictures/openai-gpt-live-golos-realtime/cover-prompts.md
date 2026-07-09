# Промпты для обложек: GPT-Live от OpenAI (голос, который слушает и говорит одновременно)

Обложки к статье `articles/habr/openai-gpt-live-golos-realtime.md` — разбор новинки GPT-Live: full-duplex-голос + фоновая GPT-5.5, плюсы, минусы и польза. Промты рассчитаны на Midjourney / Imagen / любой генератор, понимающий английские инструкции. Текст, который должен появиться НА картинке, задан на русском (кроме имён моделей и технических идентификаторов).

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/openai-gpt-live-golos-realtime/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Болталка спереди, «мыслитель» в фоне ★★★★★

Главный insight статьи — разделение ролей: быстрый голос держит разговор, а тяжёлое считает фоновая модель.

```
Editorial tech illustration, 16:9, clean modern flat-vector style with soft depth.
Split composition of a single stylized AI head in profile, made of two translucent layers.
FRONT layer: a bright, friendly glowing soundwave / speech bubble, fast and lively, labelled in Russian "Болталка — отвечает сразу".
BACK layer, dimmer and deeper, showing slow rotating gears / a glowing brain, labelled "GPT-5.5 — думает в фоне".
A thin animated arrow loops from the back layer forward into the conversation, labelled in Russian "приносит ответ, когда готов".
Small caption strip at the bottom in Russian: "Слушает и говорит одновременно". 
Top-left small tag in latin: "GPT-Live".
Palette: deep navy background, teal and warm amber neon accents, high contrast, no photorealism, no human faces, no company logos.
```

**Когда использовать:** Универсал для Habr (превью в ленте) и Telegram-анонса — точнее всего передаёт суть «две роли в одной модели».

---

## Prompt 2: Треугольник «скорость / ум / цена» — выбери 2 из 3 ★★★★★

Главная концепция-контраст: треугольник компромисса, который GPT-Live не победил, а разнёс на две модели.

```
Minimalist data-viz infographic, 16:9, dark editorial style.
A large clean triangle in the centre, each vertex glowing a different neon colour and labelled in Russian:
top vertex "Скорость", bottom-left "Ум", bottom-right "Цена".
A dashed selection highlights that only TWO vertices can light up at once; the third is dimmed.
To the right, two small glowing model-cards connected by an arrow, labelled in Russian:
card 1 "Быстрый голос → Скорость", card 2 "Фоновая GPT-5.5 → Ум".
A short red price-tag icon near the bottom-right labelled in Russian "Цена — открытый угол, ~10×".
Headline across the top in Russian: "Выбери 2 из 3 — или раздели на две модели".
Palette: near-black background, electric blue / magenta / amber vertices, thin precise lines, no faces, no logos, no photorealism.
```

**Когда использовать:** TenChat и Habr — инфографика с чёткой мыслью, хорошо читается как самостоятельный тезис.

---

## Prompt 3: «Угу, угу, ага» — сценка про поддакивания ★★★★☆

Эмоционально-ироничная версия: главный минус из статьи — навязчивые поддакивания и невозможность помолчать.

```
Warm humorous editorial cartoon, 16:9, friendly rounded vector style.
A person sitting with a coffee, mid-thought, one finger raised as if about to speak but pausing to think.
Next to them a small cute robot assistant eagerly leaning in, emitting a cluster of speech bubbles in Russian:
"угу", "ага", "да-да", "мхм" — slightly too many, comically over-enthusiastic.
The person's own thought bubble in Russian: "дай подумать...".
A small greyed-out button floating nearby, labelled in Russian "Помолчи, я думаю" with an off-toggle.
Top corner latin tag: "GPT-Live".
Palette: warm cream background, coral and teal accents, soft and playful, no realistic faces, no company logos, expressive but not sad.
```

**Когда использовать:** Pikabu и Telegram — цепляет эмоцией и самоиронией, отражает честный скепсис автора.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без узнаваемых лиц
- **Цветовая палитра:** тёмный фон + неоновые акценты (Prompt 1–2); тёплая мягкая палитра для сценки (Prompt 3)
- **Текст на изображении:** на русском, кроме `GPT-Live`, `GPT-5.5` и технической нотации

## Что НЕ нужно генерировать

- Логотипы OpenAI, Google, ByteDance, Nvidia — только generic-роботы / абстракция
- Фото реальных людей
- Грустные/растерянные «лица» у роботов — мы разбираем, не высмеиваем
- Маркетинговые баннеры с кучей текста
- Английский текст там, где русский естественнее

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 или 2 | 16:9 (превью в ленте) |
| Pikabu | Prompt 3 | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 (универсальный) | Любой, читается на мобильном |
