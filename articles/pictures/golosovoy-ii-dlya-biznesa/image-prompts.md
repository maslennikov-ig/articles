# Промты изображений: «Голосовой ИИ для бизнеса слушает лучше, чем говорит»

Статья: `articles/site/golosovoy-ii-dlya-biznesa.md` → публикуется на `aidevteam.ru/blog/golosovoy-ii-dlya-biznesa`.
Аудитория — коммерческий B2B-заказчик, не разработчики. Стиль сдержанный, редакционный, без «космоса», без роботов с глазами и без наушников-гарнитур из стоков.

**Готовые файлы кладём в эту же папку** (`articles/pictures/golosovoy-ii-dlya-biznesa/`), строго под именами из итоговой таблицы. Конвейер `pnpm articles:images` принимает только имена вида `NN-название.png|jpg|webp` и на остальных падает.

**Текста на изображениях нет нигде.** Генераторы врут в кириллице и в цифрах, а все числа статьи живут в таблицах. Смысл несёт подпись под картинкой — она уже написана ниже.

**Занятые метафоры — не повторять.** Переговорный стол с цифровым двойником (`ai-bot-dlya-prodazh`), гребцы, привязанные к кнехту (`pochemu-ne-rabotaet-vnedrenie-ii`), ценники (`kak-vybrat-llm-dlya-proekta`), сито, качели-сейсмограмма.

---

## Обложка — 3 варианта

Нужен один файл: `01-hero`. Выбираем лучший из трёх.

### Вариант 1: Короткий вход, длинный выход ★★★★★

```
Editorial illustration, 16:9, near-black blue-charcoal background with a faint
technical grid. On the far left, a small crisp microphone drawn in thin glowing
cyan lines; a short bright cyan sound wave enters it cleanly. From its base a
single warm amber cable leaves and travels across the entire frame in long slow
coils, passing through three simple inline segments shaped like small boxes,
and finally reaches a loudspeaker on the far right that is only just beginning
to glow. The asymmetry between the short cyan entry and the very long amber
path is the subject. Flat modern vector style, glowing contour drawing, deep
empty space in the middle, no text anywhere, no logos, no photorealism.
```

**Почему сильный:** одна идея статьи целиком, без единой надписи — вход мгновенный, выход долгий. Читается и в маленьком превью листинга: контраст короткого и длинного виден на любом размере.

### Вариант 2: Два секундомера ★★★★☆

```
Minimalist editorial illustration, 16:9, near-black blue-charcoal background
with a faint grid. Two stopwatches side by side, drawn as thin glowing contour
line art. The left one is small and cyan, its hand barely moved off zero. The
right one is much larger, warm amber, and its hand has swept almost a full turn,
leaving a soft glowing trail. Between them a generous empty gap. No numerals or
tick labels on either dial — only the hands and the trail. Flat modern vector
style, high contrast, no text anywhere, no logos.
```

**Почему хорош:** прямо о задержке и о разрыве между демо и продакшеном. Минус — циферблаты просят цифр, а цифры генератор испортит; поэтому в промте они запрещены явно.

### Вариант 3: Ухо и рот ★★★☆☆

```
Conceptual editorial illustration, 16:9, near-black blue-charcoal background.
Two abstract geometric forms face each other: on the left a wide open cyan
funnel drawn in thin glowing lines, catching a dense stream of small cyan
particles that flow into it freely. On the right, a narrow amber funnel of the
same size, through which the particles pass one at a time in a slow single
file, backing up into a queue behind it. Generous empty space between them.
Flat modern vector style, glowing contour, no faces, no anatomy, no text
anywhere, no logos.
```

**Почему слабее:** метафора верная, но абстрактнее двух первых, и «воронка» уже примелькалась в инфографике про продажи.

---

## Картинки внутри статьи

### `02-odna-shesteryonka` — после раздела «Задержку создаёт не ваш код»

```
Editorial illustration, 16:9, near-black blue-charcoal background with a faint
grid. A horizontal drivetrain of gears drawn as thin glowing contour line art.
Five small cyan gears sit close together on the left, all identical and crisp.
In the middle of the chain sits one enormous warm amber gear, many times their
diameter, rotating slowly with a soft motion blur on its teeth. To the right of
it, one more small cyan gear waits. The whole chain is clearly limited by the
single huge gear. Flat modern vector style, generous empty space above and
below, no text anywhere, no numbers, no logos.
```

- **alt:** `Одна огромная шестерня в цепочке маленьких — обращения модели к инструментам занимают 82% времени ответа голосового бота`
- **подпись:** `Восемьдесят два процента ожидания создаёт одно звено — обращения модели к вашим системам. Всё остальное вместе весит вшестеро меньше.`

### `04-dve-knopki` — после раздела «Замолчать и остановиться — разные команды»

```
Editorial illustration, 16:9, near-black blue-charcoal background with a faint
grid. Two clearly different physical buttons on a dark panel in the foreground,
well separated. The left button is small, round, cyan, with a soft glow — it is
pressed down. The right button is larger, rectangular, warm amber, with a
protective guard flipped over it — it is untouched. Behind the panel, dimmer and
out of focus, a simple machine assembly continues to turn, showing that work is
still running while the left button is pressed. Flat modern vector style,
glowing contour drawing, no text, no icons, no labels, no logos.
```

- **alt:** `Две разные кнопки на панели голосового бота: нажата только кнопка остановки речи, работа продолжается`
- **подпись:** `Прерывание речи и остановка работы — две разные команды. Если их свести в одну, клиент будет отменять расчёт, просто перебив бота.`

### `03-skolko-raz-vyhodit` — после раздела «Когда это возражение не работает»

```
Editorial illustration, 16:9, near-black blue-charcoal background with a faint
grid. Split composition. On the left, a small cyan glowing sphere sits inside a
simple closed room outline and stays there; a short cyan arrow loops back into
it. On the right, the same sphere but warm amber, connected by three long
looping amber paths that leave the room and reach three separate tall cabinet
shapes standing far apart, and return. The left side is compact and calm, the
right side is stretched across the frame. Flat modern vector style, thin glowing
contour lines, no text anywhere, no numbers, no logos.
```

- **alt:** `Голосовой ИИ для бизнеса: бот без обращений к внешним системам отвечает быстро, бот с тремя обращениями — медленно`
- **подпись:** `Ноль обращений к учётным системам за разговор — realtime работает уже сегодня. Три и больше — упрётесь в ту же задержку, что и мы.`

---

## Итоговая таблица

| Файл | Место вставки | alt | Подпись |
|---|---|---|---|
| `01-hero` | обложка, в тело не вставляется | `Короткий голубой звуковой сигнал входит в микрофон, а длинный янтарный кабель тянется через весь кадр к динамику` | — |
| `02-odna-shesteryonka` | после «Задержку создаёт не ваш код» | см. выше | см. выше |
| `04-dve-knopki` | после «Замолчать и остановиться — разные команды» | см. выше | см. выше |
| `03-skolko-raz-vyhodit` | после «Когда это возражение не работает» | см. выше | см. выше |

Главный запрос «голосовой ИИ для бизнеса» стоит в `alt` у `03-skolko-raz-vyhodit` — это выполняет пункт SEO-чеклиста про запрос в alt. В остальных alt его дублировать не надо: повтор одной фразы в каждом alt читается как спам.

---

## Технические требования

- Соотношение 16:9, от 1600 пикселей по ширине. Конвейер ресайзит всё до 1600, поэтому 1600 — реальный минимум, а 1920×1080 — комфортный запас. Картинку меньше 1600 конвейер растянет.
- Формат исходника: PNG или JPG. WebP и AVIF конвейер сделает сам.
- Фон почти чёрный с синим отливом, `#0b1018`–`#0d1420`. Светлых фонов нет.
- Ровно два акцента: голубой `#29a8d0`–`#4cc4e8` и янтарный `#f5a623`–`#ff6a2a`. Третий цвет не вводить.
- Цвет несёт смысл: голубой — быстрое, ровное, предсказуемое; янтарный — медленное, дорогое, рискованное. Во всех четырёх кадрах распределение именно такое, менять местами нельзя.
- Свет изнутри объекта, с мягким отсветом на плоскости. Внешнего источника нет.

## Что НЕ нужно генерировать

- Роботов с лицами, гарнитуры колл-центра, наушники с микрофоном, говорящие головы.
- Звуковые волны как декоративный фон по всему кадру — волна должна быть объектом, а не текстурой.
- Любые надписи, цифры, шкалы, циферблатные метки и подписи к элементам.
- Фотореализм, 3D-рендер офиса, стоковые люди у компьютера.
- Третий акцентный цвет, особенно зелёный и фиолетовый.
- Изометрию с печатной платой, неоновые сети из точек, золотой как акцент — это стиль эпохи статей про оркестратор, он устарел.
