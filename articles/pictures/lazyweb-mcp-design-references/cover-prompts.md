# Промпты для обложек: LazyWeb — референсы вместо говнодизайна

Обложки к статье `articles/habr/lazyweb-mcp-design-references.md` (замерка бесплатного MCP-сервера дизайн-референсов LazyWeb). Промты — на английском (так Whisk/Midjourney/Imagen работают лучше), но **текст НА картинке — по-русски**, кроме имён продуктов (`LazyWeb`, `MCP`) и чисел. Поддерживаются Whisk, Midjourney, Imagen и любой text-to-image генератор.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/lazyweb-mcp-design-references/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Из головы vs по референсам ★★★★★

```
Editorial tech illustration, 16:9, split-screen composition, dark modern background
with subtle neon grid.
LEFT HALF (cold, messy): a generic robot painting an ugly, lopsided app screen from
imagination — crooked boxes, clashing colors, a small Russian label below: "Рисует
с нуля — усреднённо". A tiny tag floats: "vibes".
RIGHT HALF (clean, confident): the same robot surrounded by a neat wall of real app
screenshots (generic UI thumbnails), assembling one crisp, modern interface from them.
Russian label below: "Берёт референсы — точно". A small glowing badge reads "LazyWeb".
A vertical divider down the middle. Top banner in Russian: "Evidence, not vibes".
Electric blue + warm gold accents. Generic robots only, no real company logos.
Text on image in Russian except "LazyWeb", "vibes", "Evidence, not vibes".
```

**Когда использовать:** Универсал, лучший для Habr и Telegram-анонса — передаёт главный тезис статьи (с нуля = усреднённо, по референсам = точно).

---

## Prompt 2: 257 тысяч реальных экранов ★★★★★

```
Clean data-visualization cover, 16:9, dark background, premium analytics aesthetic.
A massive grid/wall of small real-looking app screenshots (generic UI thumbnails)
on the left, flowing through a glowing funnel labeled in Russian "семантический поиск"
into a single robot agent on the right that holds one polished screen.
Big Russian title across the top: "257 000 реальных экранов вместо фантазии модели".
Small caption near the funnel in Russian: "бесплатно, без логина".
A subtle "LazyWeb · MCP" badge in a corner. Glowing nodes, thin connecting lines.
Electric blue + gold. Text in Russian except "LazyWeb", "MCP" and the number "257 000".
```

**Когда использовать:** Habr (превью в ленте) и TenChat — инфографика про масштаб и бесплатность, цифра как стоппер.

---

## Prompt 3: Сделай 3-5 вариантов — выбери лучший ★★★★☆

```
Editorial illustration, 16:9, dark studio background with a soft spotlight.
A friendly robot agent presents a fan of five UI mockup cards floating in the air,
each card a slightly different app screen layout. Four cards are dim; ONE card glows
gold, with a checkmark and a Russian tag "лучший". A human hand reaches toward the
glowing card to pick it.
Big Russian caption at the bottom: "Сделай 3-5 вариантов — выбери лучший".
Small badge: "на базе LazyWeb". One card in the corner is crossed out with a red tag
"устаревший" (honest nod: not every reference is good).
Warm gold + cool blue. Generic robot, no faces of real people, no real logos.
Text in Russian except "LazyWeb".
```

**Когда использовать:** Pikabu (любит сюжет) и Telegram-анонс — раскрывает главный рабочий приём и честную ноту про мусорные референсы.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон + неоновые акценты (электрический синий + золото)
- **Текст на изображении:** **на русском**, кроме `LazyWeb`, `MCP`, `vibes`, `Evidence, not vibes` и чисел

## Что НЕ нужно генерировать

- Логотипы реальных компаний и реальные скриншоты конкретных приложений — только generic-роботы и абстрактные UI-плитки
- Фото реальных людей (включая автора и создателя LazyWeb)
- Злые/унижающие лица у роботов — мы анализируем инструмент, а не глумимся
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

Все цифры (257 000 экранов), имена (`LazyWeb`, `MCP`), тезис `Evidence, not vibes` и приём «3-5 вариантов» — из самой статьи. На обложку не добавляем фактов, которых в тексте нет.
