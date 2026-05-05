# Промпты для обложек: Codex vs Claude compaction

Три варианта на английском под Whisk / Midjourney / Imagen. Рейтинг ★ — мой прогноз попадания в смысл статьи. После генерации — складываем готовые PNG в эту же папку (`articles/pictures/codex-vs-claude-compaction/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Two Twin Prompts in a Tug-of-War ★★★★★

```
A symmetrical split-screen composition: on the left side, a transparent glass
container labeled "<summary>" with neat handwritten text floating inside, glowing
in soft Anthropic-blue tones. On the right side, an opaque metallic vault labeled
"AES blob" with the same handwritten text barely visible through a small crack,
glowing in OpenAI-green tones. Between them, a stretched ribbon of code text
reads "almost identical compaction prompts". Above the scene, two robot heads
peer down — one cool architectural robot looking at the glass, one sleek
silver robot looking at the vault. Dark technical background with floating
binary fragments. Editorial illustration style, clean vector lines, mood of
quiet revelation. 16:9 aspect ratio.
```

**Когда использовать:** Универсал для Habr / Pikabu / TenChat. Главный смысл статьи передаётся одним кадром: промпты-близнецы, разная упаковка (прозрачно vs зашифровано).

---

## Prompt 2: Context Window Degradation Curve ★★★★★

```
A bold horizontal infographic-style chart titled "Деградация на длинном контексте —
у обеих моделей". X-axis labeled "Длина контекста (токены)" with markers at 0,
256K, 500K, 1M. Y-axis labeled "MRCR v2 точность, %" with scale 0 to 100.
Two declining curves both sloping downward — emphasizing both models degrade,
not just one. A teal "Opus 4.6" curve starting at 91.9% at 256K, declining to
78.3% at 1M (gentle slope). An orange "Opus 4.7" curve starting at 59.2% at
256K, dropping to 32.2% at 1M (steeper slope, roughly 2x faster). Both curves
clearly going down. Small caption underneath: "обе кривые идут вниз — разница
в наклоне". Bottom corner credit: "источник: system card Opus 4.7, §8.7.2".
Dark cyberpunk data-viz aesthetic, neon glows, monospace labels. 16:9 aspect
ratio.
```

**Когда использовать:** Лучший для Habr и TenChat — техническая и бизнес-аудитория любит наглядную аналитику. Хорошо работает превью в ленте Хабра.

⚠️ ВАЖНО: обе кривые **должны идти вниз**. Если генератор нарисует «4.6 stays flat» — это фактическая ошибка (на самом деле 4.6 тоже теряет 13.6 п.п. на отрезке 256k → 1M). Деградация на длинном контексте — общее свойство всех LLM, не уникальная проблема 4.7. Просто 4.7 теряет качество в два раза быстрее.

---

## Prompt 3: Native vs Bolted-On Compaction ★★★★☆

```
Two contrasting robot diagrams placed side by side. Left robot labeled
"Codex-Max" — its compaction module is built into the chest, visibly woven
into the neural architecture wires, glowing as one organic system. Right robot
labeled "Opus 4.7" — its compaction module is a small external box bolted onto
the back with cables, clearly an afterthought, taped on with "beta" stickers.
Both robots stand on a single line labeled "context length". Below them, a
caption "natively trained vs server-side hook". Editorial technical illustration
style, isometric view, schematic crosswire aesthetic. 16:9 aspect ratio.
```

**Когда использовать:** Если хочется акцент на главную мысль статьи — «компакция в весах модели против компакции в обвязке». Драматичнее остальных, лучше зайдёт на Pikabu.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный технический фон + контрастные цвета (Anthropic-blue, OpenAI-green/orange)
- **Текст на изображении:** допустимо короткий (имена моделей, цифры) — но не предложениями

## Что НЕ нужно генерировать

- Логотипы реальных компаний (Anthropic, OpenAI) — только generic AI characters / abstract designs
- Фото реальных людей (Kangwook Lee, Boris Cherny — не визуализируем)
- «Battle» / «vs» баннеры с агрессивной риторикой — статья нейтральная, не противопоставляет
- Confused / sad faces у моделей — анализ, не критика

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 2 (инфографика) или Prompt 1 (близнецы) | 16:9 (превью в ленте) |
| Pikabu | Prompt 3 (native vs bolted-on) или Prompt 1 | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика, для бизнес-аудитории) | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 (универсальный, читается на мобильном) | Любой |
