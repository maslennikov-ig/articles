# Промпты для обложек: настройки OpenRouter и цена вызова

Обложки к статье `articles/habr/llm-settings-price-spread.md` — «$4078 или $9.30 в месяц за одну
и ту же модель». Промты рассчитаны на Midjourney / Imagen / любой генератор с поддержкой текста
на изображении. Текст, который должен появиться на картинке, указан по-русски — кроме имён моделей,
идентификаторов и чисел.

Готовые PNG складываем в эту же папку. Здесь уже лежит `arena-pareto-2026-08-04.png` — это
**не обложка**, а иллюстрация внутрь статьи (скриншот вида «Парето» на LM Arena, вставляется
в раздел «Настройки — половина дела»).

---

## Prompt 1: Two invoices, one model ★★★★★

```
Editorial illustration, 16:9, dark charcoal background with subtle grid, cool teal and amber accents.
Two paper invoices float side by side, sharply lit, slightly tilted, casting soft shadows.
Both invoices carry the identical header line "GPT-5.6 Luna · 6000 вызовов" at the top.
The left invoice is dense with line items and its total reads "$4 078.80" in large amber digits,
with a small red label beneath: "настройки по умолчанию".
The right invoice is short and clean, its total reads "$9.30" in large teal digits,
with a small green label beneath: "настройки выбраны руками".
Between them a thin vertical divider with the caption "одна модель, одни и те же ответы".
No logos, no faces, no photorealistic people. Flat vector-editorial style with fine linework,
crisp readable typography, generous negative space.
```

**Когда использовать:** универсал. Главный инсайт статьи в одном кадре — берём на Хабр и в анонс
Telegram. На мобильном читается за счёт двух крупных сумм.

---

## Prompt 2: The multiplier stack ★★★★★

```
Data-visualization poster, 16:9, dark navy background, precise technical aesthetic, thin grid lines.
A horizontal cascade chart in four descending steps, each step a glowing bar dropping to the next,
teal-to-amber gradient from expensive to cheap.
Step labels in Russian, set beside each drop:
"провайдер ×11", "длина контекста ×5.5", "класс обслуживания ×2", "кэш промпта ×3.6".
The leftmost bar is annotated "$0.67980 за вызов", the rightmost "$0.00155 за вызов".
Title across the top in Russian: "Четыре множителя, ни один не меняет модель".
Small monospace footnote in the bottom right corner: "снимок тарифов 04.08.2026".
Clean infographic style, no characters, no logos, no photorealism, high contrast for small screens.
```

**Когда использовать:** TenChat и VC.ru — там любят инфографику с разложением. На Хабре хорошо
идёт как вторая картинка внутри статьи, к разделу «Всё вместе на одной задаче».

---

## Prompt 3: Three queues ★★★★☆

```
Isometric editorial illustration, 16:9, deep indigo background, warm rim lighting.
Three parallel queues of identical abstract data packets (simple glowing cubes, no faces, no robots)
move toward the same single glowing server gate at the right edge.
The top lane is short and fast, tagged "priority · ×4 цены".
The middle lane is medium, tagged "стандарт · ×2".
The bottom lane is long and patient, tagged "flex · базовая цена", with a small clock icon above it.
All three lanes end at the same gate, and one caption sits under the gate: "модель одна и та же".
Headline in the upper left, Russian: "Вы платите за очередь, а не за качество".
Muted palette, geometric shapes, no brand marks, no human figures, no text in English
except the tags flex / priority.
```

**Когда использовать:** Pikabu и Telegram — метафора считывается без чтения статьи. Подходит,
если нужен более «сценический» кадр вместо графика.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц, без узнаваемых логотипов
- **Палитра:** тёмный фон (charcoal / navy / indigo) плюс два акцента — бирюзовый на «дёшево»
  и янтарный на «дорого». Один и тот же код цвета во всех трёх промтах, чтобы серия читалась
  как серия
- **Текст на изображении:** по-русски, кроме `flex`, `priority`, `GPT-5.6 Luna`, дат и сумм

## Что НЕ генерировать

- Логотипы OpenRouter, OpenAI, Azure и других упомянутых компаний
- Роботов с грустными или довольными лицами — статья ничего не критикует, она объясняет
- Мешки денег, монеты, доллары россыпью: тема про инженерию, а не про финансовый успех
- Английские подписи там, где естественнее русские
- Цифры, которых нет в статье

## Адаптация под площадки

| Площадка | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 | 16:9, превью в ленте |
| Telegram-анонс | Prompt 1 | 16:9, суммы должны читаться на мобильном |
| TenChat | Prompt 2 | 4:3 или 16:9 |
| VC.ru | Prompt 2 | 16:9 |
| Pikabu | Prompt 3 | квадрат или 16:9 |
