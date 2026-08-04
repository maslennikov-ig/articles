# Иллюстрации: «Как снизить расходы на LLM: пять множителей в счёте»

Статья: `articles/site/kak-snizit-rashody-na-llm.md` (сайт, режим адаптации).
Пять изображений: обложка плюс четыре внутри.

Стиль снят с обложек `kak-vybrat-llm-dlya-proekta`, `pochemu-ne-rabotaet-vnedrenie-ii`
и `zamenit-li-ii-razrabotchikov`: почти чёрный фон с еле заметной сеткой, светящиеся
изнутри 3D-объекты, ровно два акцента — бирюзово-голубой и янтарно-оранжевый, цветной
отсвет на полу, внешнего источника света нет.

**Цвет несёт смысл:** бирюзовый — дёшево, ровно, предсказуемо. Янтарный — дорого,
неустойчиво, рискованно.

**Метафора «два объекта с ценниками» занята** обложкой `kak-vybrat-llm-dlya-proekta`
(два куба с ярлыками разного размера). Здесь она не повторяется — вместо сравнения
двух вариантов работает идея потока, который проходит через несколько сужений.

**Текста на изображениях нет.** Кириллицу генераторы пишут с ошибками, поэтому смысл
выносится в подпись под картинкой.

---

## 01-hero — обложка

### Вариант A ★★★★★

```
Cinematic 3D render, 16:9, near-black background #0b1018 with a barely visible dark grid,
no external light source, objects glow from within.
A single thick horizontal stream of light enters from the left edge, wide and amber-orange,
pulsing. It passes through five consecutive ring-shaped valves standing along its path.
After every valve the stream is visibly thinner and shifts further toward cyan-blue.
By the right edge it is a narrow, calm turquoise thread.
Each valve is a simple glowing ring, no mechanical detail, no gauges, no text anywhere.
The floor is dark polished stone catching an amber reflection on the left and a cyan one on the right.
Wide empty space above the stream. No characters, no logos, no numbers, no lettering.
```

### Вариант B ★★★★☆

```
Cinematic 3D render, 16:9, near-black background #0d1420 with a faint grid, self-illuminated objects.
Five glowing rings of decreasing diameter are arranged in perspective, receding from the viewer
like a tunnel. The nearest ring is large and amber-orange, the farthest is small and cyan-blue,
the three between them blend gradually from one accent to the other.
A soft beam of light travels through all five, narrowing as it goes.
Polished dark floor with coloured reflections beneath the rings.
No text, no characters, no logos, no interface elements, no numbers.
```

**Куда:** `featuredImage`, шапка статьи.
**alt:** `Как снизить расходы на LLM: поток света проходит через пять сужений и становится тоньше`
**Подпись:** не нужна, обложка идёт без подписи.

---

## 02-shest-marshrutov

```
Cinematic 3D render, 16:9, near-black background #0b1018 with a faint grid, inner glow only.
One large calm cyan-blue sphere sits at the right, softly lit, clearly the destination.
Six separate light channels run toward it from the left, all ending at the same sphere.
The channels differ dramatically in thickness: the topmost is a thin, quiet turquoise line,
the bottom one is a wide, heavy, amber-orange conduit, the rest scale between them.
Same destination, wildly different pipes. Dark polished floor with coloured reflections.
No text, no labels, no logos, no characters, no numbers.
```

**Куда:** после H2 «Почему одна и та же модель стоит по-разному».
**alt:** `Шесть маршрутов разной толщины ведут к одной и той же модели`
**Подпись:** `Одна модель, шесть маршрутов. Разница между крайними тарифами — двадцать два раза.`
**Зачем:** читатель понимает главный тезис статьи раньше, чем дочитает раздел: «модель» и «маршрут до модели» — разные вещи.

---

## 03-tri-ocheredi

```
Isometric 3D render, 16:9, deep near-black background #0d1420, self-illuminated geometry.
Three parallel lanes of identical small glowing cubes move toward one shared gate on the right.
The top lane is short and sparse, its cubes amber-orange, already almost at the gate.
The middle lane is medium length, cubes a neutral pale blue.
The bottom lane is long and dense, cubes calm turquoise, patiently queued, with the widest gap
between the last cube and the gate.
All three lanes end at the same single gate — this must read clearly.
Dark polished floor, coloured reflections under each lane. No faces, no robots, no text,
no logos, no numbers.
```

**Куда:** после H2 «Класс обслуживания: вдвое дешевле за фоновые задачи».
**alt:** `Три очереди разной длины ведут к одному серверу — классы обслуживания`
**Подпись:** `Класс обслуживания меняет место в очереди, а не модель. Экономкласс вдвое дешевле стандартного.`
**Зачем:** «класс обслуживания» — незнакомый бизнес-читателю термин, и картинка объясняет его быстрее абзаца.

---

## 04-postoyannaya-chast

```
Cinematic 3D render, 16:9, near-black background #0b1018 with a faint grid.
Four horizontal bars stacked vertically with even spacing, each representing one request.
Every bar is made of two segments: a long left segment and a short right segment.
In the top bar both segments glow amber-orange at full intensity.
In the three bars below, the long left segment is dimmed to a deep, almost cold turquoise —
present but visibly cheap — while the short right segment stays bright amber.
The left segments align perfectly with each other, forming a clean vertical edge:
the repeated, unchanged part. Dark polished floor with a faint coloured reflection.
No text, no numbers, no labels, no characters.
```

**Куда:** после H2 «Кэш промпта: самый недооценённый рычаг».
**alt:** `Четыре запроса, у которых одинаковое начало оплачивается только один раз`
**Подпись:** `Кэш переиспользует неизменное начало запроса. В нашем замере это снизило цену вызова в 3,9 раза.`
**Зачем:** механика кэша объясняется в одном кадре — платим полностью только за первый запрос.

---

## 05-porog

```
Cinematic 3D render, 16:9, near-black background #0d1420, faint grid.
A single continuous ribbon of light runs from left to right across the frame.
For the left two thirds it is flat, thin and calm turquoise.
At a precise point it hits an invisible step and jumps sharply upward, and from that point on
it is thicker, brighter and amber-orange, continuing to the right edge.
The break is abrupt, not a gradient — a clean vertical jump at one exact position.
Dark polished floor, turquoise reflection on the left, amber on the right.
No axes, no chart furniture, no text, no numbers, no labels, no characters.
```

**Куда:** после H2 «Порог, о котором не написано в прайс-листе».
**alt:** `Цена запроса скачком растёт после превышения порога длины контекста`
**Подпись:** `Тарифный порог срабатывает молча. У Qwen3.7 Flash — уже на 32 тысячах входных токенов.`
**Зачем:** показывает, что рост не плавный, а ступенчатый, — именно это ломает расчёт бюджета по прайс-листу.

---

## Технические требования

- **Размер:** 16:9, от 1600 по ширине (конвейер ресайзит до 1600), комфортно 1920×1080
- **Формат исходников:** PNG или JPG, конвейер сам сделает WebP и AVIF
- **Фон:** `#0b1018`–`#0d1420`, светлых фонов нет
- **Акценты:** бирюзово-голубой `#29a8d0`–`#4cc4e8` и янтарно-оранжевый `#f5a623`–`#ff6a2a`. Третий цвет не вводить
- **Исполнение:** чистый 3D-рендер со свечением изнутри, отсвет на полу
- **Текст на изображении:** отсутствует полностью

## Что НЕ генерировать

- Текст и цифры на картинке — кириллица выходит с опечатками, а цифра с ошибкой подрывает доверие ко всей статье
- Два объекта с ценниками — эта метафора уже стоит на обложке статьи про выбор модели
- Логотипы OpenAI, Azure, OpenRouter и других упомянутых компаний
- Роботов, лица, человеческие фигуры
- Мешки денег, монеты, купюры: статья про инженерное решение, а не про финансовый успех
- Circuit board, неоновые сети из точек, роботизированные руки, золотой как третий цвет — это устаревший стиль раздела
- Фотореализм и рисунок от руки

## Итоговая таблица

| Файл | Место вставки | alt | Подпись |
|---|---|---|---|
| `01-hero` | шапка | Как снизить расходы на LLM: поток света проходит через пять сужений и становится тоньше | — |
| `02-shest-marshrutov` | после «Почему одна и та же модель стоит по-разному» | Шесть маршрутов разной толщины ведут к одной и той же модели | Одна модель, шесть маршрутов. Разница между крайними тарифами — двадцать два раза. |
| `03-tri-ocheredi` | после «Класс обслуживания» | Три очереди разной длины ведут к одному серверу — классы обслуживания | Класс обслуживания меняет место в очереди, а не модель. Экономкласс вдвое дешевле стандартного. |
| `04-postoyannaya-chast` | после «Кэш промпта» | Четыре запроса, у которых одинаковое начало оплачивается только один раз | Кэш переиспользует неизменное начало запроса. В нашем замере это снизило цену вызова в 3,9 раза. |
| `05-porog` | после «Порог, о котором не написано в прайс-листе» | Цена запроса скачком растёт после превышения порога длины контекста | Тарифный порог срабатывает молча. У Qwen3.7 Flash — уже на 32 тысячах входных токенов. |

---

**ГЕЙТ.** Публикация не начинается, пока готовые PNG не лежат в этой папке.
Дальше агент переименует их по таблице, прогонит конвейер, откроет каждый файл
и сверит с текстом статьи.
