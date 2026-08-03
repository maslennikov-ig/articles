# Иллюстрации: «Qwen 3.8 Max: стоит ли брать новинку Alibaba в проект»

Статья: `articles/site/qwen-3-8-max-v-proekte.md`
Площадка: aidevteam.ru, раздел «Статьи»

Генерировать нужно **только обложку (01)**. Всё остальное уже лежит в папке:
02 и 03 — скриншоты от автора, 04 и 05 — схемы, собранные из SVG с точными
числами (генеративные модели цифры искажают, поэтому они не генерировались).

---

## 01. Обложка

Формат 16:9, минимум 1920×1080.

### Стилистика сайта — обязательна

Снята с уже опубликованных обложек (`pochemu-ne-rabotaet-vnedrenie-ii`,
`zamenit-li-ii-razrabotchikov`), а не придумана:

- фон почти чёрный сине-навигационный, примерно `#0a1526`, иногда с еле
  заметной технической сеткой;
- ровно две акцентных краски и всегда в паре: холодная циан-голубая около
  `#4cc3f5` и тёплая янтарная около `#f7a51c`;
- объекты **светятся сами** и кладут цветной отблеск на поверхность под собой.
  Не студийный свет сбоку, не «cinematic side lighting»;
- один объект-метафора в кадре, много пустого тёмного пространства, обычно
  справа или слева — туда ложится заголовок;
- допустимы обе манеры: светящаяся линейная «чертёжная» графика и плотный 3D-
  рендер. Общими остаются палитра и свечение;
- ни единой надписи, цифры или логотипа.

### Вариант A — весы, чертёжная манера ★★★★★

> A glowing wireframe illustration on a near-black deep navy background #0a1526
> with a faint technical grid. A large old-fashioned balance scale drawn in
> luminous cyan #4cc3f5 line work. On the left pan sits a massive dark block,
> heavy and oversized, rendered in cold dim blue. On the right pan sits one
> small solid cube glowing warm amber #f7a51c, casting an amber pool of light on
> the pan beneath it. The beam is perfectly level despite the size difference.
> Wide composition, large empty dark space on the right, self-illuminated
> objects, no external light source, no text, no numbers, no logos, 16:9.

Почему сильный: прямо отыгрывает главный тезис статьи — размер и цена не равны
результату. Манера повторяет обложку про лодку, палитра — обе.

### Вариант B — две колонны, 3D-рендер ★★★★☆

> A dark editorial 3D render on a near-black deep navy background #0a1526. Two
> glowing pillars stand side by side on a reflective dark floor. The left pillar
> is enormous, cold blue #4cc3f5, self-illuminated, casting a wide blue pool of
> light. The right pillar is five times smaller, warm amber #f7a51c, glowing
> with the same intensity so that both light pools on the floor are equal in
> size and brightness. Symmetrical wide composition, deep shadows, no text, no
> numbers, no logos, 16:9.

Почему ниже: близко к обложке `zamenit-li-ii-razrabotchikov` с двумя башнями —
рядом в ленте будут перекликаться. Брать, если вариант A не выйдет.

### Вариант C — монолит с активной долей ★★★☆☆

> A single massive dark monolith made of thousands of tiny cells floating in a
> near-black deep navy void #0a1526 with a faint grid. Almost all cells are
> unlit cold blue; a small cluster of cells near one edge glows warm amber
> #f7a51c and lights up the surrounding surface. Three-quarter view, volumetric
> haze, self-illuminated, minimalist, large empty space on the left, no text, no
> numbers, no logos, 16:9.

Почему ниже всех: повторяет схему 04 внутри статьи, и на одной странице они
будут читаться как одна мысль дважды.

**Что НЕ генерировать:** роботов, мозг в лампочке, рукопожатие человека и
робота, китайский флаг, логотипы Alibaba и Anthropic, любые надписи и цифры на
картинке. Кириллицу генеративные модели пишут с ошибками — весь текст выносим в
подпись под изображением.

---

## Готовые файлы

### 02-arena-medicina-top10.png
Скриншот Arena, Text Arena, категория «Медицина и здравоохранение», данные на
1 августа 2026. Вставляется в раздел «Кто в топе, если смотреть не общий
рейтинг, а свою отрасль», сразу после таблицы.

- alt: `Рейтинг Arena в категории «Медицина и здравоохранение»: qwen 3.8 max на первом месте, Claude Fable 5 на седьмом`
- подпись: `Медицинская категория Arena на 1 августа 2026. Справа — цена за миллион токенов: первое место стоит $2/$6, седьмое — $10/$50`

### 03-nash-liderbord.png
Скриншот собственного батл-теста на 3 августа 2026. Вставляется в раздел
«Сколько стоит Qwen 3.8 Max», после абзаца про DeepSeek V4 Flash.

- alt: `Лидерборд собственного теста моделей: DeepSeek V4 Flash на первом месте по соотношению цены и качества`
- подпись: `Наш батл-тест на 3 августа 2026. Первое место по деньгам — DeepSeek V4 Flash за $0,13 за миллион токенов`

### 04-aktivnye-parametry.png
Схема: сто квадратов, четыре подсвечены. Вставляется в раздел «Почему
2,4 триллиона параметров — не та цифра», после первого абзаца.

- alt: `Схема активных параметров qwen 3.8 max: из 2,4 триллиона на токен работают 95 миллиардов`
- подпись: `На каждый токен модель включает около четырёх процентов себя. Платите и ждёте вы как за 95 миллиардов, а не за 2,4 триллиона`

### Пятый пункт снят: последовательность шагов ушла в markdown-таблицу

Схема «как модель попадает в проект» была сделана картинкой, но по правилу
скилла последовательность шагов в статьях для сайта оформляется таблицей: она
рендерится всегда, читается поиском и попадает в ответы ИИ-поисковиков, чего
картинка не умеет. Таблица стоит в разделе «Как мы решаем, ставить ли новую
модель в проект». Файл-схема удалён.

---

## Итоговая таблица

| Файл | Куда | alt | Подпись |
|---|---|---|---|
| `01-hero` | обложка статьи | `Тёмный монолит из тысяч ячеек, светится только небольшая их часть` | — |
| `02-arena-medicina-top10` | после таблицы Arena | см. выше | см. выше |
| `03-nash-liderbord` | после абзаца про DeepSeek | см. выше | см. выше |
| `04-aktivnye-parametry` | после 1-го абзаца про параметры | см. выше | см. выше |

## Технические требования

- Обложка: 16:9, не меньше 1920×1080, PNG или JPG.
- Схемы 04–05 уже 1600×900 PNG, конвейер ужмёт до 1600 и сделает WebP + AVIF.
- Имена файлов менять нельзя: по ним собирается вставка в текст.
- Никакого текста на генерируемой картинке.
