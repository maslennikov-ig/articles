# Промпты для обложек: «Claude Mythos нашёл 271 баг в Firefox 150»

Три варианта обложек к статье `articles/habr/firefox-claude-mythos-271-bug-review.md` — обзор-новость о хардернинге Firefox с preview-моделью Anthropic. Поддерживаемые генераторы: Whisk, Midjourney, Imagen, Stable Diffusion XL.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/firefox-claude-mythos-271-bug-review/`). Анжела возьмёт нужный вариант под каждую платформу.

---

## Prompt 1: Главная цифра в стиле security advisory ★★★★★

```
A dark-themed editorial cover in the style of a CVE security advisory bulletin.
Centered: a giant glowing red number "271" in monospace stencil typeface,
with thin neon-cyan "uncovered" stamp ticking across it. Below the number,
in clean Russian sans-serif: "Уязвимостей в Firefox 150 нашёл AI-агент за месяц".
On either side of the number, two smaller cards stacked vertically:
left card "15 лет" with text "<legend>" inside angle brackets,
right card "20 лет" with text "XSLT" in techy monospace.
Background: deep navy gradient with faint subtle hex/circuit pattern,
red horizontal scanlines suggesting an old terminal, bottom-right small
Firefox-orange flame silhouette (no logo). Top-left tiny tag in cyan:
"Mozilla × Claude Mythos Preview". Style: editorial illustration,
high-contrast, slight CRT glow, no people, no realistic faces.
Format: 16:9, 1920×1080.
```

**Когда использовать:** Главный вариант для Habr-превью в ленте и для TenChat. Цифра останавливает скроллинг, две даты создают контраст «современное событие × древние баги». Узнаваемо как security-новость с первого взгляда.

---

## Prompt 2: Метафора «Архивариус и древние баги» ★★★★☆

```
Editorial illustration: a faceless robotic figure with a clipboard standing
in a dim archive corridor of towering metal cabinets stretching into a
vanishing point. Cabinet drawers labeled in mixed Russian and English:
"<legend>", "XSLT", "WebAssembly GC", "RLBox", "IPC race". Three drawers
are pulled open and glow soft amber from inside; from one drawer a thin
beam of amber light hits a piece of paper the robot is holding, on which
in Russian large print: "Найдено: 271 уязвимость". On the wall above
the corridor in handwritten chalk style: "Архив исправлений Firefox,
2005–2026". Style: cinematic, soft chiaroscuro lighting, muted palette
(navy archive, amber accents), Pixar-meets-blueprint feel. No people,
no facial features. Format: 16:9, 1920×1080.
```

**Когда использовать:** Pikabu, Telegram-анонс, Telegraph. Эмоциональная метафора «архив древнего кода, в который наконец-то заглянул кто-то с фонариком». Лучше резонирует с широкой аудиторией, чем чистая инфографика. Идентификаторы (`<legend>`, `XSLT`, `WebAssembly GC`, `RLBox`, `IPC`) — на латинице по правилам, всё человекочитаемое — на русском.

---

## Prompt 3: Инфографика классификации severity ★★★★☆

```
Clean infographic in dataviz editorial style. Centered title in Russian:
"Что нашёл Claude Mythos в Firefox 150". Below the title — a horizontal
stacked bar chart split into three coloured segments labeled inside each
segment in white text: leftmost dark-red segment "180 — sec-high",
middle orange segment "80 — sec-moderate", rightmost yellow segment
"11 — sec-low". Above the bar, total label in Russian: "271 уязвимость
за апрель 2026". To the right of the bar, a small vertical column titled
"Среди них:" with three bullet rows in Russian: "• Sandbox escapes",
"• Use-after-free в WebAssembly GC", "• Race conditions через IPC".
Below: "Источник: Mozilla Hacks blog, 8 мая 2026". Background:
off-white with subtle grid, accent color Firefox-orange in title underline.
Typography: clean Russian sans-serif (Inter / IBM Plex Sans Russian).
Style: editorial dataviz, FT/Bloomberg feel, no people, no logos,
no decorative robots. Format: 16:9, 1920×1080.
```

**Когда использовать:** Habr (как inline-вставка в теле статьи или альтернативная обложка), VC.ru, Dzen. Идеально для аудитории, которая хочет фактуру с первого экрана. Чистая инфографика без эмоций, цифры читаются на превью даже в небольшом размере.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без узнаваемых лиц авторов отчёта (Brian Grinstead, Christian Holler, Frederik Braun) — это не их визитка, а наш разбор
- **Цветовая палитра:** тёмные навы + amber/Firefox-orange акценты + красный для security-сигналов
- **Текст на изображении:** **на русском**, кроме идентификаторов (`<legend>`, `XSLT`, `WebAssembly GC`, `RLBox`, `IPC`, `Firefox 150`, `Claude Mythos Preview`, `sec-high/moderate/low`) и чисел (`271`, `180`, `80`, `11`, `15 лет`, `20 лет`)

## Что НЕ нужно генерировать

- Логотип Mozilla или Firefox в явном виде — только generic «оранжевое пламя» как намёк
- Логотип Anthropic / Claude — только текст "Claude Mythos Preview" в типографике
- Фото или узнаваемые лица авторов отчёта Mozilla
- Confused / sad / угрожающие выражения у роботов — мы делаем разбор, не саркастический комментарий
- Маркетинговые баннеры с десятком надписей мелким шрифтом
- Текст на английском там, где русский был бы естественнее (заголовки, подписи к графикам, призывы)
- Изображения работающего эксплоита, кода с уязвимостью, скриншотов терминала с реальными командами — статья про найденные баги, не туториал по их эксплуатации

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (превью в ленте) или Prompt 3 (внутри статьи) | 16:9 |
| Pikabu | Prompt 2 | Квадрат или 16:9 |
| TenChat | Prompt 1 или Prompt 3 | 4:3 или 16:9 |
| VC.ru | Prompt 3 (бизнес-аудитория любит цифры) | 16:9 |
| Dzen | Prompt 1 | 16:9 |
| Telegram-анонс | Prompt 2 (читается на мобильном) | Любой |
