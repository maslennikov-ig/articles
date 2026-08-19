# Промты иллюстраций — «Как проверить отчёт нейросети: шесть приёмов подмены»

Статья: `articles/site/kak-proverit-otchet-neyroseti.md`
Площадка: сайт `aidevteam.ru`, раздел «Статьи»
Дата: 27.08.2026
Серия: четвёртая статья цикла, опорная — `podklyuchit-ii-k-crm`

---

## Сводный промт (скопировать целиком)

Один блок для агента с генерацией изображений. Внутри — выбранные варианты, альтернативы разобраны ниже и в генерацию не идут.

```
Сгенерируй 2 отдельных изображения для статьи. Каждое изображение — отдельный
файл. Не коллаж, не сетка, не несколько вариантов в одном файле.

Общий стиль для обоих кадров:
- почти чёрный фон с синим отливом, #0b1018–#0d1420, еле заметная тёмная сетка;
- ровно два акцентных цвета: бирюзово-голубой #29a8d0–#4cc4e8 и
  янтарно-оранжевый #f5a623–#ff6a2a; голубой = проверяемое, янтарный = то, что
  выглядит убедительно и не подтверждается; третий цвет не вводить;
- предметы светятся изнутри и роняют цветной отсвет на поверхность;
- кинематографический 3D-рендер, малая глубина резкости;
- соотношение 16:9, минимум 1600 px по ширине, целевой размер 1920x1080.

Запрещено в обоих кадрах: любой текст, цифры, читаемые надписи в ячейках
таблицы и на бумаге; третий цвет; внешний источник света, лампы, блики,
засветы, лучи; люди; мозги, нейросетевые графы, роботы и значки «это про ИИ»;
лупы, увеличительные стёкла, галочки и красные кресты; Пиноккио, маски и
прочие образы обмана; диаграммы, графики, шкалы, стрелки; фотореализм,
акварель, рисунок от руки, плоские иконки.

Кадр 1. Файл 01-hero.png — обложка статьи.
Cinematic 3D render, 16:9, a dark office at night, near-black #0b1018 with a blue
undertone. A printed, stapled report lies open on a wooden desk, seen from above
at a slight angle, its pages glowing cool cyan #4cc4e8 from within. The visible
page is ruled into a neat table of many rectangular cells; most cells are solid
paper and lit. But several cells in the middle of the table are not paper at all
— they are holes cut clean through the sheet, and through them the dark
woodgrain of the desk is visible, their cut edges rimmed in amber #f5a623. A pen,
two paper clips and a mug sit on the desk beside the report. The room beyond the
desk is dark. No text anywhere, no digits, no readable characters in any cell.
Objects lit only from within, no lamp, no external light source. Shallow depth of
field, 1920x1080.

Кадр 2. Файл 02-pustaya-ramka.png — иллюстрация к разделу про числа, которых нет.
Cinematic 3D render, 16:9, dark office #0d1420. Close-up at a shallow angle along
a shelf above a desk. On the shelf stand several small photo frames in a row,
each frame outlined in amber #f5a623 and holding nothing — through the glass only
the dark wall behind is visible. One frame at the near end is different: it holds
a solid cyan #4cc4e8 print, filled and lit, spilling light onto the shelf and
onto a mug standing below it. Sharp focus on the near frames, the row falling
into darkness further along the shelf. No text, no digits, no readable characters
inside any frame. Inner glow only, no external light. 1920x1080.

Сохрани оба файла в папку:
/home/me/code/articles/articles/pictures/kak-proverit-otchet-neyroseti/

В конце выведи список созданных файлов с их размерами в пикселях.
```

---

## Стилевой замок (общий для всего цикла)

Обязателен для обложки целиком, для внутренних кадров — только палитра, свет и фон.

- **Фон:** почти чёрный с синим отливом, `#0b1018`–`#0d1420`, еле заметная тёмная сетка.
- **Ровно два акцента:** бирюзово-голубой `#29a8d0`–`#4cc4e8` и янтарно-оранжевый `#f5a623`–`#ff6a2a`.
- **Смысл цвета в этом цикле:** голубой — проверяемое; янтарный — то, что выглядит убедительно и не подтверждается.
- **Свет:** объекты светятся изнутри, внешнего источника нет.
- **Исполнение:** чистый 3D-рендер или светящийся контур.
- **Внутренние кадры обязаны различаться по композиции и крупности.**

Предметный ряд этой статьи — раскрытый отчёт с прорезанными ячейками и полка с пустыми фоторамками. Картотека и папки заняты первой статьёй, весы и песочные часы — второй, доска с записками — третьей.

Проверка предметности: отчёт на столе · рамки на полке. Два разных существительных, оба кадра — предметные сцены.

---

## Обложка `01-hero` — 16:9, 1920×1080

### Вариант A ★★★★★ — предметная сцена

```
Cinematic 3D render, 16:9, a dark office at night, near-black #0b1018 with a blue
undertone. A printed, stapled report lies open on a wooden desk, seen from above
at a slight angle, its pages glowing cool cyan #4cc4e8 from within. The visible
page is ruled into a neat table of many rectangular cells; most cells are solid
paper and lit. But several cells in the middle of the table are not paper at all
— they are holes cut clean through the sheet, and through them the dark
woodgrain of the desk is visible, their cut edges rimmed in amber #f5a623. A pen,
two paper clips and a mug sit on the desk beside the report. The room beyond the
desk is dark. No text anywhere, no digits, no readable characters in any cell.
Objects lit only from within, no lamp, no external light source. Shallow depth of
field, 1920x1080.
```

Почему сильный: документ выглядит полным и аккуратным, пока не заметишь, что часть таблицы — сквозные дыры. Это ровно приём номер два из статьи. Стол, ручка и кружка делают сцену рабочей, а не выставочной.

### Вариант B ★★★★☆ — предметная сцена

```
Cinematic 3D render, 16:9, dark office #0d1420. A ring binder lies open on a desk,
filled with clear plastic sleeves. Most sleeves hold printed sheets glowing cyan
#4cc4e8. Four sleeves in the middle are completely empty — just transparent film
with the dark desk showing through, their edges catching amber #f5a623. The
binder's contents page on the left is fully lit, listing everything as present. A
mug stands at the edge of the desk. Dark room behind. No text, no digits, no
readable characters on any sheet. Inner glow only, no external light. 1920x1080.
```

Почему слабее: смысл тот же и даже точнее («опись считает страницы, которых нет»), но папка с файлами хуже читается в маленьком превью, чем раскрытый отчёт.

### Вариант C ★★★☆☆ — условный кадр

```
Cinematic 3D render, 16:9, near-black #0b1018. A single large report page stands
upright in the middle of the frame at a slight angle, glowing cyan #4cc4e8, ruled
into a table of rectangular cells. Several cells are holes cut through the page,
showing pure black behind them, their edges rimmed amber #f5a623. Wide empty
darkness around the page. No text, no digits, no readable characters. Inner glow
only. 1920x1080.
```

Почему слабее: тот же образ без комнаты и стола. Годится, если предметные варианты выйдут перегруженными, но обложка цикла держится на живой сцене.

## Внутренний кадр

### `02-pustaya-ramka` — в разделе «Шесть приёмов», после подраздела «Числа, которых физически нет»

Предметный кадр.

```
Cinematic 3D render, 16:9, dark office #0d1420. Close-up at a shallow angle along
a shelf above a desk. On the shelf stand several small photo frames in a row,
each frame outlined in amber #f5a623 and holding nothing — through the glass only
the dark wall behind is visible. One frame at the near end is different: it holds
a solid cyan #4cc4e8 print, filled and lit, spilling light onto the shelf and
onto a mug standing below it. Sharp focus on the near frames, the row falling
into darkness further along the shelf. No text, no digits, no readable characters
inside any frame. Inner glow only, no external light. 1920x1080.
```

- **alt:** `Полка с пустыми фоторамками, только в ближней есть заполненная светящаяся вставка`
- **Подпись:** `В одном отчёте 39 чисел стояли картинками, а картинки не приложены. В сводной таблице они значились измеренными`
- Композиция: крупный план под углом, уходящий ряд. Отличается от обложки крупностью и осью.

---

## Технические требования

- Соотношение 16:9, минимум 1600 px по ширине, комфортно 1920×1080.
- Формат исходника: PNG или JPG.
- Имена файлов ровно как в таблице ниже, строчными латинскими буквами.
- Класть в `articles/pictures/kak-proverit-otchet-neyroseti/`.

## Что НЕ генерировать

- **Никакого текста и цифр в кадре.** Особенно в таблице на обложке: неверная цифра на картинке к статье про проверку фактов — худшее, что может случиться.
- Третьего цвета.
- Внешнего источника света, бликов, засветов, лучей.
- Мозгов, нейросетевых графов, роботов, значков «это про ИИ».
- Луп, увеличительных стёкол, галочек и красных крестов: буквальная иллюстрация проверки.
- Пиноккио, масок, актёрских образов «обмана» — статья про метод, а не про злой умысел.
- Диаграмм, графиков, шкал, стрелок.
- Людей в кадре.
- Фотореализма, акварели, рисунка от руки, плоских иконок.

---

## Итоговая таблица

| Файл | Куда вставляется | alt | Подпись |
|---|---|---|---|
| `01-hero` | после вводных абзацев, до первого H2 | Как проверить отчёт нейросети: раскрытый отчёт на столе, часть ячеек таблицы прорезана насквозь | Отчёт с настоящей опорой и отчёт с подставленной выглядят одинаково |
| `02-pustaya-ramka` | в разделе «Шесть приёмов», после подраздела «Числа, которых физически нет» | Полка с пустыми фоторамками, только в ближней есть заполненная светящаяся вставка | В одном отчёте 39 чисел стояли картинками, а картинки не приложены. В сводной таблице они значились измеренными |
