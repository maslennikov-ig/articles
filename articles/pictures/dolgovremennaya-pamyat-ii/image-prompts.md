# Промты иллюстраций — «Долговременная память ИИ: нужен ли отдельный модуль»

Статья: `articles/site/dolgovremennaya-pamyat-ii.md`
Площадка: сайт `aidevteam.ru`, раздел «Статьи»
Дата: 25.08.2026
Серия: третья статья цикла, опорная — `podklyuchit-ii-k-crm`

---

## Пересъёмка 02 и 03

> **Пересъёмка кадров 02 и 03 (19.08.2026).** Первый прогон вернул их плоским
> векторным рендером, тогда как обложка вышла фотореалистичной. Внутри набора
> это разнобой, в ленте раздела заметен. Промты ниже дополнены явным
> требованием к исполнению — перегенерировать нужно только эти два кадра,
> обложка остаётся.

```
Сгенерируй 2 отдельных изображения, каждое отдельным файлом.

Исполнение для обоих кадров, это важнее композиции: фотореалистичный трёхмерный
предметный рендер, физически корректные материалы, настоящая фактура бумаги с
толщиной листа, мягкие тени, малая глубина резкости, как в первом кадре этого
набора (пробковая доска с записками). Не плоская векторная иллюстрация, не
инфографика, не двумерная схема, не изометрия.

Палитра: почти чёрный фон #0b1018–#0d1420, ровно два акцента — бирюзово-голубой
#29a8d0–#4cc4e8 и янтарно-оранжевый #f5a623–#ff6a2a, предметы светятся изнутри,
внешнего источника света нет. 16:9, 1920x1080. Никакого текста и цифр в кадре.

Кадр 1. Файл 02-odna-kopiya.png
Photorealistic cinematic 3D render, 16:9, dark office #0d1420. A desk seen from
the side at eye level. On it a tall neat stack of identical printed sheets,
dozens of real paper sheets with visible thickness and slightly uneven edges,
the whole stack glowing dull amber #f5a623. One single sheet near the top has
been pulled halfway out of the stack and glows bright cyan #4cc4e8, casting
light on the sheets above and below it and on the wooden desk surface. A metal
paper clip lies beside the stack, catching the cyan light. The room behind is
dark. Physically based materials, soft shadows, shallow depth of field. No text,
no digits, no readable characters on any sheet. Inner glow only, no lamp, no
external light source. Not a flat vector illustration, not an infographic.

Кадр 2. Файл 03-dve-storony.png
Photorealistic cinematic 3D render, 16:9, dark office #0b1018. Two identical
cardboard report folders lie open on a wooden desk next to each other, same size,
same worn cover, real paper texture. The left folder's visible page is completely
clean, glowing calm cyan #4cc4e8. The right folder's page is the same page, but
dozens of small coloured sticky flags stick out along its right edge, densely
packed and slightly curled, glowing amber #f5a623. A metal pen rests on the desk
between the two folders. Dark empty desk on both sides. Physically based
materials, soft shadows, shallow depth of field. No text, no digits, no readable
characters on either page. Inner glow only, no external light. Not a flat vector
illustration, not an infographic.

Сохрани оба файла в папку:
/home/me/code/articles/articles/pictures/dolgovremennaya-pamyat-ii/

В конце выведи список созданных файлов с их размерами в пикселях.
```

---

## Сводный промт (скопировать целиком)

Один блок для агента с генерацией изображений. Внутри — выбранные варианты, альтернативы разобраны ниже и в генерацию не идут.

```
Сгенерируй 3 отдельных изображения для статьи. Каждое изображение — отдельный
файл. Не коллаж, не сетка, не несколько вариантов в одном файле.

Общий стиль для всех трёх кадров:
- почти чёрный фон с синим отливом, #0b1018–#0d1420, еле заметная тёмная сетка;
- ровно два акцентных цвета: бирюзово-голубой #29a8d0–#4cc4e8 и
  янтарно-оранжевый #f5a623–#ff6a2a; голубой = действующее и читаемое,
  янтарный = устаревшее и немое; третий цвет не вводить;
- предметы светятся изнутри и роняют цветной отсвет на поверхность;
- кинематографический 3D-рендер, малая глубина резкости;
- соотношение 16:9, минимум 1600 px по ширине, целевой размер 1920x1080.

Запрещено во всех кадрах: любой текст, цифры, читаемые надписи и подписи;
третий цвет; внешний источник света, лампы, блики, засветы, объёмные лучи;
люди; мозги, нейросетевые графы, роботы и прочие значки «это про ИИ»;
диаграммы, графики, шкалы и стрелки; фотореализм, акварель, рисунок от руки,
плоские иконки; часы, календари и таймлайны.

Кадр 1. Файл 01-hero.png — обложка статьи.
Cinematic 3D render, 16:9, a dark office at night, near-black #0b1018 with a blue
undertone. A cork notice board hangs on the wall above a desk. Two paper notes of
exactly the same size are pinned to the board side by side with identical push
pins. The left note is old: yellowed, its bottom corner curled, the paper fibres
soft, glowing dull amber #f5a623. The right note is fresh and flat, glowing clean
cyan #4cc4e8, its light falling on the board and on the desk below. Nothing marks
either note as cancelled — no cross, no strike, no sticker. On the desk beneath,
a mug and a stack of pins. The room around the board is dark. No text anywhere,
no digits, no readable handwriting on either note. Objects lit only from within,
no lamp, no external light source. Shallow depth of field, 1920x1080.

Кадр 2. Файл 02-odna-kopiya.png — иллюстрация к разделу про массовые замены.
Cinematic 3D render, 16:9, dark office #0d1420. A desk seen from the side. On it a
tall neat stack of identical printed sheets, dozens of them, all the same, edges
perfectly aligned, the whole stack glowing dull amber #f5a623. One single sheet
near the top has been pulled halfway out of the stack and glows bright cyan
#4cc4e8, its light falling on the sheets above and below it and on the desk. A
paper clip lies beside the stack. The room behind is dark. No text, no digits, no
readable characters on any sheet. Inner glow only, no external light. 1920x1080.

Кадр 3. Файл 03-dve-storony.png — иллюстрация к разделу про два ответа на один вопрос.
Cinematic 3D render, 16:9, dark office #0b1018. Two identical report folders lie
open on a desk next to each other, same size, same cover. The left folder's
visible page is completely clean, glowing calm cyan #4cc4e8. The right folder's
page is exactly the same page, but dozens of small coloured sticky flags stick
out along its edge, densely packed, glowing amber #f5a623 — the same document,
marked up beyond recognition. A pen rests between the two folders. Dark empty
desk on both sides. No text, no digits, no readable characters on either page.
Inner glow only, no external light. 1920x1080.

Сохрани все три файла в папку:
/home/me/code/articles/articles/pictures/dolgovremennaya-pamyat-ii/

В конце выведи список созданных файлов с их размерами в пикселях.
```

---

## Стилевой замок (общий для всего цикла)

Обязателен для обложки целиком, для внутренних кадров — только палитра, свет и фон.

- **Фон:** почти чёрный с синим отливом, `#0b1018`–`#0d1420`, еле заметная тёмная сетка.
- **Ровно два акцента:** бирюзово-голубой `#29a8d0`–`#4cc4e8` и янтарно-оранжевый `#f5a623`–`#ff6a2a`. Третий цвет не вводить.
- **Смысл цвета в этом цикле:** голубой — действующее, читаемое, надёжное; янтарный — устаревшее, немое, дорогое.
- **Свет:** объекты светятся изнутри и роняют цветной отсвет на поверхность. Внешнего источника нет.
- **Исполнение:** чистый 3D-рендер или светящийся контур.
- **Внутренние кадры обязаны различаться по композиции и крупности.**

Предметный ряд этой статьи — пробковая доска с записками, стопка одинаковых распечаток, две раскрытые папки-отчёта. Картотека и папки со штемпелем заняты первой статьёй, весы и песочные часы — второй; здесь повторяется только палитра.

Проверка предметности: доска с записками · стопка распечаток · две папки с закладками. Три разных существительных, все три кадра — предметные сцены.

---

## Обложка `01-hero` — 16:9, 1920×1080

### Вариант A ★★★★★ — предметная сцена

```
Cinematic 3D render, 16:9, a dark office at night, near-black #0b1018 with a blue
undertone. A cork notice board hangs on the wall above a desk. Two paper notes of
exactly the same size are pinned to the board side by side with identical push
pins. The left note is old: yellowed, its bottom corner curled, the paper fibres
soft, glowing dull amber #f5a623. The right note is fresh and flat, glowing clean
cyan #4cc4e8, its light falling on the board and on the desk below. Nothing marks
either note as cancelled — no cross, no strike, no sticker. On the desk beneath,
a mug and a stack of pins. The room around the board is dark. No text anywhere,
no digits, no readable handwriting on either note. Objects lit only from within,
no lamp, no external light source. Shallow depth of field, 1920x1080.
```

Почему сильный: старая договорённость и новая висят рядом, обе одинаково «действующие», и отличить их можно только по возрасту бумаги. Сцена собирается из настоящих вещей, читается без подписи и не повторяет картотеку и весы из соседних статей цикла.

### Вариант B ★★★★☆ — предметная сцена

```
Cinematic 3D render, 16:9, dark office #0d1420. A desk with a printed price sheet
lying on it, glowing dull amber #f5a623. A second, identical sheet has just been
put down on top of it, slightly offset, glowing cyan #4cc4e8 — the older one
shows underneath along two edges. A stapler and a pen lie nearby. The room is
dark beyond the desk. No text, no digits, no readable characters on either sheet.
Inner glow only, no external light. 1920x1080.
```

Почему слабее: точнее про «новая цена поверх старой», но два листа бумаги друг на друге хуже читаются в маленьком превью ленты.

### Вариант C ★★★☆☆ — условный кадр

```
Cinematic 3D render, 16:9, near-black #0b1018 with a faint grid. Close view of an
open card-index drawer from slightly above. Two identical cards stand side by
side, indistinguishable in outline. The left card glows amber #f5a623 and carries
a heavy diagonal strike-through bar. The right card glows cyan #4cc4e8 and is
clean. All other cards stay unlit. Wide empty dark space above. No text, no
digits, no readable characters. Inner glow only. 1920x1080.
```

Почему слабее: сам приём хороший, но ящик картотеки уже занят обложкой опорной статьи цикла — лента раздела начнёт повторяться.

## Внутренние кадры

### `02-odna-kopiya` — в разделе «Кейс: 68 413 записей и ни одной отменённой»

Предметный кадр.

```
Cinematic 3D render, 16:9, dark office #0d1420. A desk seen from the side. On it a
tall neat stack of identical printed sheets, dozens of them, all the same, edges
perfectly aligned, the whole stack glowing dull amber #f5a623. One single sheet
near the top has been pulled halfway out of the stack and glows bright cyan
#4cc4e8, its light falling on the sheets above and below it and on the desk. A
paper clip lies beside the stack. The room behind is dark. No text, no digits, no
readable characters on any sheet. Inner glow only, no external light. 1920x1080.
```

- **alt:** `Стопка одинаковых распечаток, из которой наполовину вытянут один светящийся лист`
- **Подпись:** `Из 17 657 замен 17 008 не изменили ни одного значения. Настоящих изменений — каждое двадцать шестое`
- Композиция: широкий боковой план, горизонтальный ритм.

### `03-dve-storony` — в разделе «Кейс», после таблицы с нулём и 649

Предметный кадр.

```
Cinematic 3D render, 16:9, dark office #0b1018. Two identical report folders lie
open on a desk next to each other, same size, same cover. The left folder's
visible page is completely clean, glowing calm cyan #4cc4e8. The right folder's
page is exactly the same page, but dozens of small coloured sticky flags stick
out along its edge, densely packed, glowing amber #f5a623 — the same document,
marked up beyond recognition. A pen rests between the two folders. Dark empty
desk on both sides. No text, no digits, no readable characters on either page.
Inner glow only, no external light. 1920x1080.
```

- **alt:** `Две одинаковые раскрытые папки-отчёта: в одной чистая страница, в другой та же страница в закладках`
- **Подпись:** `Один и тот же вопрос к одной базе: ноль противоречий или 649. Оба ответа формально верные`
- Композиция: взгляд сверху на два одинаковых предмета рядом. Отличается от `02` осью и планом.

---

## Технические требования

- Соотношение 16:9, минимум 1600 px по ширине, комфортно 1920×1080.
- Формат исходника: PNG или JPG. Конвертацию делает конвейер.
- Имена файлов ровно как в таблице ниже, строчными латинскими буквами.
- Класть в `articles/pictures/dolgovremennaya-pamyat-ii/`.

## Что НЕ генерировать

- **Никакого текста и цифр в кадре.** Ни «649», ни «96 %», ни дат.
- Третьего цвета. Только голубой и янтарный на почти чёрном.
- Внешнего источника света, бликов, засветов, объёмных лучей.
- Мозгов, нейросетевых графов, роботов, значков «это про ИИ».
- Часов, календарей и таймлайнов: буквальная иллюстрация слова «время» — самый затёртый кадр в этой теме. Песочные часы заняты второй статьёй цикла.
- Диаграмм, графиков, шкал, полос и стрелок.
- Людей в кадре.
- Фотореализма, акварели, рисунка от руки, плоских иконок.

---

## Итоговая таблица

| Файл | Куда вставляется | alt | Подпись |
|---|---|---|---|
| `01-hero` | после вводных абзацев, до первого H2 | Долговременная память ИИ: две записки на пробковой доске, старая пожелтевшая и свежая, обе приколоты одинаково | Старое значение и новое висят рядом, и ничто не помечено отменённым |
| `02-odna-kopiya` | в разделе «Кейс: 68 413 записей и ни одной отменённой», после абзаца про 17 008 вытеснений | Стопка одинаковых распечаток, из которой наполовину вытянут один светящийся лист | Из 17 657 замен 17 008 не изменили ни одного значения. Настоящих изменений — каждое двадцать шестое |
| `03-dve-storony` | в том же разделе, сразу после таблицы «0 или 649» | Две одинаковые раскрытые папки-отчёта: в одной чистая страница, в другой та же страница в закладках | Один и тот же вопрос к одной базе: ноль противоречий или 649. Оба ответа формально верные |
