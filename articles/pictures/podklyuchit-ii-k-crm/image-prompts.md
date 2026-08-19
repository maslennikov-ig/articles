# Промты иллюстраций — «Как подключить ИИ к CRM: что спросить и что проверить»

Статья: `articles/site/podklyuchit-ii-k-crm.md`
Площадка: сайт `aidevteam.ru`, раздел «Статьи»
Дата: 19.08.2026


> **Статус на 19.08.2026: картинки по этому набору уже сгенерированы** — по
> прежней, более условной версии промтов (архив ящиков в глубине, штемпель,
> отчёт с пустым ящиком, рулетка в проёме). `alt` и подписи в статье
> соответствуют именно им, переделывать ничего не нужно.
>
> Предметные варианты ниже — на случай, если набор будет переснят. Тогда
> `alt` и подписи в статье надо вернуть к формулировкам из итоговой таблицы
> этого файла.

---

## Сводный промт (скопировать целиком)

> Набор уже снят по прежней версии промтов. Этот блок — для пересъёмки: он
> собран из предметных вариантов. Если запустите его, `alt` и подписи в статье
> нужно вернуть к формулировкам из итоговой таблицы этого файла.

```
Сгенерируй 4 отдельных изображения для статьи. Каждое изображение — отдельный
файл. Не коллаж, не сетка, не несколько вариантов в одном файле.

Общий стиль для всех четырёх кадров:
- почти чёрный фон с синим отливом, #0b1018–#0d1420, еле заметная тёмная сетка;
- ровно два акцентных цвета: бирюзово-голубой #29a8d0–#4cc4e8 и
  янтарно-оранжевый #f5a623–#ff6a2a; голубой = то, что система читает и на что
  можно опереться, янтарный = то, что лежит в базе и остаётся немым;
  третий цвет не вводить;
- предметы светятся изнутри и роняют цветной отсвет на поверхность;
- кинематографический 3D-рендер, малая глубина резкости;
- соотношение 16:9, минимум 1600 px по ширине, целевой размер 1920x1080.

Запрещено во всех кадрах: любой текст, цифры, читаемые надписи на карточках,
папках и бумагах; третий цвет; внешний источник света, лампы, блики, засветы,
объёмные лучи; люди; мозги, нейросетевые графы, роботы и прочие значки «это про
ИИ»; диаграммы, графики, шкалы, полосы и стрелки; фотореализм, акварель,
рисунок от руки, плоские иконки.

Кадр 1. Файл 01-hero.png — обложка статьи.
Cinematic 3D render, 16:9, a dark office room at night, near-black #0b1018 with a
blue undertone. In the foreground a plain wooden desk. On the desk sits a heavy
card-index drawer that has been pulled right out of its cabinet and set down,
packed full of paper cards standing upright. A metal index tab divides the cards:
the cards in front of the tab glow warm cyan #4cc4e8 from within, lighting the
desk surface, the rim of a ceramic mug and a ballpoint pen lying beside them. All
the cards behind the tab stay dull amber #f5a623 and unlit. Behind the desk, a
wall of closed filing cabinets recedes into darkness, their handles barely
catching the cyan spill. No text anywhere, no digits, no readable labels on the
cards or the cabinets. Objects lit only from within, no lamp, no external light
source, no beams, no lens flare. Shallow depth of field, 1920x1080.

Кадр 2. Файл 02-odin-shtamp.png — иллюстрация к разделу про переписанные даты.
Cinematic 3D render, 16:9, dark office #0d1420. Close side view of a desk. On it
a leaning stack of about twenty document folders seen edge-on, their spines
glowing soft cyan #29a8d0. Across every single spine, at exactly the same height,
the same rectangular ink stamp mark glows amber #ff6a2a — identical position and
shape on all twenty, so the marks line up into one continuous amber band running
through the whole stack. A heavy wooden-handled rubber stamp lies beside the
stack on an open ink pad, its rubber face wet and glowing amber. Dark empty room
to the right. No text, no digits, no readable characters inside the stamp mark.
Inner glow only, no external light. 1920x1080.

Кадр 3. Файл 03-pustoy-yashchik.png — иллюстрация к разделу про пустое поле.
Cinematic 3D render, 16:9, dark office #0b1018. A desk photographed from above at
a slight tilt. On the desktop lies a single printed report sheet glowing cyan
#4cc4e8 from within, with one very large blank rounded panel occupying its upper
half where a headline figure would be — the panel is empty, no characters of any
kind. A few paper clips and a pen sit next to the sheet. The desk's own drawer
below is pulled fully open and is completely empty: bare amber-lit #f5a623 rails
inside, not a single folder, the amber light spilling upward onto the underside
of the desktop. Empty dark floor at the left edge. No text, no numbers anywhere.
Inner glow only. 1920x1080.

Кадр 4. Файл 04-merka.png — иллюстрация к разделу про замер вместо чистки.
Cinematic 3D render, 16:9, dark interior #0d1420. Wide frontal shot of a doorway
in a bare wall, the door frame glowing faint cyan #29a8d0. A retractable steel
measuring tape is stretched taut horizontally across the opening at chest height,
the blade glowing bright cyan #4cc4e8; the tape's case rests on the floor to one
side, casting an amber #f5a623 pool of light. On the near side of the doorway,
waiting to be carried through: two stacked cardboard boxes and the corner of a
desk, lit only by the amber spill. Behind the doorway, deep darkness. No text, no
digits, no scale markings on the blade. Inner glow only, no external light.
1920x1080.

Сохрани все четыре файла в папку:
/home/me/code/articles/articles/pictures/podklyuchit-ii-k-crm/

В конце выведи список созданных файлов с их размерами в пикселях.
```

---

## Стилевой замок (снят с `pochemu-ne-rabotaet-vnedrenie-ii/01-hero.webp`, `kak-vybrat-llm-dlya-proekta`, `zamenit-li-ii-razrabotchikov`)

Обязательно для обложки целиком, для внутренних — только палитра, свет и фон.

- **Фон:** почти чёрный с синим отливом, `#0b1018`–`#0d1420`, еле заметная тёмная сетка.
- **Ровно два акцента:** бирюзово-голубой `#29a8d0`–`#4cc4e8` и янтарно-оранжевый `#f5a623`–`#ff6a2a`. Третий цвет не вводить.
- **Смысл цвета в этой статье:** голубой — то, что система читает и на что можно опереться; янтарный — то, что лежит в базе, но остаётся немым.
- **Свет:** объекты светятся изнутри и роняют цветной отсвет на поверхность. Внешнего источника нет.
- **Исполнение:** чистый 3D-рендер или светящийся контур. Не фотореализм, не рисунок от руки, не плоские иконки.
- **Композиция обложки:** один-два объекта, много пустоты, сопоставление слева-справа или вглубь.
- **Внутренние кадры обязаны различаться по композиции и крупности.** Три кадра по одной схеме — брак набора.

Проверка предметности: ящик картотеки на столе · стопка папок со штемпелем · отчёт и пустой ящик стола · рулетка в дверном проёме. Четыре разных существительных. Все четыре кадра — предметные сцены, которые можно было бы снять на телефон в тёмной комнате.

**Смена смысла обложки.** Прошлая версия статьи открывалась метафорой «6 % содержания» — лоток с бумажками. Статья переписана: теперь она открывается списком вопросов, которые собственник задаёт на планёрке и может задать базе напрямую. Обложка показывает то, что стало доступно: архив, который наконец можно прочитать целиком.

---

## Обложка `01-hero` — 16:9, 1920×1080

### Вариант A ★★★★★ — предметная сцена

```
Cinematic 3D render, 16:9, a dark office room at night, near-black #0b1018 with a
blue undertone. In the foreground a plain wooden desk. On the desk sits a heavy
card-index drawer that has been pulled right out of its cabinet and set down,
packed full of paper cards standing upright. A metal index tab divides the cards:
the cards in front of the tab glow warm cyan #4cc4e8 from within, lighting the
desk surface, the rim of a ceramic mug and a ballpoint pen lying beside them. All
the cards behind the tab stay dull amber #f5a623 and unlit. Behind the desk, a
wall of closed filing cabinets recedes into darkness, their handles barely
catching the cyan spill. No text anywhere, no digits, no readable labels on the
cards or the cabinets. Objects lit only from within, no lamp, no external light
source, no beams, no lens flare. Shallow depth of field, studio product-render
quality, 1920x1080.
```

Почему сильный: сцену можно собрать из настоящих вещей и снять на телефон — стол, ящик картотеки, кружка, ручка. Читается без подписи: архив стоял закрытым, а один срез наконец вынули и прочитали. Кружка и ручка делают кадр обжитым, а не выставочным.

### Вариант B ★★★★☆ — предметная сцена

```
Cinematic 3D render, 16:9, dark office interior #0d1420. A desk seen from a low
angle. On it, a tall stack of closed paper folders, dusty and dull amber #f5a623.
One folder has been taken from the middle of the stack and lies open on the desk
in front, its two pages glowing cyan #4cc4e8, the light spilling across the desk
and up onto the underside of the stack above. A pair of reading glasses rests on
the open folder. The room behind the desk is empty darkness. No text, no digits,
no readable characters on any page. Inner glow only, no lamp, no external light.
1920x1080.
```

Почему слабее: тот же смысл, но стопка папок — образ ближе к «разбираем бумаги», чем к «спрашиваем архив словами».

### Вариант C ★★★☆☆ — условный кадр

```
Cinematic 3D render, 16:9, near-black background #0b1018 with a faint dark grid.
A vast archive of card-index drawers fills the frame in deep perspective,
receding into blackness — dozens of rows and columns, metal fronts edged in dull
amber #f5a623. One single horizontal row at eye level glows bright cyan #4cc4e8
from within, its light spilling onto the drawers above and below and onto the
floor. Everything else unlit. Wide empty dark space at the top. No text, no
digits, no labels. Inner glow only, no external light. 1920x1080.
```

Почему слабее: масштаб красивый, но это уже не комната, а условное пространство — на обложке цикла лучше стоит живая сцена. Держим как запасной вариант, если A и B выйдут тесными.

## Внутренние кадры

### `02-odin-shtamp` — в подразделе «Почему половина вопросов упирается в данные»

Предметный кадр.

```
Cinematic 3D render, 16:9, dark office #0d1420. Close side view of a desk. On it
a leaning stack of about twenty document folders seen edge-on, their spines
glowing soft cyan #29a8d0. Across every single spine, at exactly the same height,
the same rectangular ink stamp mark glows amber #ff6a2a — identical position and
shape on all twenty, so the marks line up into one continuous amber band running
through the whole stack. A heavy wooden-handled rubber stamp lies beside the
stack on an open ink pad, its rubber face wet and glowing amber. Dark empty room
to the right. No text, no digits, no readable characters inside the stamp mark.
Inner glow only, no external light. 1920x1080.
```

- **alt:** `Стопка папок, на каждой один и тот же оттиск даты`
- **Подпись:** `Одна массовая выгрузка переписывает дату изменения у всех записей сразу. В интерфейсе это выглядит нормально`
- Композиция: средний план сбоку, горизонтальный ритм.

### `03-pustoy-yashchik` — в том же подразделе, ниже

Предметный кадр.

```
Cinematic 3D render, 16:9, dark office #0b1018. A desk photographed from above at
a slight tilt. On the desktop lies a single printed report sheet glowing cyan
#4cc4e8 from within, with one very large blank rounded panel occupying its upper
half where a headline figure would be — the panel is empty, no characters of any
kind. A few paper clips and a pen sit next to the sheet. The desk's own drawer
below is pulled fully open and is completely empty: bare amber-lit #f5a623 rails
inside, not a single folder, the amber light spilling upward onto the underside
of the desktop. Bright confident sheet above, hollow drawer below. Empty dark
floor at the left edge. No text, no numbers anywhere. Inner glow only.
1920x1080.
```

- **alt:** `Отчёт с пустым местом под крупную цифру и выдвинутый пустой ящик стола под ним`
- **Подпись:** `83 % покрытия. Ящик, из которого эта цифра якобы посчитана, пуст`
- Композиция: два уровня по вертикали, взгляд сверху под углом. Отличается от `02` крупностью и осью.

### `04-merka` — в разделе «„Значит, сначала год чистить данные?“ Нет»

Предметный кадр.

> Файл переименован из `04-fonarik`: фонарик и ящик повторяли бы кадр `03`.

```
Cinematic 3D render, 16:9, dark interior #0d1420. Wide frontal shot of a doorway
in a bare wall, the door frame glowing faint cyan #29a8d0. A retractable steel
measuring tape is stretched taut horizontally across the opening at chest height,
the blade glowing bright cyan #4cc4e8; the tape's case rests on the floor to one
side, casting an amber #f5a623 pool of light. On the near side of the doorway,
waiting to be carried through: two stacked cardboard boxes and the corner of a
desk, lit only by the amber spill. Behind the doorway, deep darkness. No text, no
digits, no scale markings on the blade. Inner glow only, no external light.
1920x1080.
```

- **alt:** `Мерная лента поперёк дверного проёма и коробки, которые ещё не занесли`
- **Подпись:** `Восемь проверок занимают часы. Мы дошли до них через полтора месяца`
- Композиция: фронтальный широкий план, вертикальная симметрия проёма. Отличается от `02` и `03` и осью, и планом.

---

## Технические требования

- Соотношение 16:9, минимум 1600 px по ширине, комфортно 1920×1080. Конвейер ресайзит до 1600, картинку меньше растянет.
- Формат исходника: PNG или JPG. Конвертацию в WebP и AVIF делает конвейер.
- Имена файлов ровно как в таблице ниже, строчными латинскими буквами.
- Класть в `articles/pictures/podklyuchit-ii-k-crm/`.

## Что НЕ генерировать

- **Никакого текста и цифр в кадре.** Ни «83 %», ни «6 %», ни дат, ни подписей на папках. Модели пишут кириллицей с ошибками, а неверная цифра на картинке бьёт по доверию ко всей статье сильнее, чем отсутствие картинки.
- Третьего цвета. Только голубой и янтарный на почти чёрном.
- Внешнего источника света, бликов, засветов, объёмных лучей. Луч света от «искусственного интеллекта» на архив — ровно то, что здесь запрещено.
- Устаревшего стиля эпохи статей про оркестратор: изометрия с печатной платой, неоновые сети из точек, роботизированные руки, золотой как третий акцент.
- Мозгов, нейросетевых графов, роботов и прочих значков «это про ИИ». Статья про данные заказчика, а не про технологию.
- Фотореализма, акварели, рисунка от руки, плоских иконок.
- Людей в кадре — предмет говорит сам, фигура отвлечёт.
- Диаграмм, графиков, шкал и полос: данные в этой статье идут таблицами, они читаются поиском, а картинка — нет.

---

## Итоговая таблица

| Файл | Куда вставляется | alt | Подпись |
|---|---|---|---|
| `01-hero` | после вводных абзацев, до первого H2 | Подключить ИИ к CRM: вынутый на стол ящик картотеки, часть карточек в нём светится | Данные копились годами. Посмотреть на них целиком стало можно только сейчас |
| `02-odin-shtamp` | в подразделе «Почему половина вопросов упирается в данные», после абзаца «Дата не помнит ничего старше июня» | Стопка папок, на каждой один и тот же оттиск даты | Одна массовая выгрузка переписывает дату изменения у всех записей сразу. В интерфейсе это выглядит нормально |
| `03-pustoy-yashchik` | в том же подразделе, после абзаца «83 % покрытия, за которыми 0,14 %» | Отчёт с пустым местом под крупную цифру и выдвинутый пустой ящик стола под ним | 83 % покрытия. Ящик, из которого эта цифра якобы посчитана, пуст |
| `04-merka` | в разделе «„Значит, сначала год чистить данные?“ Нет», после абзаца про «починим по ходу» | Мерная лента поперёк дверного проёма и коробки, которые ещё не занесли | Восемь проверок занимают часы. Мы дошли до них через полтора месяца |
