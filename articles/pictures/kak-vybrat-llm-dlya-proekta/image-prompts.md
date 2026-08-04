# Промты для иллюстраций: «Как выбрать LLM для проекта и не переплатить в сорок раз»

Статья: `articles/site/kak-vybrat-llm-dlya-proekta.md`
Публикация: `aidevteam.ru/blog/kak-vybrat-llm-dlya-proekta`
Дата: 2026-08-03

**Все 5 изображений сгенерированы и переименованы** (2026-08-03), 1672×941.
Плюс две Mermaid-диаграммы в тексте — см. пункт 06.

---

## Стилистика сайта (обязательна для всех пяти)

Снята с обложек и внутренних иллюстраций статей июля 2026:
`pochemu-ne-rabotaet-vnedrenie-ii`, `zamenit-li-ii-razrabotchikov`,
`ai-bot-dlya-prodazh`. Единая система, отступать от неё нельзя — картинки
попадают в общую ленту раздела и должны читаться как один набор.

- **Фон:** почти чёрный с синим отливом, `#0b1018`–`#0d1420`. Иногда еле
  заметная тёмная сетка. Никаких светлых фонов.
- **Ровно два акцентных цвета:**
  - бирюзово-голубой `#29a8d0`–`#4cc4e8`
  - янтарно-оранжевый `#f5a623`–`#ff6a2a`, в глубину уходит в красный
- **Цвет несёт смысл, а не украшает.** Голубой — ровное, надёжное,
  предсказуемое, машинное. Оранжевый — неустойчивое, рискованное, дорогое.
  В каждой картинке этой статьи распределение именно такое.
- **Свет:** объекты светятся изнутри и роняют цветной отсвет на пол под собой.
  Внешнего источника света нет.
- **Композиция:** один-два объекта, много пустого тёмного пространства,
  сопоставление слева-справа. Никакой мелкой детализации по углам.
- **Исполнение:** чистый 3D-рендер или светящийся контурный рисунок.
  Не фотореализм, не иллюстрация «от руки», не плоские иконки.
- **Соотношение:** 16:9.

Хвост промта, общий для всех пяти:

```
Dark near-black background #0b1018 with a very subtle darker grid. Objects glow
from within and cast coloured light onto the floor beneath them; no external
light source. Exactly two accent colours: teal-cyan #29a8d0 to #4cc4e8 and amber
orange #f5a623 to #ff6a2a. Clean 3D render, generous empty space, no text, no
labels, no numbers, no logos. Aspect ratio 16:9.
```

### Что НЕ генерировать

- Текст и цифры в любом виде. Кириллицу генераторы пишут плохо, а неверное
  число рядом со статьёй про точность измерений подрывает доверие ко всему
  тексту. Весь смысл — в подписи под картинкой.
- Роботов, андроидов, человекоподобные машины.
- Изометрические схемы с circuit board и «нейросетями из точек» — это старый
  стиль сайта, он выведен из обращения.
- Третий акцентный цвет. Зелёный, фиолетовый, розовый не использовать.
- Светлый или белый фон.
- Образ «ровная стена блоков рядом с качелями» — занят в статье про ИИ-бота
  для продаж, две соседние статьи не должны иллюстрироваться одинаково.

---

## 01. Обложка

**Файл:** `01-hero`
**Alt:** `Два одинаковых светящихся куба с ярлыками резко разного размера`
**Подпись:** `Один и тот же ответ. Разница в счёте — до двадцати двух раз`

### Вариант A ★★★★★

```
Two identical glowing teal-cyan cubes standing side by side on a dark reflective
floor, exactly the same size and shape. A small amber-orange tag hangs from the
first cube on a thin glowing thread; from the second hangs a hugely oversized
amber tag, many times larger, almost dwarfing the cube itself. Both tags are
completely blank. Dark near-black background #0b1018 with a very subtle darker
grid. Objects glow from within and cast coloured light onto the floor beneath
them; no external light source. Exactly two accent colours: teal-cyan #29a8d0 to
#4cc4e8 and amber orange #f5a623 to #ff6a2a. Clean 3D render, generous empty
space, no text, no labels, no numbers, no logos. Aspect ratio 16:9.
```

Почему так: главная мысль статьи — товар один, цена разная. Разница передана
размером ярлыка, товар остаётся голубым и одинаковым. Цифра не нужна.

### Вариант B ★★★★

```
Two identical glowing teal-cyan spheres resting on a dark reflective floor. The
left one sits on a low plain platform, the right one on a towering amber-orange
pedestal many times taller, though the sphere on top is exactly the same size.
Dark near-black background #0b1018 with a very subtle darker grid. Objects glow
from within and cast coloured light onto the floor beneath them; no external
light source. Exactly two accent colours: teal-cyan #29a8d0 to #4cc4e8 and amber
orange #f5a623 to #ff6a2a. Clean 3D render, generous empty space, no text, no
labels, no numbers, no logos. Aspect ratio 16:9.
```

Пьедестал как метафора цены читается мгновенно, но ярлык ближе к теме тарифов.

---

## 02. После раздела «У одной модели не одна цена, а одиннадцать»

**Файл:** `02-odinnadcat-cennikov`
**Alt:** `От одного светящегося куба веером расходится множество ярлыков разного размера`
**Подпись:** `Один и тот же товар у разных продавцов. Тариф зависит от того, через кого вы к нему пришли`

### Вариант A ★★★★★

```
A single glowing teal-cyan cube at the centre of a dark reflective floor, with
about a dozen blank amber-orange tags radiating outward from it on thin glowing
threads, fanning in different directions. The tags vary dramatically in size,
from tiny to oversized. All tags are completely blank. Dark near-black background
#0b1018 with a very subtle darker grid. Objects glow from within and cast
coloured light onto the floor beneath them; no external light source. Exactly two
accent colours: teal-cyan #29a8d0 to #4cc4e8 and amber orange #f5a623 to
#ff6a2a. Clean 3D render, generous empty space, no text, no labels, no numbers,
no logos. Aspect ratio 16:9.
```

### Вариант B ★★★

```
A single glowing teal-cyan cube with many blank amber-orange tags stacked and
overlapping on one side, hanging like layered price labels on a shop item.
[общий хвост стилистики]
```

Компактнее, но «одиннадцать разных» читается хуже, чем веер.

---

## 03. После раздела «Режим размышлений: восемь минут работы и ноль слов»

**Файл:** `03-tihiy-nol`
**Alt:** `Плотный клубок оранжевого свечения, а на выходе — пустая голубая пластина`
**Подпись:** `Восемь с половиной минут работы, тридцать три тысячи оплаченных токенов, ноль слов на выходе`

### Вариант A ★★★★★

```
A dense, tangled knot of glowing amber-orange energy filaments churning inside an
open dark chamber on the left, extremely intricate and tightly wound. On the
right, emerging from a narrow slot in the chamber, a single perfectly flat, empty
teal-cyan plate slides out — completely smooth and blank, nothing on its surface.
The contrast between the furious tangle and the empty output is the subject. Dark
near-black background #0b1018 with a very subtle darker grid. Objects glow from
within and cast coloured light onto the floor beneath them; no external light
source. Exactly two accent colours: teal-cyan #29a8d0 to #4cc4e8 and amber orange
#f5a623 to #ff6a2a. Clean 3D render, generous empty space, no text, no labels, no
numbers, no logos. Aspect ratio 16:9.
```

Почему так: «очень много работы, ноль результата» — это контраст плотности и
пустоты. Оранжевый клубок = размышления, голубая пустая пластина = то, что
получил пользователь.

### Вариант B ★★★★

```
An hourglass shape rendered in glowing amber-orange, with all its sand already
run through into the lower bulb, standing beside a single flat empty teal-cyan
plate on a dark reflective floor. The lower bulb is densely packed; the plate is
entirely blank.
[общий хвост стилистики]
```

Спокойнее и понятнее в маленьком размере, но теряет мысль про интенсивность.

---

## 04. После раздела «Место в англоязычном рейтинге ничего не говорит о работе на русском»

**Файл:** `04-inorodnye-znaki`
**Alt:** `В ровных рядах голубых штрихов несколько оранжевых знаков чужой формы`
**Подпись:** `По смыслу ответ безупречен. Отправить его клиенту нельзя`

### Вариант A ★★★★★

```
Neat parallel rows of short glowing teal-cyan dashes filling a dark surface like
lines of abstract unreadable text — uniform rhythm, even spacing, no legible
letters of any alphabet. Scattered among them, four or five amber-orange marks of
a visibly different shape break the rhythm: thicker, angular, clearly foreign to
the pattern. Dark near-black background #0b1018 with a very subtle darker grid.
Objects glow from within and cast coloured light onto the floor beneath them; no
external light source. Exactly two accent colours: teal-cyan #29a8d0 to #4cc4e8
and amber orange #f5a623 to #ff6a2a. Clean 3D render, generous empty space, no
text, no labels, no numbers, no logos. Aspect ratio 16:9.
```

Важно: просить именно «абстрактные нечитаемые штрихи», а не текст. Иначе
генератор напишет исковерканную латиницу, и картинку придётся переделывать.

### Вариант B ★★★

```
The same rows of glowing teal-cyan dashes, but in one area the pattern is
visibly damaged: several dashes are smeared, broken and bleeding into amber
orange, as if the print failed on that spot. The rest of the field is perfectly
clean.
[общий хвост стилистики]
```

Ближе к рассыпавшемуся тексту Gemma, чем к иероглифам. Обе находки в разделе
описаны, так что вариант рабочий.

---

## 05. После раздела «Предсказуемость бюджета важнее цены за токен»

**Файл:** `05-kuchno-i-vrazbros`
**Alt:** `Две мишени: на одной попадания легли кучно, на другой разбросаны по всему полю`
**Подпись:** `Ровный на восемьдесят пять лучше, чем иногда восемьдесят четыре, а иногда шестьдесят семь`

### Вариант A ★★★★★

```
Two identical circular targets standing upright side by side on a dark reflective
floor, shown straight on. The left target has a tight cluster of glowing
teal-cyan hit marks grouped closely together. The right target has the same
number of amber-orange hit marks, but scattered widely across the whole face,
some near the edge. Same number of marks on both, the only difference is the
spread. Dark near-black background #0b1018 with a very subtle darker grid.
Objects glow from within and cast coloured light onto the floor beneath them; no
external light source. Exactly two accent colours: teal-cyan #29a8d0 to #4cc4e8
and amber orange #f5a623 to #ff6a2a. Clean 3D render, generous empty space, no
text, no labels, no numbers, no logos. Aspect ratio 16:9.
```

Почему так: раздел про разброс, а не про уровень, — и мишени это единственный
образ, где одинаковое количество попаданий при разной кучности видно сразу.
Одинаковое число отметок принципиально, это и есть «средний балл тот же».

### Вариант B ★★★

```
Two glowing horizon lines stretching across a dark field: the upper one perfectly
straight and steady in teal-cyan, the lower one jagged and erratic in amber
orange, both spanning the same width.
[общий хвост стилистики]
```

Проще в генерации, но линии слишком близки к обычному графику и читаются как
«хуже/лучше», а не как «ровнее/скачет».

---

## 06. Схемы Mermaid — вставлены в текст, генерировать не нужно

В статье две диаграммы, обе уже в markdown:

- `flowchart LR` в разделе «Прайс-лист и счёт — разные числа» — путь от прайса
  до фактического списания;
- `flowchart TD` в разделе «Как выбрать LLM для проекта: короткий ответ» —
  порядок проверки модели под задачу.

**Рендер на момент вставки ещё не работает.** В блоге блок ```mermaid отдаётся
как подсвеченный код: `MermaidClient` подключён только на страницах паспортов
`/p/[slug]`. Задача на доработку передана агенту репозитория сайта; до её
приёмки статью не публиковать, иначе диаграммы приедут исходником.

Проверить перед публикацией: на `/blog/kak-vybrat-llm-dlya-proekta` вместо
блоков кода видны SVG-диаграммы.

---

## Итоговая таблица

| Файл | Место вставки | Alt | Подпись |
|---|---|---|---|
| `01-hero` | обложка, `featuredImage` | Два одинаковых светящихся куба с ярлыками резко разного размера | Один и тот же ответ. Разница в счёте — до двадцати двух раз |
| `02-odinnadcat-cennikov` | после «У одной модели не одна цена, а одиннадцать» | От одного светящегося куба веером расходится множество ярлыков разного размера | Один и тот же товар у разных продавцов. Тариф зависит от того, через кого вы к нему пришли |
| `03-tihiy-nol` | после «Режим размышлений: восемь минут работы и ноль слов» | Плотный клубок оранжевого свечения, а на выходе — пустая голубая пластина | Восемь с половиной минут работы, тридцать три тысячи оплаченных токенов, ноль слов на выходе |
| `04-inorodnye-znaki` | после «Место в англоязычном рейтинге ничего не говорит о работе на русском» | В ровных рядах голубых штрихов несколько оранжевых знаков чужой формы | По смыслу ответ безупречен. Отправить его клиенту нельзя |
| `05-kuchno-i-vrazbros` | после «Предсказуемость бюджета важнее цены за токен» | Две мишени: на одной попадания легли кучно, на другой разбросаны по всему полю | Ровный на восемьдесят пять лучше, чем иногда восемьдесят четыре, а иногда шестьдесят семь |

---

## Технические требования

- **Обложка:** минимум 1920×1080.
- **Внутренние:** минимум 1600 пикселей по ширине — конвейер всё равно ужимает
  до 1600 и делает WebP с AVIF.

## Что делать после генерации

1. Положить файлы в `articles/pictures/kak-vybrat-llm-dlya-proekta/` под именами
   из таблицы, расширение любое из png/jpg/webp.
2. Сказать об этом — дальше конвейер, проверка и публикация идут без вас.

Агент перед публикацией открывает каждое изображение и сверяет с текстом. Если
на картинке окажется читаемый текст, цифра или третий акцентный цвет — файл
вернётся на перегенерацию с исправленным промтом.
