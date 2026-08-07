# Промты изображений: «Контроль качества работы ИИ: три места, где он ломается»

Статья: `articles/site/kontrol-kachestva-raboty-ii.md` → публикуется на `aidevteam.ru/blog/kontrol-kachestva-raboty-ii`.
Аудитория — коммерческий B2B-заказчик. Стиль сдержанный, редакционный: без роботов, без судейских молотков, без галочек в зелёных кружках.

**Готовые файлы кладём в эту же папку** (`articles/pictures/kontrol-kachestva-raboty-ii/`), строго под именами из итоговой таблицы. Конвейер `pnpm articles:images` принимает только имена вида `NN-название.png|jpg|webp`.

**Текста на изображениях нет нигде.** Ни цифр, ни делений на шкалах, ни подписей: генераторы врут в кириллице и в числах. Смысл несёт подпись под картинкой, она уже написана ниже.

**Занятые метафоры — не повторять.** Микрофон с длинным кабелем, цепочка шестерён, две кнопки на панели, комната со сферой и серверами (`golosovoy-ii-dlya-biznesa`); переговорный стол с цифровым двойником (`ai-bot-dlya-prodazh`); гребцы у кнехта (`pochemu-ne-rabotaet-vnedrenie-ii`); ценники (`kak-vybrat-llm-dlya-proekta`); сито и качели-сейсмограмма.

---

## Обложка — 3 варианта

Нужен один файл: `01-hero`. Выбираем лучший из трёх.

### Вариант 1: Печать поверх трещины ★★★★★

```
Editorial illustration, 16:9, near-black blue-charcoal background with a faint
technical grid. Centre-left, a smooth rectangular metal plate drawn in thin
glowing cyan contour lines. A jagged warm amber crack runs across the plate,
clearly visible and unrepaired. A large circular inspection stamp, drawn in the
same cyan line style with a blank empty centre and no lettering of any kind, is
pressed down over the plate and covers part of the crack while the rest of the
crack still shows beyond its rim. Generous empty space on the right. Flat
modern vector style, glowing contour drawing, no text anywhere, no letters, no
numbers, no logos, no photorealism.
```

**Почему сильный:** ровно тезис статьи в одном кадре — проверка прошла, дефект остался. Читается и в маленьком превью листинга: контраст ровной пластины и рваной трещины виден на любом размере. Пустой центр печати снимает главный риск — генератор не сможет вписать туда кривые буквы.

### Вариант 2: Стрелка, которую придержали ★★★★☆

```
Minimalist editorial illustration, 16:9, near-black blue-charcoal background
with a faint grid. A large measuring gauge drawn as thin glowing cyan contour
line art, its dial completely blank — no numerals, no tick marks, no labels.
The needle points high into the upper range. A thin warm amber wire is tied to
the needle and pulled taut off to the side, holding the needle away from where
it would otherwise rest. The wire leaves the frame. Generous empty space. Flat
modern vector style, high contrast, no text anywhere, no numbers, no logos.
```

**Почему хорош:** прямо про первый излом — оценке подсказали. Минус: пустой циферблат выглядит непривычно, и генератор постоянно пытается дорисовать деления; в промте это запрещено дважды.

### Вариант 3: Три звена, одно треснуло ★★★☆☆

```
Conceptual editorial illustration, 16:9, near-black blue-charcoal background
with a faint grid. Three large chain links in a horizontal row, drawn in thin
glowing contour lines. The outer two links are cyan, closed and intact. The
middle link is warm amber and split by a clean break, its two ends slightly
apart so the chain no longer holds. Generous empty space above and below. Flat
modern vector style, glowing contour, no text anywhere, no numbers, no logos.
```

**Почему слабее:** метафора верная, но безадресная — «где-то рвётся» подошло бы половине статей блога, а сюжет статьи конкретнее.

---

## Картинки внутри статьи

### `02-lupa-mimo` — после раздела «Первый излом: проверяющему можно подсказать»

```
Editorial illustration, 16:9, near-black blue-charcoal background with a faint
grid. A large magnifying glass drawn as thin glowing cyan contour line art,
held at an angle over a flat surface. Inside its circular field the surface is
clean and empty. Just outside the rim, clearly in the open and unmagnified,
sits a jagged warm amber crack in the surface. A thin amber line enters from
the edge of the frame and touches the handle of the magnifier, nudging it away
from the crack. Flat modern vector style, generous empty space, no hands, no
faces, no anatomy, no text anywhere, no numbers, no logos.
```

- **alt:** `Контроль качества работы ИИ: лупа проверяющего отведена в сторону от дефекта`
- **подпись:** `Проверяющий, которому исполнитель может подсказать серьёзность находки, перестаёт быть проверяющим. У людей это лечат подчинением, у агентов — запретом в правилах.`

### `03-pyat-odinakovyh` — после раздела «Второй излом: проверяющих становится много»

```
Editorial illustration, 16:9, near-black blue-charcoal background with a faint
grid. Five identical cyan lenses stand in a row on the left, all aimed at the
same single object on the right: a small metal plate drawn in thin glowing
contour lines. Each lens casts a beam onto the plate, and all five beams land
in exactly the same spot, overlapping into one, so the illuminated area is no
larger than a single beam would make. One lone warm amber lens stands slightly
apart and casts an identical beam onto the very same spot. Flat modern vector
style, thin glowing contour lines, no text anywhere, no numbers, no logos.
```

- **alt:** `Пять одинаковых проверяющих освещают ровно то же место, что и один`
- **подпись:** `Пятеро проверяющих находят ровно то же, что и один, — но время и счёт растут впятеро. Замер автора Superpowers: минус двадцать пять минут на задачу и та же оценка качества.`

### `04-vosem-kopiy` — после раздела «Что сломалось у нас»

```
Editorial illustration, 16:9, near-black blue-charcoal background with a faint
grid. On the left, a stack of eight identical warm amber cards, drawn in thin
glowing contour lines, offset slightly from one another so all eight are
countable — every card carries the same blank rectangular block with no
lettering. On the right, a tall vertical bar drawn in cyan, filled almost to
the very top, with one small unfilled sliver left at the very top. The bar has
no scale marks, no numerals and no labels of any kind. Generous empty space
between the stack and the bar. Flat modern vector style, glowing contour
drawing, no text anywhere, no numbers, no logos.
```

- **alt:** `Восемь одинаковых копий ответа и почти полная шкала оценки — автоматический судья снял за повтор один балл`
- **подпись:** `Бот скопировал финальный ответ восемь раз подряд, а судья снял за это ровно один балл. Оценка была честной по рубрике: строки про повторы в ней просто не было.`

---

## Итоговая таблица

| Файл | Место вставки | alt | Подпись |
|---|---|---|---|
| `01-hero` | обложка, в тело не вставляется | `Стрелку измерительного прибора удерживает натянутый трос, уходящий за кадр` | — |

**Выбран вариант 2** («Стрелка, которую придержали»). Циферблат вышел без делений, как и требовалось, поэтому alt обложки в этой таблице обновлён под фактическую картинку — исходный alt был написан под вариант 1 с печатью.
| `02-lupa-mimo` | после «Первый излом» | см. выше | см. выше |
| `03-pyat-odinakovyh` | после «Второй излом» | см. выше | см. выше |
| `04-vosem-kopiy` | после «Что сломалось у нас» | см. выше | см. выше |

Главный запрос «контроль качества работы ИИ» стоит в `alt` у `02-lupa-mimo` — это закрывает пункт SEO-чеклиста про запрос в alt. В остальных alt его дублировать не надо: одна и та же фраза во всех alt читается как спам.

---

## Технические требования

- Соотношение 16:9, от 1600 пикселей по ширине. Конвейер ресайзит всё до 1600, поэтому 1600 — реальный минимум, а 1920×1080 — комфортный запас.
- Формат исходника: PNG или JPG. WebP и AVIF конвейер сделает сам.
- Фон почти чёрный с синим отливом, `#0b1018`–`#0d1420`. Светлых фонов нет.
- Ровно два акцента: голубой `#29a8d0`–`#4cc4e8` и янтарный `#f5a623`–`#ff6a2a`. Третий цвет не вводить.
- Цвет несёт смысл: голубой — то, что работает штатно и предсказуемо; янтарный — дефект, помеха, лишнее. Во всех четырёх кадрах распределение именно такое, менять местами нельзя.
- Свет изнутри объекта, с мягким отсветом на плоскости. Внешнего источника нет.

## Что НЕ нужно генерировать

- Судейские молотки, весы Фемиды, галочки и крестики, красные штампы «REJECTED».
- Роботов, лица, руки, фигуры людей — во всех четырёх кадрах анатомии нет.
- Любые надписи, цифры, деления шкал, метки на циферблатах и подписи к элементам.
- Фотореализм, 3D-рендер цеха, стоковых инспекторов с планшетами.
- Третий акцентный цвет, особенно зелёный и красный: зелёный сразу читается как «проверка пройдена», а статья ровно об обратном.
- Изометрию с печатной платой, неоновые сети из точек, золотой как акцент — стиль эпохи статей про оркестратор, он устарел.
