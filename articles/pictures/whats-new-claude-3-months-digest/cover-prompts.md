# Промпты для обложек: «Если пропустили Claude последние 3 месяца»

Три варианта обложки к статье на Хабр [whats-new-claude-3-months-digest.md](../../habr/whats-new-claude-3-months-digest.md). Поддерживаются Whisk, Midjourney, Imagen и аналогичные генераторы. Текст на изображении — на русском, кроме имён продуктов (`Claude`, `Subagents`, `Skills`, `Cowork`, `Opus 4.7`, `MCP`, `Bitcoin`, `BTC`) и технических идентификаторов.

После генерации — складываем PNG в эту же папку (`articles/pictures/whats-new-claude-3-months-digest/`). Анжела возьмёт нужную для каждой платформы.

---

## Prompt 1: Parallel agents orchestra (топ-1 фича — Subagents) ★★★★★

```
A wide editorial illustration, 16:9 aspect ratio, dark navy and indigo background with soft neon accents in violet and warm orange.

In the center: a single glowing terminal window labeled "Claude Code" emitting five thin light beams that fan outward, each beam reaching a small geometric robot-icon — a clean, abstract, non-anthropomorphic shape (cube, triangle, hexagon, sphere, cylinder). Each robot has a small label beneath it on its own translucent badge, in Russian: "Поиск кода", "Аудит безопасности", "Анализ зависимостей", "Тесты", "Документация". Above the central terminal, a clean serif heading in Russian: "Параллельные subagents — топ-1 за квартал".

In the lower-right corner, a small inline subtitle in lighter type: "Если пропустили Claude последние 3 месяца".

Style: clean editorial vector + subtle grain, like a tech publication illustration. No photorealistic humans. No company logos. No emoji. Negative space respected — the image should breathe.
```

**Когда использовать:** Habr (главная обложка), Pikabu. Передаёт суть статьи через её топ-1 — параллельные subagents. Концентрированный визуал без перегруза.

---

## Prompt 2: Five-card digest inventory (инфографика «топ-5») ★★★★★

```
A wide horizontal infographic, 16:9 aspect ratio, soft dark slate background with subtle dot grid.

Five evenly-spaced rectangular cards in a single row across the canvas. Each card has a thin glowing border in a different accent color (cyan, violet, amber, soft pink, mint green from left to right) and a numbered badge in the upper-left corner ("1", "2", "3", "4", "5").

Card contents from left to right:
1. A speedometer/gauge icon. Title on card: "Opus 4.7 + /effort". Subtitle in Russian: "Рабочая модель квартала".
2. A desktop monitor icon with a folder being organized. Title: "Claude Cowork". Subtitle in Russian: "Десктоп-агент, GA".
3. A red warning triangle icon with a downward arrow. Title: "v2.1.88". Subtitle in Russian: "Мартовский bug — анти-новинка".
4. A network-graph icon with three small connected nodes. Title: "Agent Teams". Subtitle in Russian: "Experimental, ×3-7 токенов".
5. A modular blocks icon with a small magnifying glass overlay. Title: "Plugin Marketplace". Subtitle in Russian: "Skills с auto-update".

Above the row of cards, a large clean heading in Russian: "Что вы пропустили в Claude за 3 месяца".

Below the row, in smaller type, a single line in Russian: "Топ-5 фич с юзкейсами — из практики, а не из release notes".

Style: clean modern editorial infographic, no photorealism, no logos. Vector-style icons with subtle glow. Generous spacing.
```

**Когда использовать:** TenChat (4:3 кроп тоже хорошо ляжет), Habr (альтернативный вариант для тех, кто кликает по «структурным» обложкам), Telegram-анонс. Это «всё в одной картинке» — даёт читателю карту статьи ещё до клика.

---

## Prompt 3: Bitcoin wallet recovery scene (эмоциональный крючок $400K) ★★★★☆

```
A wide cinematic illustration, 16:9 aspect ratio, dim warm lighting like an old apartment at night, slight film grain.

In the foreground: a cluttered wooden desk covered with old objects — two open laptops (one slightly older-looking), a stack of external hard drives with tangled cables, scattered handwritten notes, an open notebook with cryptic strings of characters, a half-empty coffee mug. On one of the laptops, a clean dark terminal window glows brightly with text — visible on the screen is a single line in Russian: "Найден backup от декабря 2019" followed by a small green checkmark icon.

Above the desk, faintly visible in the background as if projected on the wall: a stylized abstract Bitcoin logo glowing softly, and a large number "$400,000" rendered in elegant bold serif. To the side of the desk, a small open lock icon — the moment the wallet got unlocked.

In the upper-left corner, a clean editorial caption strip in Russian: "Как Claude нашёл пароль через 11 лет хаоса в файлах".

Style: editorial cinematic, warm color palette, no human figures visible (just the implied user's workspace), no photorealistic faces. Realistic objects but slightly stylized lighting. No company logos.
```

**Когда использовать:** Pikabu (story-driven обложка, эмоциональная), Telegram-анонс с упором на «как $400K вернулись через AI». Можно использовать как cover ВТОРОЙ ленты на Habr, если первая не зайдёт. Подходит для соцсетей.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без распознаваемых лиц
- **Цветовая палитра:** тёмный фон + цветные акценты (для Prompt 1 — violet/orange; для Prompt 2 — несколько разных accent-цветов на карточках; для Prompt 3 — тёплая ночная палитра)
- **Текст на изображении:** на русском, кроме имён моделей/продуктов (`Claude`, `Opus 4.7`, `/effort`, `/fast`, `Cowork`, `Agent Teams`, `Plugin Marketplace`, `Bitcoin`, `v2.1.88`) и технических идентификаторов

## Что НЕ нужно генерировать

- Логотипы реальных компаний (Anthropic, OpenAI, Google и т.д.) — только generic-иконки
- Фото реальных людей, в том числе Дарио Амодея и пользователя cprkrn — никаких узнаваемых лиц
- Подмигивающие/говорящие/«живые» модели или роботы с эмоциями — мы анализируем, не персонифицируем
- Маркетинговые баннеры с обилием текста и стрелок
- Английский текст там, где русский был бы естественнее (заголовки, подписи на карточках)

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (главный) или Prompt 2 (если хочется инфографики) | 16:9 (превью в ленте) |
| Pikabu | Prompt 3 (эмоциональный, history-driven) | 16:9 или квадрат |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Telegram анонс | Prompt 3 (cinematic, читается на мобильном) | Любой, ориентир — мобильное превью |
| VC.ru (если будет) | Prompt 2 (бизнес-аудитории нравится структура) | 16:9 |
