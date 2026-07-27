# Промты изображений: «Почему не работает внедрение ИИ: пилот прошёл, эффекта нет»

Статья: `articles/site/pochemu-ne-rabotaet-vnedrenie-ii.md` → публикуется на `aidevteam.ru/blog/pochemu-ne-rabotaet-vnedrenie-ii`.
Аудитория — руководитель, у которого пилот уже прошёл и не дал эффекта. Стиль тот же ряд, что у «ИИ-бота для продаж» и «Заменит ли ИИ разработчиков»: тёмный фон, амбер — человеческая сторона, циан — цифровая, плоская векторная манера.

**Готовые файлы кладём в эту же папку**, строго под именами: `01-hero`, `02-nikto-ne-derzhit`, `03-sito`, `04-spokoynaya-panel`. Расширение `.png` или `.jpg`. Конвейер принимает только имена вида `NN-название` и на остальных падает.

**Текста, цифр и графиков с числами на изображениях нет нигде.** Это третья статья подряд с таким правилом, и оно себя оправдало: генератор искажает цифры, а все числа статьи живут в тексте.

---

## Обложка — 3 варианта

Нужен один файл: `01-hero`.

### Вариант 1: Гребут изо всех сил, лодка на привязи ★★★★★

```
Editorial illustration, 16:9, dark charcoal background with a subtle grid.
A side view of a rowing boat drawn in cool cyan lines, with two generic
faceless figures rowing hard, oars deep in the water, bright churned foam and
spray around the blades — clear sense of effort and speed. But a thick taut
amber rope runs from the stern back to a heavy mooring post on the right,
holding the boat perfectly still. Calm flat water behind the post, no wake at
all. Flat modern vector style, high contrast, no text, no numbers, no logos,
no photorealism.
```

**Почему сильный:** это ровно тезис статьи в одном кадре — усилие есть, движения нет. Читается в превью листинга и без подписи. Спокойная вода за кормой сразу говорит «эффекта не было».

### Вариант 2: Велосипед на станке ★★★★☆

```
Conceptual editorial illustration, 16:9, dark navy background. A bicycle seen
from the side, mounted on a stationary training stand, drawn in cool cyan
lines. The rear wheel spins fast with soft motion blur arcs and a faint glow.
The bicycle itself does not move: the stand is solid and grounded. Ahead of it,
in dim amber, a road stretches away into the dark and stays out of reach.
Minimal flat vector style, generous negative space, no text, no numbers,
no logos.
```

**Почему хорош:** та же мысль через понятный бытовой образ. Держим как запас, если лодка выйдет перегруженной деталями.

### Вариант 3: Стрелка, которая вернулась в начало ★★★☆☆

```
Minimalist editorial illustration, 16:9, dark background. A single thick cyan
arrow starts at the left, sweeps confidently up and to the right, then curves
back down and returns exactly to its own starting point, forming a closed loop.
A small amber marker sits at that starting point, untouched and unmoved.
Nothing else in frame. Flat vector, high contrast, no text, no labels,
no numbers, no logos.
```

**Почему слабее:** абстрактно, без подписи не читается. Годится скорее внутрь статьи, чем на обложку.

---

## Иллюстрация 2 — штурвал, который никто не держит

- **Файл:** `02-nikto-ne-derzhit`
- **Место:** раздел «Где теряется ответственность за результат», после абзаца про дырку в постановке
- **Уровень:** концептуальная иллюстрация
- **alt:** `Штурвал, который никто не держит, — главная причина, почему не работает внедрение ИИ`
- **Подпись:** `Все на местах, обязательства выполнены, за результат не отвечает никто`

```
Conceptual editorial illustration, 16:9, dark charcoal background. In the
center, a ship's wheel drawn in cool cyan lines, glowing softly, turning
slightly on its own — nobody's hands are on it. Around it, at a comfortable
distance, three generic human silhouettes in warm amber: one faces away with
arms folded, one looks down at a flat rectangular object in their hands, one
walks out of frame. None of them looks at the wheel. Flat modern vector style,
high contrast, no faces, no text, no numbers, no logos.
```

**Проверка при приёмке:** руки ни одной фигуры не касаются штурвала, и никто на него не смотрит. Если генератор поставил человека за штурвал — берём другой прогон, смысл переворачивается.

---

## Иллюстрация 3 — сетка ловит мелкое, крупное проходит

- **Файл:** `03-sito`
- **Место:** раздел «Что автоматика ловит, а что нет», после абзаца про кашу с нулём ошибок
- **Уровень:** концептуальная иллюстрация
- **alt:** `Сетка задерживает мелкие обломки, а крупный блок проходит сквозь прореху`
- **Подпись:** `Контроль качества ловит «сломалось». «Работает, но не то» проходит насквозь`

```
Conceptual editorial illustration, 16:9, dark background. A taut fine mesh
screen stretched vertically across the frame, drawn in cool cyan lines. Many
small angular fragments are caught in the mesh and pile up on its left side,
lit cyan. In the middle of the screen there is a wide clean gap, and a single
large solid amber cube passes straight through it, continuing to the right,
completely untouched. Motion lines behind the cube. Flat modern vector style,
high contrast, no text, no numbers, no logos.
```

**Проверка при приёмке:** мелкие обломки задержаны слева, крупный блок уже прошёл сквозь прореху и летит вправо. Если сетка задержала и его — картинка противоречит разделу.

---

## Иллюстрация 4 — спокойная панель

- **Файл:** `04-spokoynaya-panel`
- **Место:** раздел «Чем надёжнее система, тем тише контролёр», после абзаца про иронию автоматизации
- **Уровень:** концептуальная иллюстрация
- **alt:** `Человек откинулся в кресле перед ровной панелью приборов, где ни один сигнал не горит`
- **Подпись:** `Чем спокойнее панель, тем тише внутренний контролёр`

```
Conceptual editorial illustration, 16:9, dark charcoal background with a subtle
grid. A control desk seen from behind and slightly to the side. A generic human
silhouette in warm amber leans far back in an operator chair, hands resting in
their lap, head tilted back, clearly relaxed and disengaged. In front of them a
long instrument panel drawn in cool cyan: a row of identical calm indicator
lights and perfectly flat, even readout bars, all steady, nothing alarming.
Soft glow from the panel onto the figure. Flat modern vector style, high
contrast, no text on the panel, no numbers, no digits on any readout, no logos.
```

**Проверка при приёмке:** на панели ни одной цифры и ни одной надписи, все индикаторы одинаково спокойные, поза человека расслабленная. Если генератор нарисовал тревожный красный сигнал — смысл ломается: панель должна выглядеть безупречно.

---

## Технические требования

- **Размер:** минимум 1920×1080, соотношение 16:9. Конвейер ужмёт до 1600px по длинной стороне.
- **Формат:** PNG или JPG.
- **Палитра:** тёмный фон, амбер — человеческая сторона, циан — система и автоматика.
- **Никакого текста, цифр и логотипов.**
- Один ряд с картинками двух предыдущих статей: те же цвета, та же плоская векторная манера, тот же тёмный фон с сеткой.

## Что НЕ нужно генерировать

- Логотипы вендоров, названия моделей, узнаваемые интерфейсы и дашборды.
- Роботов с лицами и эмоциями.
- Графики с процентами и любые цифры: все числа статьи живут в тексте, расхождение — причина не публиковать.
- Людей с узнаваемыми лицами.
- Красные аварийные сигналы на панели в иллюстрации 4: там всё должно выглядеть спокойно.
- Фиолетовые градиенты на белом фоне.

## Итоговая таблица

| Файл | Место вставки | alt | Подпись |
|---|---|---|---|
| `01-hero` | обложка статьи (`featuredImage`) | Лодка, в которой гребут изо всех сил, привязана канатом к причалу и стоит на месте | — |
| `02-nikto-ne-derzhit` | «Где теряется ответственность за результат» | Штурвал, который никто не держит, — главная причина, почему не работает внедрение ИИ | Все на местах, обязательства выполнены, за результат не отвечает никто |
| `03-sito` | «Что автоматика ловит, а что нет» | Сетка задерживает мелкие обломки, а крупный блок проходит сквозь прореху | Контроль качества ловит «сломалось». «Работает, но не то» проходит насквозь |
| `04-spokoynaya-panel` | «Чем надёжнее система, тем тише контролёр» | Человек откинулся в кресле перед ровной панелью приборов, где ни один сигнал не горит | Чем спокойнее панель, тем тише внутренний контролёр |
