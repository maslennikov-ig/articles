# Промпты для обложек: «Тихая болезнь эпохи ИИ» (контроль / ответственность / эффективность)

Обложки для статьи `articles/habr/ai-talk-vs-work-mode.md` (Хабр) и её будущих адаптаций (VC.ru, TenChat, Telegram-анонс). Промпты совместимы с Whisk / Midjourney / Imagen / любым другим генератором.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/ai-talk-vs-work-mode/`). Анжела возьмёт отсюда нужную для каждой платформы.

---

## Prompt 1: Два режима одного человека ★★★★★

```
Editorial illustration, 16:9, dark navy background with subtle grid. The same
generic person (no recognizable face) shown twice as a split scene divided by a
thin vertical line. Left half labeled "ПОБОЛТАТЬ": the person leans forward,
curious and alive, surrounded by many small orange question-mark speech bubbles.
Right half labeled "ПОРАБОТАТЬ": the same person leans back, relaxed and passive,
handing a glowing lever to a calm cyan robot, the question marks fading to gray.
Flat modern vector style, high contrast, warm orange accents on the left, cyan on
the right, dark background, no photorealism, no recognizable faces, no logos.
```

**Когда использовать:** Универсал — главный инсайт статьи в одном кадре. Лучший вариант для Habr (превью в ленте) и Telegram-анонса.

---

## Prompt 2: Тихая передача штурвала ★★★★☆

```
Conceptual editorial illustration, 16:9, dark charcoal background. A ship's helm
(wheel) in the center. A human figure seen from behind (no face), relaxed, is
quietly letting go of the wheel and turning away; a smooth confident cyan robot
hand takes the wheel. Three small glowing tags drift from the human toward the
robot, each with a Russian word: "КОНТРОЛЬ", "ОТВЕТСТВЕННОСТЬ", "ЭФФЕКТИВНОСТЬ".
A faint caption floats above: "кажется быстрее". Warm orange light on the human
side, cool cyan on the robot side, flat vector style, no logos, no purple-on-white.
```

**Когда использовать:** TenChat и VC.ru — метафора потери контроля без кода, читается деловой аудиторией. Хорош и как первая иллюстрация внутри статьи.

---

## Prompt 3: Всё зелёное — а построено не то ★★★★☆

```
Minimalist data-viz style cover, 16:9, dark background. On the left, a vertical
checklist of green checkmarks with short Russian labels: "Тесты — ок",
"Кросс-проверка моделей — ок", "Багов — 0". All glowing green, reassuring. On the
right, connected by an arrow, a small crooked/wrong building or tangled structure
in red-orange, clearly built wrong, with a Russian caption underneath: "но не то".
Bold Russian title across the top: "Ноль багов — и провал". Clean flat icons,
crisp readable typography, cyan and green on the left, warning orange-red on the
right, no gradients overload, no logos.
```

**Когда использовать:** Habr — аудитория любит конкретику и сразу считывает нерв статьи (харнес ловит баги, но не ловит провал суждения). Сильная вторая иллюстрация рядом с зачином.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон + тёплый оранжевый (человек / любопытство) и циан (модель / гладкость) как контрастная пара; красно-оранжевый — только для «тревожного» акцента в Prompt 3
- **Текст на изображении:** **на русском**, кроме нейтральных тех-идентификаторов (имена моделей и т.п. — здесь не требуются)

## Что НЕ нужно генерировать

- Логотипы Anthropic / OpenAI / любых вендоров — только generic роботы и абстракции
- Реальные интерфейсы продуктов (Claude Code, ChatGPT, Cursor)
- Грустные/злые лица у роботов — мы разбираем поведение, а не ругаем модели
- Фиолетовые градиенты на белом фоне
- Английский текст там, где естественен русский

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (или Prompt 3 внутри) | 16:9 (превью в ленте) |
| VC.ru | Prompt 2 | 16:9 |
| TenChat | Prompt 2 | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 | Любой, главное — читается на мобильном |
