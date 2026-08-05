# Промты иллюстраций: «ИИ-ассистент врёт клиентам, потому что вокруг него пусто»

Статья: `articles/site/ii-assistent-vret-klientam.md` · сайт `aidevteam.ru`
Дата: 05.08.2026

## Общие технические требования

- Соотношение 16:9, минимум 1600 px по ширине (комфортно – 1920×1080).
- Фон почти чёрный с синим отливом: `#0b1018`–`#0d1420`.
- Ровно два акцента: бирюзово-голубой `#29a8d0`–`#4cc4e8` и янтарно-оранжевый
  `#f5a623`–`#ff6a2a`. Третьего цвета нет.
- Смысл цвета: голубой – подтверждённое, проверенное, надёжное; оранжевый –
  выдуманное, неподтверждённое, рискованное.
- Свет идёт изнутри объектов и роняет цветной отсвет на поверхность. Внешнего
  источника нет.
- Один-два объекта, много пустоты, сопоставление слева-справа.
- Чистый 3D-рендер или светящийся контур. Не фотореализм, не рисунок от руки,
  не плоские иконки.
- **Текста на картинке нет.** Смысл выносится в подпись. Кириллицу модели
  пишут с ошибками.

## Чего НЕ генерировать

- Изометрию с печатной платой, неоновые сети из точек, роботизированные руки,
  золотой как третий акцент – это стиль эпохи статей про оркестратор.
- Роботов, мозг с микросхемами, рукопожатие человека и робота.
- Повтор соседних статей: измерительный прибор с натянутым тросом
  (`kontrol-kachestva-raboty-ii`), два одинаковых светящихся куба с разными
  ярлыками (`qwen-3-8-max-v-proekte`), два счёта на бумаге
  (`kak-snizit-rashody-na-llm`), лодка у причала (`pochemu-ne-rabotaet-vnedrenie-ii`).

---

## 01-hero — обложка

Смысл: у товара заполнена только часть карточки, остальное модель дописала
сама. Подтверждённое светится голубым, дописанное – оранжевым.

### Вариант A – ярлык на кресле ★★★★★

> A single office chair standing alone in a vast dark void, background almost
> black with a faint blue tint (#0b1018). A physical paper tag hangs from the
> armrest on a thin thread. The upper half of the tag is filled with crisp
> glowing cyan (#4cc4e8) printed lines; the lower half of the tag is blank
> paper, and from that blank area thin amber (#ff6a2a) lines of handwriting
> are still growing outward into the air, dissolving into faint smoke. The
> chair itself is rendered as a clean matte 3D object, lit only by the two
> glows: cyan light pooling on the floor under the tag, amber light bleeding
> onto the seat. No text is readable — lines only. Deep empty space around the
> object, single centred subject, cinematic 3D render, 16:9, 1920x1080.

### Вариант B – две стопки карточек ★★★★☆

> Two stacks of thin physical cards on a dark reflective floor, background
> almost black with blue tint. The left stack is thick and glows cold cyan
> from within, edges crisp and aligned. The right stack is mostly empty air —
> only two or three cards exist, and above them amber-orange light sketches
> the ghostly outlines of the missing cards that were never there, wireframe
> and semi-transparent. Cyan and amber reflections spill onto the wet-looking
> floor. No text, no icons. Macro depth of field, cinematic 3D render, 16:9.

### Вариант C – по мотивам обсуждений ★★★☆☆

> Идея: в обсуждениях на Hacker News галлюцинацию называют не сбоем, а
> оценочным суждением о результате.
> Что меняем: вместо метафоры «поломки» – идеально работающий механизм,
> выдающий не тот продукт. Наша палитра, другая композиция.
>
> A precise mechanical dispenser rendered in clean matte 3D, softly lit from
> inside with cyan light, working perfectly — gears aligned, no damage. From
> its output slot flows a ribbon of amber-orange glowing material that has no
> matching shape in the machine, curling into the dark empty space. The
> machine is calm and correct; the output is wrong. Almost black background
> with blue tint, cyan pool of light under the machine, amber reflection on
> the floor to the right. No text. Cinematic 3D render, 16:9.

**Файл:** `01-hero`
**Место:** обложка (`featuredImage`)
**alt:** `На ярлыке товара заполнена только верхняя половина, нижнюю дописывает оранжевое свечение`
**Подпись:** не требуется (обложка)

---

## 02-arena-pareto — скриншот публичной арены

**Это не генерация.** Нужен твой скриншот с Pareto-графиком «цена против
Arena Score», где видно mimo-v2.5-pro (1466 при $0.76/M) и deepseek-v4-flash
(1438 при $0.25/M).

Положи файл в `articles/pictures/ii-assistent-vret-klientam/` под именем
`02-arena-pareto.png` – сам я его сохранить не могу, он пришёл вложением в
переписку.

**Место:** после абзаца «Почему вообще эти четыре…» в разделе «Что показал
замер»
**alt:** `Публичный лидерборд: соотношение цены и качества моделей на 5 августа 2026 года`
**Подпись:** `Отбор кандидатов: горизонталь – цена за миллион токенов, вертикаль – балл публичной арены. Снимок от 05.08.2026.`

---

## 03-sudya-lupa — судья ловит конкретность, а не выдумку

Смысл: проверяющий реагирует на резкость формулировки, а не на её ложность.
Чёткая ложь попадается, расплывчатая проходит.

### Вариант A – лупа над двумя пятнами ★★★★★

> A large glass magnifying lens floating in a dark void, background almost
> black with blue tint. Under the lens, on the dark surface, lie two glowing
> amber shapes of identical size: the left one has hard crisp edges and is
> caught in the lens's cyan-lit focus ring, its outline sharply projected; the
> right one has soft diffuse edges and sits just outside the focus, almost
> invisible, its amber glow bleeding into the darkness unnoticed. The lens rim
> glows cold cyan. Reflections of both shapes on the polished floor. No text,
> no numbers. Cinematic 3D render, shallow depth of field, 16:9, 1920x1080.

### Вариант B – сито ★★★★☆

> A metal sieve suspended horizontally in a dark empty space, glowing cyan
> along its rim, background almost black with a blue tint. Sharp angular amber
> fragments rest on top of the mesh, caught. Below the sieve, a soft amber
> mist has passed straight through the same mesh and drifts down into the
> darkness, uncaught and spreading. Cyan light pools on the mesh, amber light
> stains the floor below. Clean matte 3D materials, deep negative space, no
> text. Cinematic render, 16:9.

**Файл:** `03-sudya-lupa`
**Место:** после абзаца «Судья ловит конкретность…» в разделе «Автоматический
судья тоже врёт»
**alt:** `Под увеличительным стеклом резкое пятно попадается, а размытое проходит мимо фокуса`
**Подпись:** `Конкретная выдумка попадается, расплывчатая проходит. Победитель отчасти выиграл гейт тем, что говорил обтекаемее.`

---

## 04-granica-kod-model — что проверяет код, а что модель

Смысл: граница проходит по проверяемости утверждения. Перечислимое – жёстко
и холодно; неперечислимое – мягко и приблизительно.

### Вариант A – две поверхности ★★★★★

> A dark room split by an invisible vertical boundary, background almost black
> with blue tint. On the left half: a grid of small rectangular slots milled
> into a solid metal plate, each slot holding one glowing cyan block that fits
> exactly, machined tolerances visible, cold and precise. On the right half:
> the same plate dissolves into soft amber vapour where no slots exist, and
> loose amber shapes hover approximately in place, never touching any surface.
> Cyan light reflects hard off the metal; amber light diffuses into fog. No
> text, no labels. Cinematic 3D render, wide composition, 16:9, 1920x1080.

### Вариант B – макро ★★★☆☆

> Extreme macro shot of the edge where a machined metal surface ends and open
> darkness begins. The metal is lit from within by cold cyan light, its edge
> razor-sharp and in focus. Beyond the edge, amber particles float in complete
> darkness, out of focus, belonging to no structure. Background almost black
> with a blue tint. Shallow depth of field, dust visible in the light beam, no
> text. Cinematic 3D macro render, 16:9.

**Файл:** `04-granica-kod-model`
**Место:** после абзаца «Проверяемость утверждения решает здесь больше…»
**alt:** `Слева блоки точно входят в пазы металлической плиты, справа висят в воздухе без опоры`
**Подпись:** `Слева – то, что перечислимо и проверяется кодом. Справа – то, что можно только оценивать.`

---

## 05-shestoy-rezhim — шестого режима не было

Смысл: пять состояний продуманы, шестое – клиент отказался – отсутствует, и
инструмент остаётся доступен.

Схему решил не делать: механика в тексте описана прозой, а Mermaid-диаграмма
для робота пуста – она рисуется на клиенте. Предметная сцена работает лучше.

### Вариант A – щиток с рубильниками ★★★★★

> A dark control panel mounted on a wall in an almost black room with a blue
> tint. Five heavy physical switches sit in a row, each seated in a precisely
> machined slot, glowing calm cyan. To the right of them, a sixth slot is
> empty — just a rectangular hole in the panel with nothing in it, and from
> inside that hole a faint amber glow leaks out, spilling onto the panel
> surface and the floor below. Analogue metal and worn paint texture, no
> labels, no text, no numbers. Single subject, wide empty space around it.
> Cinematic 3D render, 16:9, 1920x1080.

### Вариант B – связка ключей ★★★☆☆

> A key rack in a dark room, background almost black with blue tint. Five keys
> hang on their hooks, each glowing cold cyan. The sixth hook is bare, and
> below it a single amber-glowing key lies on the floor where anyone could
> pick it up. Cyan light pools around the rack, amber light stains the floor.
> Clean matte 3D, deep shadows, no text. Cinematic render, 16:9.

**Файл:** `05-shestoy-rezhim`
**Место:** после абзаца «У нас есть механизм, который мы называем гейтингом…»
**alt:** `Пять рубильников стоят в пазах, шестой паз пустой и оттуда пробивается оранжевый свет`
**Подпись:** `Пять режимов у нас были. Шестого – «клиент отказался» – не было, и инструмент оставался доступен.`

---

## Итоговая таблица

| Файл | Место вставки | alt | Подпись |
|---|---|---|---|
| `01-hero` | обложка | На ярлыке товара заполнена только верхняя половина, нижнюю дописывает оранжевое свечение | – |
| `02-arena-pareto` | раздел «Что показал замер», после абзаца про отбор моделей | Публичный лидерборд: соотношение цены и качества моделей на 5 августа 2026 года | Отбор кандидатов: горизонталь – цена за миллион токенов, вертикаль – балл публичной арены. Снимок от 05.08.2026. |
| `03-sudya-lupa` | раздел «Автоматический судья тоже врёт», после абзаца про конкретность | Под увеличительным стеклом резкое пятно попадается, а размытое проходит мимо фокуса | Конкретная выдумка попадается, расплывчатая проходит. |
| `04-granica-kod-model` | раздел «Что должен проверять код, а что модель» | Слева блоки точно входят в пазы металлической плиты, справа висят в воздухе без опоры | Слева – то, что перечислимо и проверяется кодом. Справа – то, что можно только оценивать. |
| `05-shestoy-rezhim` | раздел «Второй тип вранья», после абзаца про пять режимов | Пять рубильников стоят в пазах, шестой паз пустой и оттуда пробивается оранжевый свет | Пять режимов у нас были. Шестого – «клиент отказался» – не было. |

Разнообразие: обложка и 05 – предметные сцены, 03 – оптика с макро, 04 –
сцена с масштабом и фактурой металла, 02 – реальный скриншот. Двух схем
подряд нет.
