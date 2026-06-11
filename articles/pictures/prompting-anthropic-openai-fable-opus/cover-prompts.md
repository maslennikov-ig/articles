# Промпты для обложек: гайды Anthropic vs OpenAI, Fable 5 vs Opus 4.8

Обложки для статьи `articles/habr/prompting-anthropic-openai-fable-opus.md` (Хабр) и её будущих адаптаций. Промпты совместимы с Midjourney / Imagen / любым другим генератором.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/prompting-anthropic-openai-fable-opus/`). Анжела возьмёт отсюда нужную для каждой платформы.

---

## Prompt 1: Одна компания — противоположные инструкции ★★★★★

```
Editorial illustration, 16:9, dark navy background with subtle grid. Two
identical friendly generic robots stand side by side facing the viewer. One
person in the middle (seen from behind, no recognizable face) hands each
robot a different instruction card. The left card reads "Спавнь больше
субагентов" with a small label "Opus 4.8" under the left robot. The right
card reads "Притормози с субагентами" with a small label "Fable 5" under
the right robot. Above the scene, one large manual/book hovers with the
title "Один вендор — два гайда". Flat modern vector style, high contrast,
warm orange and cyan accents on dark background, no photorealism, no real
company logos.
```

**Когда использовать:** Универсал — главный инсайт статьи в одном кадре. Лучший вариант для Habr (превью в ленте) и Telegram-анонса.

---

## Prompt 2: Инфографика противоположных советов ★★★★☆

```
Clean data-viz style cover, 16:9, dark charcoal background. A two-column
comparison table rendered as a stylized infographic with glowing borders.
Header row: left cell "Opus 4.8" (amber accent), right cell "Fable 5"
(cyan accent). Three visible rows with short Russian labels: row 1 —
"Субагенты: поощрять" vs "Субагенты: сдерживать"; row 2 — "Effort: xhigh"
vs "Effort: high"; row 3 — "Старые промпты: работают" vs "Старые промпты:
мешают". Above the table a bold Russian title: "Противоположные советы —
одна компания". Minimalist iconography next to each row (robot icon, gauge
icon, document icon). Flat design, no gradients overload, no logos, crisp
readable typography.
```

**Когда использовать:** Habr и TenChat — аудитория любит конкретику в превью. Хорош как первая иллюстрация внутри статьи рядом с таблицей.

---

## Prompt 3: Три коллекции промптов (зоопарк конфигов) ★★★★☆

```
Warm editorial illustration, 16:9, desk scene viewed slightly from above.
Three thick ring binders standing on a developer's desk, each with a
labeled spine: "Opus 4.8", "Fable 5", "GPT-5.x". A fourth thin folder lies
flat, labeled "Универсальные". Sticky notes poke out of the binders; one
visible note reads "не показывать счётчик токенов", another reads "убрать
CAPS". In the background, a monitor glows with an abstract prompt editor
(unreadable blurred text). Cozy but slightly chaotic mood, muted palette
with orange/cyan accents, flat vector style, no faces, no logos.
```

**Когда использовать:** Pikabu и Telegram — эмоционально-бытовая метафора «зоопарк конфигов», читается без контекста. Подойдёт и для будущей Dzen-адаптации.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон + оранжевый (Opus/Anthropic-тепло) и циан (Fable/техника) как контрастная пара
- **Текст на изображении:** **на русском**, кроме имён моделей (`Opus 4.8`, `Fable 5`, `GPT-5.x`) и технических идентификаторов (`effort`, `xhigh`)

## Что НЕ нужно генерировать

- Логотипы Anthropic / OpenAI — только generic роботы и абстракции
- Реальные интерфейсы продуктов (Claude Code, ChatGPT)
- Грустные/злые лица у роботов — мы разбираем поведение, а не ругаем модели
- Фиолетовые градиенты на белом фоне (ирония статьи обязывает)
- Английский текст там, где естественен русский

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 | 16:9 (превью в ленте) |
| Pikabu | Prompt 3 | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 | Любой, главное — читается на мобильном |
