# Промты изображений: «ИИ-бот для продаж: когда он окупается, а когда вредит»

Статья: `articles/site/ai-bot-dlya-prodazh.md` → публикуется на `aidevteam.ru/blog/ai-bot-dlya-prodazh`.
Аудитория — коммерческий B2B-заказчик, не разработчики. Поэтому стиль сдержанный, редакционный, без «космоса» и без роботов-няшек.

**Готовые файлы кладём в эту же папку** (`articles/pictures/ai-bot-dlya-prodazh/`), строго под именами из итоговой таблицы. Конвейер `pnpm articles:images` принимает только имена вида `NN-название.png|jpg|webp` и на остальных падает.

**Текста на изображениях нет нигде.** Это сознательное решение: генераторы врут в кириллице и в цифрах, а все числа статьи живут в таблицах. Смысл несёт подпись под картинкой, она уже написана ниже.

---

## Обложка — 3 варианта

Нужен один файл: `01-hero`. Выбираем лучший из трёх.

### Вариант 1: Две стороны одного стола ★★★★★

```
Editorial illustration, 16:9, dark charcoal background with a subtle grid.
A negotiation table seen from the side. On the left a generic businessperson
silhouette (no face, no recognizable features), leaning back with folded arms,
warm amber rim light. On the right, in the same chair posture, a calm geometric
figure made of thin cyan lines and soft glow — a digital counterpart, clearly
not human, no robot face. Between them on the table: a single closed folder.
Flat modern vector style, high contrast, amber on the human side, cyan on the
digital side, no text anywhere, no logos, no photorealism.
```

**Почему сильный:** сразу читается тема — ИИ по ту сторону переговоров, а не «нейросеть в вакууме». Работает и в превью листинга, и в поиске по картинкам.

### Вариант 2: Диалог, который слушают ★★★★☆

```
Conceptual editorial illustration, 16:9, dark navy background. Two speech
bubbles face each other in the center: the left one solid amber with rounded
organic edges, the right one built from thin cyan wireframe lines. Above them,
slightly larger and dimmer, a third neutral gray bubble looks down on both —
the observer. Thin connecting lines form a triangle. Minimal flat vector style,
generous empty space, no text inside the bubbles, no icons, no logos.
```

**Почему хорош:** метафора «продавец, покупатель, судья» без единой надписи. Чуть абстрактнее первого, зато универсальнее.

### Вариант 3: Ровно и на качелях ★★★☆☆

```
Minimalist editorial illustration, 16:9, dark background. Left third: a solid
straight cyan horizontal line, perfectly level, casting a soft glow. Right two
thirds: the same line but wildly jagged, swinging up and down like a seismograph
trace, in warm amber turning to red at the lowest dip. A single small generic
human silhouette stands at the low dip, looking up. Flat vector, high contrast,
no grid, no text, no numbers, no logos.
```

**Почему слабее:** сильная идея (ровная модель против неровной), но как обложка читается не с первого взгляда. Держим как запас.

---

## Иллюстрация 2 — схема замера

- **Файл:** `02-tri-roli`
- **Место:** после H2 «Что значит «умеет продавать»: шесть вещей, которые мы измеряем», сразу за абзацем про мягкую первую версию замера
- **Уровень:** данные, нужна наглядность (схему в блоге показать нечем: Mermaid в разделе не рендерится, сырой SVG вырезается пайплайном)
- **alt:** `Схема замера: ИИ-бот для продаж ведёт диалог с моделью-покупателем, третья модель оценивает разговор`
- **Подпись:** `Продавец, покупатель и судья. Покупатель и судья одни и те же для всех тестируемых моделей, иначе баллы несравнимы`

```
Clean technical diagram illustration, 16:9, dark charcoal background. Three
distinct nodes arranged in a triangle. Bottom left: a rounded rectangle filled
with soft amber glow. Bottom right: a rounded rectangle built from thin cyan
wireframe lines. Top center, larger and neutral gray: a hexagon with a thin
outline. A thick double-headed arrow connects the two bottom nodes horizontally.
Two thin dashed arrows rise from the middle of that connection up into the
hexagon. Flat vector, crisp edges, generous spacing, no text, no letters, no
numbers, no icons inside the shapes, no logos.
```

**Проверка при приёмке:** три фигуры, двусторонняя стрелка внизу, две тонкие стрелки вверх. Никаких надписей.

---

## Иллюстрация 3 — выдуманный кейс

- **Файл:** `03-vydumannyy-keys`
- **Место:** после абзаца «Меня в этой истории цепляет другое…», перед списком «Что с этим делают на практике»
- **Уровень:** концептуальная иллюстрация
- **alt:** `Цифровой собеседник уверенно показывает документ, которого не существует`
- **Подпись:** `Модель под давлением торга сочиняет кейс с цифрами. Инструкция «не выдумывай» этому не мешает`

```
Conceptual editorial illustration, 16:9, dark charcoal background. A calm
geometric figure made of thin cyan lines — a digital counterpart, no face —
confidently holds out a sheet of paper toward the viewer. The sheet is bright
and clean but completely blank, and its lower half dissolves into thin drifting
particles, as if it never fully existed. A faint amber spotlight from the left
falls on the empty sheet. Flat modern vector style, high contrast, no text on
the paper, no numbers, no charts, no logos, no photorealism.
```

**Проверка при приёмке:** лист пустой и распадается. Если генератор дописал на нём цифры или таблицу — берём другой прогон: числа на картинке противоречат тексту.

---

## Иллюстрация 4 — ровная стена и качели

- **Файл:** `04-stena-i-kacheli`
- **Место:** после абзаца «Я снизил оценку руками…» в разделе «Средний балл врёт: смотрите на разброс»
- **Уровень:** концептуальная иллюстрация (числа остаются в таблице выше)
- **alt:** `Ровная кирпичная стена рядом с раскачивающимися качелями`
- **Подпись:** `Две модели с похожим средним баллом. Одна одинакова на любом клиенте, вторая проваливается на неудобном`

```
Conceptual editorial illustration, 16:9, dark background split into two halves
by generous empty space. Left half: a low, perfectly even wall of identical
cyan blocks, flat top edge, calm and static. Right half: a swing hanging from
two long ropes, caught mid-motion at a steep tilt, in warm amber turning red at
the lowest point, with soft motion blur arcs behind it. Same visual weight on
both halves. Flat modern vector style, dark background, no text, no numbers,
no people, no logos.
```

**Проверка при приёмке:** слева ровный верхний край, справа явный наклон и след движения.

---

## Технические требования

- **Размер:** минимум 1920×1080, соотношение 16:9. Конвейер ужмёт до 1600px по длинной стороне.
- **Формат:** PNG или JPG (WebP тоже примет, но лучше отдать исходник побольше).
- **Имена файлов:** строго `01-hero.png`, `02-tri-roli.png`, `03-vydumannyy-keys.png`, `04-stena-i-kacheli.png`. Любое другое имя конвейер отклонит.
- **Палитра:** тёмный фон, тёплый амбер — человеческая сторона, циан — цифровая, красный только как тревожный акцент.
- **Никакого текста, цифр, графиков с числами и логотипов.**

## Что НЕ нужно генерировать

- Логотипы вендоров и названия моделей.
- Реальные интерфейсы мессенджеров и CRM.
- Роботов с лицами и эмоциями: разговор о поведении модели, а не о милоте.
- Любые числа на изображении. Все цифры статьи живут в markdown-таблицах, и расхождение картинки с таблицей — причина не публиковать.
- Фиолетовые градиенты на белом фоне.

## Итоговая таблица

| Файл | Место вставки | alt | Подпись |
|---|---|---|---|
| `01-hero` | обложка статьи (`featuredImage`) | Менеджер по продажам и его цифровой двойник сидят по разные стороны одного стола переговоров | — |
| `02-tri-roli` | после H2 «Что значит «умеет продавать»…» | Схема замера: ИИ-бот для продаж ведёт диалог с моделью-покупателем, третья модель оценивает разговор | Продавец, покупатель и судья. Покупатель и судья одни и те же для всех тестируемых моделей, иначе баллы несравнимы |
| `03-vydumannyy-keys` | раздел «Самый дорогой риск ИИ-бота для продаж — вранье под торгом» | Цифровой собеседник уверенно показывает документ, которого не существует | Модель под давлением торга сочиняет кейс с цифрами. Инструкция «не выдумывай» этому не мешает |
| `04-stena-i-kacheli` | раздел «Средний балл врёт: смотрите на разброс» | Ровная кирпичная стена рядом с раскачивающимися качелями | Две модели с похожим средним баллом. Одна одинакова на любом клиенте, вторая проваливается на неудобном |
