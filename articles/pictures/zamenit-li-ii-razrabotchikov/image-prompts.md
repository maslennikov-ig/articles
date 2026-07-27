# Промты изображений: «Заменит ли ИИ разработчиков: что меняется для заказчика»

Статья: `articles/site/zamenit-li-ii-razrabotchikov.md` → публикуется на `aidevteam.ru/blog/zamenit-li-ii-razrabotchikov`.
Аудитория — руководитель, который согласует смету. Стиль тот же, что у «ИИ-бота для продаж»: тёмный фон, амбер как человеческая сторона, циан как цифровая. Раздел должен выглядеть как один раздел, а не как набор случайных картинок.

**Готовые файлы кладём в эту же папку**, строго под именами: `01-hero`, `02-fasad`, `03-svyazka`, `04-pustoy-stul`. Расширение `.png` или `.jpg`. Конвейер принимает только имена вида `NN-название` и на остальных падает.

**Текста, цифр и графиков с числами на изображениях нет нигде.** Все числа статьи живут в таблице и в тексте. Это снимает главный риск: генератор искажает цифры, и картинка начинает противоречить тексту.

---

## Обложка — 3 варианта

Нужен один файл: `01-hero`.

### Вариант 1: Одна конструкция, два состояния ★★★★★

```
Editorial illustration, 16:9, dark charcoal background with a subtle grid.
Two structures of the same shape stand side by side, seen from the side.
On the left: a thin glowing amber wireframe arch, elegant and light, almost
weightless, no supports underneath. On the right: the same arch built for
real in cool cyan — thicker deck, visible piers going down to the ground,
cross-bracing. Equal visual weight, generous empty space between them.
Flat modern vector style, high contrast, no text, no numbers, no people,
no logos, no photorealism.
```

**Почему сильный:** показывает главный тезис статьи одним кадром — одна и та же задача, разный расчёт на вес. Работает в превью листинга и понятен без подписи.

### Вариант 2: Два срока жизни ★★★★☆

```
Conceptual editorial illustration, 16:9, dark navy background. A single tall
tower of stacked blocks in the center-left, glowing warm amber, slightly
leaning, with a few blocks missing near the base. To the right, the same
tower rebuilt in cool cyan: fully filled, straight, standing on a wide flat
base. Soft floor glow under both. Minimal flat vector style, generous
negative space, no text, no numbers, no logos.
```

**Почему хорош:** та же мысль через башню, чуть буквальнее. Держим как запас, если арка выйдет невнятной.

### Вариант 3: Разделение труда ★★★☆☆

```
Minimalist editorial illustration, 16:9, dark background. Two overlapping
translucent circles in the center. The left circle glows warm amber and is
noticeably larger. The right circle is built from thin cyan wireframe lines
and is noticeably smaller. Their overlap is brighter than both. Nothing else
in frame. Flat vector, high contrast, no text, no labels, no percentages,
no numbers, no logos.
```

**Почему слабее:** абстрактно, без подписи не читается. Годится скорее внутрь статьи, чем на обложку.

---

## Иллюстрация 2 — фасад без строения

- **Файл:** `02-fasad`
- **Место:** раздел «Где заканчивается прототип и начинается продукт», после абзаца про то, что всплывает при масштабировании
- **Уровень:** концептуальная иллюстрация
- **alt:** `Нарядный фасад дома, у которого с обратной стороны ничего не построено`
- **Подпись:** `Прототип впечатляет с той стороны, с которой на него смотрят`

```
Conceptual editorial illustration, 16:9, dark charcoal background. A building
facade seen at a three-quarter angle: the front face is complete, elegant and
lit with warm amber light, with windows and a doorway. Behind it there is
nothing — just thin scaffolding props holding the flat facade upright and
empty dark space where the building should be. A long shadow stretches
forward. Flat modern vector style, high contrast, no text, no signage, no
numbers, no people, no logos.
```

**Проверка при приёмке:** передняя стена целая и освещённая, за ней пустота и подпорки. Если генератор построил полноценный дом — берём другой прогон, смысл теряется.

---

## Иллюстрация 3 — связка эксперта и инженера

- **Файл:** `03-svyazka`
- **Место:** раздел «Рабочая связка: ваш эксперт плюс инженер», после абзаца про то, что нужду в инженере видно в самих цифрах
- **Уровень:** концептуальная иллюстрация
- **alt:** `Эксперт и инженер собирают одну конструкцию с разных сторон — ответ на вопрос, заменит ли ИИ разработчиков`
- **Подпись:** `Эксперт отвечает за то, что строим, инженер — за то, выдержит ли это нагрузку`

```
Conceptual editorial illustration, 16:9, dark background. Two generic human
silhouettes, no faces, work on opposite sides of the same arch structure in
the center. The left figure, lit warm amber, points at the top of the arch,
shaping its outline. The right figure, drawn in thin cyan lines, kneels at
the base and installs a support pier. The arch itself is half amber outline
on the left, half solid cyan structure on the right. Flat modern vector
style, high contrast, no text, no tools with brand marks, no numbers,
no logos.
```

**Проверка при приёмке:** две фигуры, одна конструкция, левая половина — контур, правая — с опорой. Фигуры не должны выглядеть спорящими: они работают вместе.

---

## Иллюстрация 4 — пустой стул

- **Файл:** `04-pustoy-stul`
- **Место:** раздел «Обратная крайность: „вы программисты, вам виднее“», после абзаца про самые тяжёлые проекты
- **Уровень:** концептуальная иллюстрация
- **alt:** `Переговорный стол, за которым одно место занято, а второе пустует`
- **Подпись:** `Проект без участия эксперта заказчика идёт медленнее и дороже, чем самый сложный технически`

```
Conceptual editorial illustration, 16:9, dark charcoal background with a
subtle grid. A negotiation table seen from the side, same style as a previous
illustration in this series. On the right side a generic figure drawn in thin
cyan lines sits at the table, leaning forward, working. On the left side the
chair is empty and pushed slightly back, outlined in dim amber, with no one
in it. A single sheet of paper lies on the table in front of the empty chair,
untouched. Flat modern vector style, high contrast, no text on the paper,
no numbers, no logos.
```

**Проверка при приёмке:** одно место занято, второе пусто, лист перед пустым стулом чистый. Пустой стул должен читаться как отсутствие человека, а не как «его ещё не позвали».

---

## Технические требования

- **Размер:** минимум 1920×1080, соотношение 16:9. Конвейер ужмёт до 1600px по длинной стороне.
- **Формат:** PNG или JPG.
- **Палитра:** тёмный фон, амбер — человеческая сторона и «то, что видно», циан — инженерная сторона и «то, что держит».
- **Никакого текста, цифр и логотипов.**
- Стилистически держим один ряд с картинками статьи «ИИ-бот для продаж»: те же цвета, та же плоская векторная манера, тот же тёмный фон с сеткой.

## Что НЕ нужно генерировать

- Логотипы вендоров, названия моделей, узнаваемые интерфейсы.
- Роботов с лицами и эмоциями.
- Диаграммы с процентами: все проценты статьи живут в таблице, и расхождение с картинкой — причина не публиковать.
- Людей с узнаваемыми лицами.
- Фиолетовые градиенты на белом фоне.

## Итоговая таблица

| Файл | Место вставки | alt | Подпись |
|---|---|---|---|
| `01-hero` | обложка статьи (`featuredImage`) | Лёгкий каркасный мостик и рядом тот же мост, построенный с опорами под нагрузку | — |
| `02-fasad` | «Где заканчивается прототип и начинается продукт» | Нарядный фасад дома, у которого с обратной стороны ничего не построено | Прототип впечатляет с той стороны, с которой на него смотрят |
| `03-svyazka` | «Рабочая связка: ваш эксперт плюс инженер» | Эксперт и инженер собирают одну конструкцию с разных сторон — ответ на вопрос, заменит ли ИИ разработчиков | Эксперт отвечает за то, что строим, инженер — за то, выдержит ли это нагрузку |
| `04-pustoy-stul` | «Обратная крайность: „вы программисты, вам виднее“» | Переговорный стол, за которым одно место занято, а второе пустует | Проект без участия эксперта заказчика идёт медленнее и дороже, чем самый сложный технически |
