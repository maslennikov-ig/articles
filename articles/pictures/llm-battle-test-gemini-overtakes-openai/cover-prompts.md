# Промпты для обложек: Battle test 5 LLM (май 2026) — китайцы выигрывают по цене и качеству

Обложки к статье `articles/habr/llm-battle-test-gemini-overtakes-openai.md` — третий battle test в цикле. Главные идеи: Gemini догнал OpenAI по качеству (97/S), но по соотношению цена/качество верхушку заняли китайские модели (DeepSeek, Tencent, Qwen). Генераторы: Whisk / Midjourney / Imagen / любой text-to-image.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/llm-battle-test-gemini-overtakes-openai/`). Анжела возьмёт оттуда нужную для каждой платформы.

**Важно про текст на картинке:** имена моделей, цифры, тарифы — латиницей/как есть (`Gemini-3.5-flash`, `97/S`, `$0.09`). Человекочитаемые заголовки и подписи — на русском.

---

## Prompt 1: Карта рынка — США держат качество, Китай держит цену/качество ★★★★★

```
A wide editorial infographic split into two competing territories on a dark tech map.
Left side glowing blue, labeled in Russian "КАЧЕСТВО" — three premium robot emblems
stacked at the top: "GPT-5.5  97/S", "Gemini-3.5-flash  97/S", "Claude Opus  96/S",
with US-style clean minimalist design and small price tags "$0.23", "$0.09", "$0.21".
Right side glowing gold/red, labeled in Russian "ЦЕНА / КАЧЕСТВО" — three compact
efficient robot emblems: "DeepSeek V4 Pro  $0.0047", "Tencent Hy3  $0.0017",
"Qwen 3.7", positioned as the winners of the value territory.
Center divider line with Russian caption: "Май 2026: впервые верхушка по цене и качеству — китайская".
Style: editorial data-map, dark background, neon accents, no real company logos,
generic robot/emblem characters only. Aspect ratio 16:9.
```

**Когда использовать:** Универсал — Habr (главное превью в ленте), TenChat. Передаёт главный тезис статьи буквально в одном кадре: США = качество, Китай = цена/качество.

---

## Prompt 2: Два флагмана на одной вершине, ценники разные ★★★★★

```
A podium scene. Two robot champions standing side by side on the SAME top step,
both wearing identical gold medals labeled "97 / S". Left robot clean and minimalist
(Gemini style) with a small green price tag floating above: "$0.09". Right robot more
imposing, premium-looking (GPT-5.5 style) with a price tag: "$0.23 — в 2.5× дороже".
Between them a scoreboard in Russian: "ПАРИТЕТ ПО КАЧЕСТВУ". Below the podium, smaller,
a compact gold robot holding a tiny tag "$0.0017" (Tencent) with a Russian caption
"а по цене/качеству — вот этот". Dark futuristic background, neon data streams.
No real logos, generic characters. Aspect ratio 16:9.
```

**Когда использовать:** Habr и Pikabu — драматичная сценка про паритет качества при разнице в цене. Хорошо читается на мобильном.

---

## Prompt 3: Лидерборд цена/качество — реальная инфографика ★★★★☆

```
A horizontal bar chart titled in Russian "Индекс цена/качество — кто реально эффективен"
on a dark dashboard background. Bars sorted descending:
"Tencent Hy3 — 88.5" (longest, glowing gold),
"DeepSeek V4 Pro — 86.6" (gold, almost as long),
"Gemini-3.5-flash — 75.8" (medium, blue),
"GPT-5.5 — 70.0" (short, silver),
"Qwen 3.7 Max — 65.7" (shortest, gray).
Each bar shows model name on the left and a small price label on the right
("$0.0017", "$0.0047", "$0.09", "$0.23", "$0.07"). Bottom caption in Russian:
"Battle test, 23 мая 2026 — реальные токены OpenRouter". Top three bars
(all Chinese models) subtly highlighted. Modern infographic, dark theme,
electric blue and gold. Aspect ratio 16:9.
```

**Когда использовать:** TenChat и Habr — деловая аудитория любит чистую инфографику с цифрами. Подчёркивает, что топ-3 по цене/качеству — китайские.

---

## Prompt 4: Заменяемая модель — слот в продукте ★★★★☆

```
A symbolic scene of a software product represented as a sleek dark device or console
with a single glowing "model slot" in the center, labeled in Russian "МОДЕЛЬ".
Several interchangeable model cartridges hover nearby, ready to be swapped:
"GPT-5.5", "Gemini-3.5-flash", "DeepSeek V4 Flash", "Tencent Hy3" — each a distinct
colored chip. One cartridge ("DeepSeek V4 Flash") is currently inserted and glowing.
A cable labeled "OpenRouter" connects the slot to all cartridges. Russian caption at
the bottom: "Продукт, который умеет менять модель без переписывания кода".
Clean tech-illustration style, dark background, neon accents, no real logos.
Aspect ratio 16:9.
```

**Когда использовать:** Habr — иллюстрирует архитектурный раздел (заменяемая модель через OpenRouter ID). Сильный крючок для технической аудитории, которая ценит инженерные паттерны.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон + неоновые акценты (синий = США/качество, золото/красный = Китай/цена-качество)
- **Текст на изображении:** на русском, кроме имён моделей и технических идентификаторов

## Что НЕ нужно генерировать

- Логотипы реальных компаний (Google, OpenAI, DeepSeek, Tencent, Alibaba) — только generic robot/emblem characters
- Флаги США и Китая в политическом контексте — статья про технику, не про геополитику (территории-зоны на карте — ок, флаги — нет)
- Confused / sad faces у моделей — мы анализируем, не критикуем
- Маркетинговые баннеры с кучей текста
- Текст на английском там, где русский был бы естественнее

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (карта рынка) или Prompt 2 (подиум) | 16:9 (превью в ленте) |
| Pikabu | Prompt 2 (подиум, драматично) | Квадрат или 16:9 |
| TenChat | Prompt 3 (инфографика индекса) | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 (карта — универсальна) | Любой, читается на мобильном |
