# Промты иллюстраций — «Поиск по базе знаний с ИИ: почему он не находит нужное»

Статья: `articles/site/poisk-po-baze-znaniy-s-ii.md`
Площадка: сайт `aidevteam.ru`, раздел «Статьи»
Дата: 21.08.2026
Серия: вторая статья цикла, опорная — `podklyuchit-ii-k-crm`


> **Статус на 19.08.2026: картинки по этому набору уже сгенерированы** — по
> прежней версии промтов (две дорожки к ящику, весы со стопками, карточки с
> песочными часами). `alt` и подписи в статье соответствуют им.
>
> Предметные варианты ниже — на случай пересъёмки.

---

## Сводный промт (скопировать целиком)

> Набор уже снят по прежней версии промтов. Этот блок — для пересъёмки: он
> собран из предметных вариантов. Если запустите его, `alt` и подписи в статье
> нужно вернуть к формулировкам из итоговой таблицы этого файла.

```
Сгенерируй 3 отдельных изображения для статьи. Каждое изображение — отдельный
файл. Не коллаж, не сетка, не несколько вариантов в одном файле.

Общий стиль для всех трёх кадров:
- почти чёрный фон с синим отливом, #0b1018–#0d1420, еле заметная тёмная сетка;
- ровно два акцентных цвета: бирюзово-голубой #29a8d0–#4cc4e8 и
  янтарно-оранжевый #f5a623–#ff6a2a; голубой = то, на что можно опереться,
  янтарный = то, что лежит рядом и дорого обходится; третий цвет не вводить;
- предметы светятся изнутри и роняют цветной отсвет на поверхность;
- кинематографический 3D-рендер, малая глубина резкости;
- соотношение 16:9, минимум 1600 px по ширине, целевой размер 1920x1080.

Запрещено во всех кадрах: любой текст, цифры, читаемые надписи на бумагах,
карточках и закладках; третий цвет; внешний источник света, лампы, блики,
засветы, объёмные лучи; люди; мозги, нейросетевые графы, роботы и значки «это
про ИИ»; лупы, увеличительные стёкла и значок поиска; диаграммы, графики,
шкалы, полосы и стрелки; фотореализм, акварель, рисунок от руки, плоские иконки.

Кадр 1. Файл 01-hero.png — обложка статьи.
Cinematic 3D render, 16:9, a dark office room at night, near-black #0b1018 with a
blue undertone. A wooden desk seen from slightly above. Two things lie on it side
by side. On the left, an open address book with cut alphabetical thumb tabs down
its edge; one page is turned to a tab and glows clean cyan #4cc4e8, its light
falling on the desk. On the right, a cardboard folder lies open and a fan of
loose paper clippings has spilled out of it across the desk, each clipping marked
with a small coloured sticky flag; the whole spill glows warm amber #f5a623, more
diffuse, no single bright point. A mug and a pen sit at the top edge of the desk.
The room behind is empty darkness. No text anywhere, no digits, no readable
characters on the pages, clippings or tabs. Objects lit only from within, no
lamp, no external light source, no beams. Shallow depth of field, 1920x1080.

Кадр 2. Файл 02-vesy.png — иллюстрация к разделу про объединение двух веток поиска.
Cinematic 3D render, 16:9, dark office #0d1420. A classic two-pan balance scale
stands on a desk, its brass frame glowing faint cyan #29a8d0. On the left pan: a
thick document folder, stuffed with papers, its edges glowing cyan #4cc4e8. On
the right pan: an identical folder of exactly the same thickness, but its covers
have fallen slightly open and it is completely empty inside, glowing amber
#f5a623. The beam is perfectly level — the two folders balance. A mug stands on
the desk beside the scale. Dark empty room to the right. No text, no digits, no
readable characters on any paper. Inner glow only, no external light. 1920x1080.

Кадр 3. Файл 03-sorok-kartochek.png — иллюстрация к разделу про второй проход.
Cinematic 3D render, 16:9, dark office #0b1018. Top-down view of a desk with about
forty index cards laid out face down in a loose grid, each glowing dim cyan
#29a8d0. A handful of cards near the centre have been turned face up and glow
brighter cyan #4cc4e8. Standing on the same desk beside them, a tall hourglass
with amber #f5a623 sand glowing from within, most of the sand still in the upper
bulb — it dominates the composition. Next to it a mug of coffee gone cold, a thin
skin on its surface catching the amber light. Empty dark desk along the bottom
edge. No text, no digits, no readable characters on the cards. Inner glow only.
1920x1080.

Сохрани все три файла в папку:
/home/me/code/articles/articles/pictures/poisk-po-baze-znaniy-s-ii/

В конце выведи список созданных файлов с их размерами в пикселях.
```

---

## Стилевой замок (общий для всего цикла)

Обязателен для обложки целиком, для внутренних кадров — только палитра, свет и фон.

- **Фон:** почти чёрный с синим отливом, `#0b1018`–`#0d1420`, еле заметная тёмная сетка.
- **Ровно два акцента:** бирюзово-голубой `#29a8d0`–`#4cc4e8` и янтарно-оранжевый `#f5a623`–`#ff6a2a`. Третий цвет не вводить.
- **Смысл цвета в этом цикле:** голубой — то, что система читает и на что можно опереться; янтарный — то, что лежит рядом, но остаётся немым или дорого обходится.
- **Свет:** объекты светятся изнутри и роняют цветной отсвет на поверхность. Внешнего источника нет.
- **Исполнение:** чистый 3D-рендер или светящийся контур. Не фотореализм, не рисунок от руки, не плоские иконки.
- **Композиция обложки:** один-два объекта, много пустоты.
- **Внутренние кадры обязаны различаться по композиции и крупности.**

Предметный ряд цикла — архив, картотека, папки, измерительные инструменты. Эта статья добавляет адресную книгу, весы и песочные часы; в первой статье их не было, поэтому лента раздела не повторяется.

Проверка предметности: адресная книга и веер вырезок · чаши весов с двумя папками · песочные часы над разложенными карточками. Три разных существительных, все три кадра — предметные сцены.

---

## Обложка `01-hero` — 16:9, 1920×1080

### Вариант A ★★★★★ — предметная сцена

```
Cinematic 3D render, 16:9, a dark office room at night, near-black #0b1018 with a
blue undertone. A wooden desk seen from slightly above. Two things lie on it side
by side. On the left, an open address book with cut alphabetical thumb tabs down
its edge; one page is turned to a tab and glows clean cyan #4cc4e8, its light
falling on the desk. On the right, a cardboard folder lies open and a fan of
loose paper clippings has spilled out of it across the desk, each clipping marked
with a small coloured sticky flag; the whole spill glows warm amber #f5a623, more
diffuse, no single bright point. A mug and a pen sit at the top edge of the desk.
The room behind is empty darkness. No text anywhere, no digits, no readable
characters on the pages, clippings or tabs. Objects lit only from within, no
lamp, no external light source, no beams. Shallow depth of field, 1920x1080.
```

Почему сильный: два способа найти нужное лежат рядом как две настоящие вещи — точный указатель и разобранная по темам кипа. Сцена собирается из реальных предметов, читается без подписи и не повторяет картотеку из первой статьи цикла.

### Вариант B ★★★★☆ — предметная сцена

```
Cinematic 3D render, 16:9, dark office #0d1420. A desk with two mail trays
standing next to each other. The left tray holds a single envelope standing
upright, alone, glowing crisp cyan #4cc4e8. The right tray is heaped with a thick
pile of unopened letters, all glowing dull amber #f5a623 together. A letter
opener lies between the trays. The rest of the room is dark. No text, no digits,
no readable addresses on any envelope. Inner glow only, no external light.
1920x1080.
```

Почему слабее: точнее показывает «одно письмо против всей почты», но хуже передаёт, что во втором случае ищут по смыслу, а не просто разгребают.

### Вариант C ★★★☆☆ — условный кадр

```
Cinematic 3D render, 16:9, near-black #0b1018 with a faint grid. Two routes lead
from the foreground to a single card-index drawer standing in the middle
distance, its front glowing cyan #4cc4e8. The left route is a short straight rail
of bright cyan light going directly to the drawer. The right route is a long
looping amber #f5a623 track that curves far out to the side and returns to the
same drawer, several times longer. Both end at exactly the same point. Wide empty
dark space above. No text, no digits, no labels, no arrows. Inner glow only.
1920x1080.
```

Почему слабее: схема двух путей объясняет механизм, но это уже условный кадр, а обложка цикла держится на предметной сцене. Годится как внутренняя иллюстрация, если понадобится четвёртая.

## Внутренние кадры

### `02-vesy` — в разделе «Гибридный поиск: почему объединение ухудшило результат»

Предметный кадр.

```
Cinematic 3D render, 16:9, dark office #0d1420. A classic two-pan balance scale
stands on a desk, its brass frame glowing faint cyan #29a8d0. On the left pan: a
thick document folder, stuffed with papers, its edges glowing cyan #4cc4e8. On
the right pan: an identical folder of exactly the same thickness, but its covers
have fallen slightly open and it is completely empty inside, glowing amber
#f5a623. The beam is perfectly level — the two folders balance. A mug stands on
the desk beside the scale. Dark empty room to the right. No text, no digits, no
readable characters on any paper. Inner glow only, no external light. 1920x1080.
```

- **alt:** `Весы: на одной чаше набитая папка, на другой такая же по толщине, но пустая`
- **Подпись:** `Формула объединения смотрит на места в выдаче, а не на то, что нашлось. Пустая находка весит столько же`
- Композиция: средний план, горизонтальная ось, симметрия.

### `03-sorok-kartochek` — в разделе «Второй проход: дорогая починка того, что сломали»

Предметный кадр.

```
Cinematic 3D render, 16:9, dark office #0b1018. Top-down view of a desk with about
forty index cards laid out face down in a loose grid, each glowing dim cyan
#29a8d0. A handful of cards near the centre have been turned face up and glow
brighter cyan #4cc4e8. Standing on the same desk beside them, a tall hourglass
with amber #f5a623 sand glowing from within, most of the sand still in the upper
bulb — it dominates the composition. Next to it a mug of coffee gone cold, a thin
skin on its surface catching the amber light. Empty dark desk along the bottom
edge. No text, no digits, no readable characters on the cards. Inner glow only.
1920x1080.
```

- **alt:** `Сорок карточек на столе, несколько перевёрнуты, рядом большие песочные часы`
- **Подпись:** `Второй проход перечитывает четыре десятка найденных записей. Точность растёт, секунды тоже`
- Композиция: взгляд сверху, крупный предмет рядом с мелкими. Отличается от `02` осью и крупностью.

---

## Технические требования

- Соотношение 16:9, минимум 1600 px по ширине, комфортно 1920×1080.
- Формат исходника: PNG или JPG. Конвертацию в WebP и AVIF делает конвейер.
- Имена файлов ровно как в таблице ниже, строчными латинскими буквами.
- Класть в `articles/pictures/poisk-po-baze-znaniy-s-ii/`.

## Что НЕ генерировать

- **Никакого текста и цифр в кадре.** Ни процентов, ни подписей на карточках.
- Третьего цвета. Только голубой и янтарный на почти чёрном.
- Внешнего источника света, бликов, засветов, объёмных лучей.
- Мозгов, нейросетевых графов, роботов, роботизированных рук, значков «это про ИИ».
- Луп, увеличительных стёкол и значка поиска: буквальная иллюстрация слова «поиск» — самый затёртый кадр в этой теме.
- Диаграмм, графиков, шкал, полос и стрелок: цифры в статье идут таблицами, они читаются поиском, а картинка — нет.
- Людей в кадре.
- Фотореализма, акварели, рисунка от руки, плоских иконок.

---

## Итоговая таблица

| Файл | Куда вставляется | alt | Подпись |
|---|---|---|---|
| `01-hero` | после вводных абзацев, до первого H2 | Поиск по базе знаний с ИИ: на столе адресная книга с алфавитными вырубками и рассыпанные вырезки с закладками | Два способа найти нужное. Один работает по названию, другой по теме |
| `02-vesy` | в разделе «Гибридный поиск: почему объединение ухудшило результат», после абзаца «Первое место слабой ветки весит ровно столько же» | Весы: на одной чаше набитая папка, на другой такая же по толщине, но пустая | Формула объединения смотрит на места в выдаче, а не на то, что нашлось. Пустая находка весит столько же |
| `03-sorok-kartochek` | в разделе «Второй проход: дорогая починка того, что сломали», после таблицы сравнения с лучшей одиночной веткой | Сорок карточек на столе, несколько перевёрнуты, рядом большие песочные часы | Второй проход перечитывает четыре десятка найденных записей. Точность растёт, секунды тоже |
