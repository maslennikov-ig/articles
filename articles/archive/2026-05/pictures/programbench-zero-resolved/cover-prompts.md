# Промпты для обложек: ProgramBench — все модели на 0%

Три варианта обложки для статьи `articles/habr/programbench-zero-resolved.md` про новый бенчмарк ProgramBench, на котором все девять топовых LLM показали 0% полного резолва. Промпты на английском, текст на изображении — на русском (кроме имён моделей и чисел). Поддерживаются Whisk, Midjourney, Imagen 3+, любой современный text-to-image c приличным рендером надписей.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/programbench-zero-resolved/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Wall of Zero (главный insight) ★★★★★

```
A dramatic editorial illustration, 16:9 ratio, dark navy and deep red palette with hints of cold cyan light. Foreground: a row of nine stylized robot silhouettes, each one slightly different in shape (suggesting different AI model "personalities" — bulky, compact, sleek, square, rounded — but no real-world brand logos). Each robot stands with its head tilted up. Above them and across the entire upper half of the frame: a massive concrete-grey wall, lit from below, with one giant glowing word painted in red Russian sans-serif: «РЕЗОЛВ: 0%». Below the word, slightly smaller white technical caption: «9 моделей · 200 задач · 248 000 тестов». Tiny model labels float on small floating tags above each robot — readable but secondary: "Opus 4.7", "GPT 5.4", "Gemini 3.1 Pro", "Sonnet 4.6", "Haiku 4.5", "GPT 5.4 mini", "GPT 5 mini", "Gemini 3 Flash", "Opus 4.6". Above the wall, in faint chalky letters: "ProgramBench — Meta SLab × Stanford × Harvard". Cinematic atmospheric lighting, slight fog, painterly editorial style, no photorealistic faces, no real company logos.
```

**Когда использовать:** универсальная обложка #1, лучше всего для Habr (16:9, читается в ленте) и Telegram-анонса. Сразу даёт цифру и масштаб.

---

## Prompt 2: SWE-bench vs ProgramBench (контраст бенчмарков) ★★★★★

```
A clean editorial data-visualization illustration, 16:9 ratio, modern infographic aesthetic, dark charcoal background with warm amber and cool teal accents. Two horizontal bar charts stacked vertically, each labeled in Russian. Top chart: title «SWE-bench: пофиксить баг». Three semi-transparent green bars filling about 70% of available width, labeled "Opus 4.7", "GPT 5.4", "Gemini 3.1 Pro", each with tiny percentage markers near 70%. Bottom chart: title «ProgramBench: собрать с нуля». Same three model labels, but bars are nearly invisible — just thin red glowing slivers (3%, 0%, 0%) hugging the left edge against a vast empty space stretching right. Between the two charts, in clean Russian typography centered: «Один и тот же агент. Разные тесты. Разные миры». In the upper-right corner, tiny technical caption: "9 моделей · 200 tasks · 248K tests · sandboxed Docker · zero internet". Subtle grid lines, sharp typography, no logos, editorial-grade composition.
```

**Когда использовать:** Habr и TenChat — там аудитория ценит инфографику и сравнения. Объясняет суть статьи без чтения текста: модели на старом бенчмарке хороши, на новом проваливаются.

---

## Prompt 3: Air Castle (метафора vibe-coding) ★★★★☆

```
Editorial illustration in painterly digital style, 16:9 ratio, twilight palette — deep purples, dusty pinks, weathered gold. Center frame: a confident-looking robot character (generic, not branded) standing on a small platform of solid ground, holding an architect's blueprint with one hand and pointing upward with the other. Above the robot, a magnificent floating castle of white-and-gold spires, towers, gardens — the full "system under one prompt" dream. But the castle is visibly disintegrating from the bottom: chunks of stone falling, scaffolding poking out where walls should be, gaps revealing empty interior. The falling chunks become small grey blocks labeled in tiny Russian text: «зависимости», «архитектура», «инварианты», «тесты». Underneath the entire scene, a calm Russian caption in editorial serif: «Собрать систему промптом — пока миф». Top-right small technical tag: "ProgramBench · 0% resolved". Painterly, slightly melancholy, not mocking — observational. No real company logos, no recognizable human faces.
```

**Когда использовать:** Pikabu (там любят метафоры и драматическую сценку) и второй вариант для Telegram-анонса. Эмоционально цепляет, объясняет угол подачи без графиков.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080.
- **Формат:** PNG (приоритет) или JPG.
- **Стиль:** без фотореализма людей, без узнаваемых лиц, без логотипов реальных компаний (Meta, OpenAI, Anthropic, Google).
- **Цветовая палитра:** тёмный фон + контрастные акценты (красный/амбер/тил). Не пастель — статья про провал бенчмарка, не про утренний кофе.
- **Текст на изображении:** **на русском** (заголовки, подписи), кроме имён моделей (`Opus 4.7`, `GPT 5.4`, `Gemini 3.1 Pro` и т.д.), названия бенчмарков (`ProgramBench`, `SWE-bench`) и численных показателей (`0%`, `200 tasks`, `248K tests`, `3%`).

## Что НЕ нужно генерировать

- Логотипы Meta, OpenAI, Anthropic, Google — только generic AI-character дизайны.
- Фото реальных людей (включая авторов paper — John Yang, Kilian Lieret и др.).
- Confused / sad / crying faces у роботов — обложка не должна выглядеть как насмешка над моделями. Тон — наблюдение, не глумление.
- Маркетинговые баннеры с кучей текста и эмодзи.
- Текст на английском там, где русский был бы естественнее (заголовки, подписи к диаграммам).
- Хайп-шаблоны вроде «AI failed!!!» — статья сдержанная, обложка тоже.

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (Wall of Zero) или Prompt 2 (контраст бенчмарков) | 16:9 — превью в ленте |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Pikabu | Prompt 3 (Air Castle) | Квадрат или 16:9 |
| Telegram анонс | Prompt 1 (универсал, читается на мобильном) | 16:9 |
| VC.ru / Dzen (если будет адаптация) | Prompt 1 | 16:9 |
