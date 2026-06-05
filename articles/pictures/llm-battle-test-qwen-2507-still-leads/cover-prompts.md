# Промпты для обложек: «Год на троне» — Qwen3-235B-2507 держит value-лидерство

Обложки к статье `articles/habr/llm-battle-test-qwen-2507-still-leads.md` (battle test 2026-06, очная ставка четырёх моделей). Промты — на английском (так Whisk/Midjourney/Imagen работают лучше), но **текст НА картинке — по-русски**, кроме id моделей и чисел. Поддерживаются Whisk, Midjourney, Imagen и любой text-to-image генератор.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/llm-battle-test-qwen-2507-still-leads/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Тихий король среди штиля и шторма ★★★★★

```
Editorial tech illustration, 16:9, dark futuristic background with subtle neon grid.
Center: a calm, slightly worn robot labeled "Qwen 2507" sitting on a glowing throne.
The throne's base is engraved with a Russian sign: "ЛУЧШИЙ ПО ЦЕНЕ/КАЧЕСТВУ".
Around the throne, several flashier, newer robots (labels "Gemini", "DeepSeek", "MiniMax")
rush past in motion blur, trying to climb but sliding off — they cannot take the seat.
Small floating banner near the throne, in Russian: "Релиз — июль 2025. Всё ещё №1".
Mood: a quiet veteran king amid a chaotic race. Electric blue + warm gold accents.
No real company logos, generic robots only. Text on image in Russian (except "Qwen 2507",
"Gemini", "DeepSeek", "MiniMax", "2025").
```

**Когда использовать:** Универсал, лучший для Habr и Telegram-анонса — передаёт главный insight статьи (одна старая модель держит трон, новинки мимо).

---

## Prompt 2: Хронология — рынок штормит, одна линия не падает ★★★★★

```
Clean data-visualization cover, 16:9, dark background.
A timeline along the X axis with Russian labels: "Июль 2025", "Апрель 2026", "Июнь 2026".
Multiple thin colored lines jump around chaotically: one labeled "Gemini" shoots up steeply
with an arrow "57 → 97"; another labeled "DeepSeek" zig-zags with a tag "×3 ретеста";
a "MiniMax" line spikes then dips. Through all of them, ONE thick, steady GOLD horizontal
line stays flat at the very top, labeled "Qwen-2507 · value №1".
Big Russian title across the top: "Год. Никто не сдвинул".
Subtle gridlines, glowing nodes. Minimal, premium analytics aesthetic.
Text in Russian except model ids and the numbers "57 → 97", "×3".
```

**Когда использовать:** Habr (превью в ленте) и TenChat — инфографика про долговечность, цифры на месте.

---

## Prompt 3: Эффект айфона — хайп против результата ★★★★☆

```
Satirical-but-respectful editorial illustration, 16:9, dark stage with spotlight.
On a high pedestal stands a glossy, adored robot labeled "MiniMax", a cheering crowd of
small silhouettes below holding up phones. Above its head a speech bubble shows Russian text
glitching with a Chinese character wedged in: "典型ный пример" (highlighted red).
A small downward score tag floats beside it: "−CJK". Off to the side, in the shadows,
the plain "Qwen 2507" robot quietly holds a price tag "value 91.6" and a small Russian
sign: "тихий чемпион".
Bottom caption in Russian: "Хайп ≠ результат на твоих задачах".
Amber warning tones + cool background. Generic robots, no real logos. No sad/mocking faces —
analytical, not cruel. Text in Russian except "MiniMax", "Qwen 2507", "典型ный пример",
"CJK", "91.6".
```

**Когда использовать:** Pikabu (любит сюжет/сатиру) и Telegram-анонс — раскрывает непопулярное мнение про MiniMax и вопрос к читателям.

---

## Prompt 4: Спидометр — новый критерий ★★★★☆

```
Dynamic racing-dashboard illustration, 16:9, dark, motion blur.
Four robot runners on a track with speed tags above each: "Gemma-26B · 57 с" sprinting ahead,
"Gemma-31B · 106 с", "DeepSeek · 132 с", and "Qwen · 170 с" trailing last.
A large dashboard gauge in the foreground with a Russian label on its face:
"СКОРОСТЬ ГЕНЕРАЦИИ — отягчающий критерий", needle pointing into a red zone.
Neon speed lines, energetic but clean. Text in Russian except model ids and "57 с / 170 с".
```

**Когда использовать:** запасной вариант для Habr/TenChat, если нужна обложка под раздел про скорость генерации.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон + неоновые акценты (электрический синий + золото); для Prompt 3 — янтарные «warning»-тона
- **Текст на изображении:** **на русском**, кроме id моделей (`Qwen 2507`, `Gemini`, `DeepSeek`, `MiniMax`, `Gemma-26B`), чисел и артефакта `典型ный пример`

## Что НЕ нужно генерировать

- Логотипы реальных компаний (Alibaba, Google, Microsoft) — только generic-роботы/абстракции
- Фото реальных людей (включая автора)
- Злые/унижающие лица у моделей — мы анализируем, а не глумимся (особенно в Prompt 3)
- Маркетинговые баннеры с простынёй текста
- Английский текст там, где русский естественнее

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 или 2 | 16:9 (превью в ленте) |
| Pikabu | Prompt 3 | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 или 3 | Любой, читается на мобильном |

## Правило: ничего не выдумывать

Все цифры, имена моделей, артефакт `典型ный пример` и value 91.6 — из самой статьи. На обложку не добавляем фактов, которых в тексте нет.
