# Промпты для обложек: «Харнесс вокруг продающего агента решает больше, чем выбор модели»

Обложки к статье `articles/habr/llm-judge-marked-assumption-2026-08.md` (Хабр).
Промты на английском, текст на самой картинке – по-русски. Генераторы: любой
image-to-image или text-to-image с поддержкой 16:9.

Готовые PNG складываем сюда же, в `articles/pictures/llm-judge-marked-assumption-2026-08/`.

Палитра общая с разделом статей на сайте, чтобы обложки цикла читались как один
набор: почти чёрный фон с синим отливом `#0b1018`–`#0d1420`, ровно два акцента –
бирюзово-голубой `#29a8d0`–`#4cc4e8` и янтарно-оранжевый `#f5a623`–`#ff6a2a`.
Голубой – подтверждённое и проверяемое, оранжевый – неподтверждённое.

Внутренние иллюстрации сайтовой версии (кресло с ярлыком, сито, плита с пазами,
щиток с рубильниками) не повторять: это соседний материал того же цикла.

---

## Prompt 1: Model swap changes nothing ★★★★★

Главный тезис заголовка: меняешь модель – класс ошибки остаётся, потому что
дело в обвязке.

```
Four identical dark machined slots milled into a single heavy metal plate,
standing in an almost black room with a faint blue tint (#0b1018). Into each
slot a different glowing cyan core is fitted — four cores, four shapes, all
seated correctly. From every one of the four slots the same amber-orange
(#ff6a2a) vapour leaks upward through the same unsealed gap at the plate's
edge, identical in all four cases. The cores differ; the leak does not.
Cyan light pools on the metal, amber light stains the floor. Clean matte 3D
render, wide composition, deep negative space, no text, no labels, no logos.
16:9, 1920x1080, cinematic lighting.
```

**Когда использовать:** основная обложка Хабра. Читается в ленте на превью:
четыре разных ядра, одна и та же утечка.

---

## Prompt 2: The harness, layer by layer ★★★★☆

Пять слоёв обвязки в порядке внедрения – единственная схематичная версия из трёх.

```
Cross-section view of five concentric protective shells around a single small
glowing cyan core, rendered as clean matte 3D in an almost black room with a
blue tint. The innermost shells are solid machined metal, tight and precise,
lit cyan from within; the outer two shells are progressively more porous —
mesh, then thin scattered mist — glowing faint amber where the material thins
out. A single amber particle has escaped through the outermost layer and
drifts into the dark. Russian labels in small clean sans-serif type beside
the shells, right-aligned: «каталог», «состояния», «контракт», «рубрика»,
«проверка». Nothing else written. 16:9, 1920x1080, cinematic.
```

**Когда использовать:** второй вариант обложки, если хочется, чтобы структура
статьи читалась ещё до открытия. Подписи по-русски – проверить на опечатки
после генерации, кириллицу генераторы ломают.

---

## Prompt 3: Two rulers, one object ★★★★☆

Метрики показывают разное – про рубрику и про инверсию ранга.

```
Two very different measuring instruments aimed at one and the same small
matte object floating in an almost black void with a blue tint. On the left a
precise digital caliper glowing cold cyan, jaws closed exactly on the object.
On the right an old analogue dial gauge glowing warm amber, its needle
resting at a visibly different position, connected to the same object by a
thin probe. The object between them is plain and unremarkable. Both
instruments are lit from inside; cyan and amber reflections meet on the wet
dark floor beneath. No readable numbers on the dials, no text anywhere.
Macro depth of field, cinematic 3D render, 16:9, 1920x1080.
```

**Когда использовать:** для анонса в Telegram и для соцсетей – метафора
читается без контекста статьи.

---

## Технические требования

- Размер: минимум 1600 по ширине (конвейер ресайзит до 1600), комфортно 1920×1080
- Формат: PNG
- Соотношение: 16:9
- Стиль: чистый 3D-рендер или светящийся контур; не фотореализм, не рисунок от
  руки, не плоские иконки
- Текст на изображении: только в Prompt 2, только по-русски, пять коротких слов

## Что НЕ нужно генерировать

- Роботов, гуманоидов, рукопожатие человека и машины
- Логотипы реальных компаний и узнаваемые интерфейсы (в статье названы RAGAS,
  DeepEval, DoorDash – их визуальную айдентику не трогаем)
- Мозг с микросхемами, нейросети из точек, изометрию с печатной платой
- Грустные или растерянные «лица» у моделей – мы разбираем механику, а не
  критикуем продукты
- Английские подписи: аудитория русскоязычная

## Адаптация под площадки

| Площадка | Промт | Кроп |
|---|---|---|
| Хабр | Prompt 1 | 16:9, превью в ленте |
| Telegram-анонс | Prompt 3 | 16:9, читается на мобильном |
| Запас | Prompt 2 | 16:9 |
