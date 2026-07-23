# Промпты для обложек: двойной бенчмарк 7 моделей — «кто продаёт» vs «кто учит»

Обложки для статьи `articles/habr/llm-dual-benchmark-sell-vs-teach-2026-07.md` (Хабр, дальше адаптации под VC/Telegram). Промты на английском, текст на самих картинках — на русском (кроме имён моделей и чисел). Подходят для Midjourney / Imagen / любого генератора.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/llm-dual-benchmark-sell-vs-teach-2026-07/`). Анжела возьмёт отсюда нужную для каждой платформы.

---

## Prompt 1: Два табло, одни роботы ★★★★★

```
Editorial illustration, 16:9. A split-screen dark futuristic ops room with two glowing leaderboard screens side by side. Left screen titled "КТО ЛУЧШЕ ПРОДАЁТ", right screen titled "КТО ЛУЧШЕ УЧИТ". Seven identical small AI robots are ranked on both boards — but the order is visibly shuffled between the two: glowing crossing arrows connect the same robot to different positions. One robot near the top of the left board (labeled "Kimi K3") drops to a low position on the right board; another robot (labeled "GPT-5.6 Luna") rises from mid-left to #1 on the right. Caption at the bottom: "Одна когорта — два рейтинга". Neon teal and amber accents on deep navy background, clean data-viz aesthetic, no human faces.
```

**Когда использовать:** Универсал — главный insight статьи в одном кадре. Лучший вариант для Habr (превью в ленте) и Telegram-анонса.

---

## Prompt 2: Reasoning съел урок ★★★★★

```
Cinematic dark illustration, 16:9. An AI robot sits at a desk writing a lesson on a long paper scroll, but a giant glowing thought-cloud above its head has swallowed almost all the ink. The thought-cloud is labeled "13 639 токенов на размышления". The visible scroll text is short and cuts off mid-sentence at "…высвобождая 400 часов", with a red stamp "ОБРЫВ". Next to the desk, a nearly empty budget gauge labeled "Бюджет: 16 384 токена". Blue-violet thought-cloud glow against dark background, moody rim lighting, no human faces.
```

**Когда использовать:** Для секции/анонса про reasoning-риск; хорошо заходит технической аудитории Хабра. Альтернативная обложка Habr, основная для поста про Kimi.

---

## Prompt 3: Лошадка за одну десятую цента ★★★★☆

```
Editorial illustration, 16:9. A small plain AI robot stands on the #1 podium between two flashy, oversized, expensive-looking robots. The small robot holds a simple price tag "$0.001" and wears two gold medals labeled "ПРОДАЖИ" and "УРОКИ". The expensive robot beside it holds a price tag "$0.20" with a red downward arrow and looks puzzled. Caption at the bottom: "Дёшево ≠ плохо. Дорого ≠ хорошо". Dark tech background, warm gold accent lighting on the small robot, cool grey on the expensive ones, no human faces.
```

**Когда использовать:** Value-сюжет (Nex-N2-Mini) — эмоционально-вовлекающий вариант для VC.ru и Telegram; квадратный кроп живёт хорошо.

---

## Prompt 4: Фабрикатор у доски ★★★★☆

```
Dark editorial illustration, 16:9. An AI robot confidently lectures at a whiteboard covered in fake citations written in chalk: "Фондация РМП — 34%", "637 поставщиков", "CCC = DIO+DPO−DSO ✗", "Нил Скреб". A large magnifying glass hovering over the board highlights each claim with a red warning glow. Caption: "Выдуманные источники в обучающем уроке". Amber-red warning palette on charcoal background, analytical mood (inspection, not mockery), no human faces.
```

**Когда использовать:** Секция про честность/фабрикации; вариант для Pikabu-адаптации и для отдельного Telegram-поста про Laguna.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон (navy/charcoal) + неоновые teal/amber акценты; золото — только в Prompt 3
- **Текст на изображении:** на русском, кроме имён моделей (Kimi K3, GPT-5.6 Luna) и чисел/цен ($0.001, 13 639)

## Что НЕ нужно генерировать

- Логотипы реальных компаний (xAI, OpenAI, Moonshot) — только generic-роботы
- Грустные/униженные лица у «проигравших» моделей — мы диагностируем, не издеваемся
- Маркетинговые баннеры с кучей текста
- Текст на английском там, где русский естественнее

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (запасной — Prompt 2) | 16:9 (превью в ленте) |
| VC.ru | Prompt 3 | 16:9 |
| Telegram анонс | Prompt 1 или Prompt 3 | Любой, главное — читается на мобильном |
| Pikabu (если пойдёт) | Prompt 4 | Квадрат или 16:9 |
