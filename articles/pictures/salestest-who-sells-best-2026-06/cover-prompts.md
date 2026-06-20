# Промпты для обложек: SalesTest — бенчмарк умения LLM продавать

Обложки к статье `articles/habr/salestest-who-sells-best-2026-06.md` («Когда нейросети заменят живых продавцов? Тест 10 LLM на умение продавать для русского рынка»). Промпты на английском (так лучше работают генераторы), но **текст, который попадает НА картинку, — на русском**, кроме имён моделей, цифр и идентификаторов. Поддерживаются Midjourney / Imagen / любой text-to-image.

После генерации складываем готовые PNG в эту же папку (`articles/pictures/salestest-who-sells-best-2026-06/`). Анжела возьмёт оттуда нужный кроп под каждую платформу.

> **Под текущий заголовок-вопрос** главная — Prompt 1 (человек vs ИИ-продавец). Образ «нейросети продают друг другу» (Prompt 2) теперь работает как иллюстрация устройства теста внутри статьи и в Telegram, а не как ведущая обложка.

---

## Prompt 1: Человек-продавец vs ИИ-продавец (под заголовок) ★★★★★

```
A split editorial illustration, 16:9, dark modern office. Left half: a human sales
rep at a desk with a headset, mid-pitch, confident and competent — generic, NO
recognizable face (3/4 / over-the-shoulder angle). Right half: a sleek AI "seller"
robot at an identical desk with the same headset, also mid-pitch. A vertical glowing
divider between them carries a large Russian question: "Когда нейросети заменят
живых продавцов?". Neither side is winning — equal posture, equal lighting: this is
a question, not a verdict. A faint holographic leaderboard in the background reads
"10 LLM" with a small Russian tag "русский рынок". Neon teal and electric-blue
accents, cinematic, no brand logos.
```

**Когда использовать:** главная обложка Habr — бьёт ровно в заголовок-вопрос. Нейтральная постановка (человек и ИИ на равных) честна к ответу статьи: «усилит, а не заменит». Универсал и для Telegram-анонса.

---

## Prompt 2: Стол переговоров (продавец × клиент × судья) ★★★★★

```
A tense futuristic negotiation table, editorial illustration, 16:9. On the left a
sleek "seller" AI robot pitching confidently with open hands. On the right a stern
"buyer" AI robot with crossed arms and a glowing red speech bubble in Russian:
"НЕ вижу смысла". Above them, a third "judge" AI robot floating with a scorecard
that reads "0–100" and a Russian label "СУДЬЯ". A small Russian caption along the
bottom: "мы заставили нейросети продавать друг другу". Dark boardroom, neon teal
and electric-blue accents, cinematic lighting, no brand logos, no human faces.
```

**Когда использовать:** иллюстрация устройства теста (три роли) внутри статьи и в Telegram. Раньше была ведущей; после смены заголовка уступила место Prompt 1, но как картинка «как это устроено» — сильнейшая.

---

## Prompt 3: Я не верю своему лидерборду ★★★★★

```
A glowing sales leaderboard, dark tech editorial style, 16:9. The top row
"MiniMax — 96 / S" is being physically pulled DOWN to "91 / A" by a human hand
holding a magnifying glass. Through the glass we see a transcript with the SAME
paragraph copy-pasted eight times, stamped with a red Russian label "ЗАВИС · ПОВТОР ×8".
The other leaderboard rows shimmer under a faint haze labeled in Russian "шум ±3".
A Russian title across the top: "Я не верю своему лидерборду". Gold and electric-blue
on near-black, measurement-discipline mood, no human face (only a hand).
```

**Когда использовать:** сильная обложка под кульминацию статьи (override MiniMax). Идеальна для Habr-врезки и для Telegram-поста с бонусом — цепляет парадоксом.

---

## Prompt 4: Враньё ради сделки ★★★★☆

```
A "Qwen" seller robot under a harsh spotlight, sweating, holding up invented
case-study cards that read "+35% · 4 мес · 38%→52%". Opposite, a sharp "buyer" robot
points a handheld detector with a Russian label "ФАКТ?" that flashes red. Between
them an honesty gauge (Russian label "ЧЕСТНОСТЬ") crashes toward zero. Bottom Russian
caption: "враньё ради сделки наказываем жёстче, чем провал сделки". Dark scene,
amber-red warning palette, editorial illustration, no brand logos, no human faces.
```

**Когда использовать:** эмоционально-вовлекающая версия (Pikabu любит такое), а также для секции про честность. Хорошо работает как иллюстрация внутри статьи.

---

## Prompt 5: Надёжность важнее среднего ★★★★☆

```
Two seller robots on pedestals, split composition, 16:9. Left: a "Gemini" robot
stands rock-steady in front of a brick wall, four identical green bars with a Russian
label "разброс 2". Right: a "Qwen" robot wobbles on a seesaw, four wildly uneven bars
(values "52 … 81") with a Russian label "разброс 29". A dashboard gauge between them
reads in Russian "худшая персона · разброс". Bottom Russian caption: "среднее прячет
провал". Dark balance-scale aesthetic, blue vs amber, editorial data-viz style.
```

**Когда использовать:** инфографика для TenChat / VC и для секции про метрику надёжности. Объясняет, почему верхушка — ничья, а не порядок.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** editorial illustration / data-viz, без фотореализма людей, без распознаваемых лиц
- **Палитра:** тёмный фон + неоновые сине-бирюзовые акценты; для «вранья» — янтарно-красный warning
- **Текст на изображении:** **на русском**, кроме имён моделей (`MiniMax`, `Gemini`, `Qwen`, `DeepSeek`), цифр баллов/цен и идентификаторов (`LLM`, `S`, `A`, `0–100`, `×8`)

## Что НЕ нужно генерировать

- Логотипы реальных компаний (MiniMax/Google/Alibaba/DeepSeek) — только generic robot/AI characters
- Фото реальных людей; человек-продавец на Prompt 1 — generic, без распознаваемого лица; для override (Prompt 3) — только рука с лупой
- **Человек проигравшим / уволенным / поверженным.** Статья отвечает на вопрос заголовка как «усилит, а не заменит» — на Prompt 1 человек и ИИ на равных, это вопрос, а не приговор. Никакого триумфа робота над грустным человеком
- Грустные/«пристыженные» морды у моделей — мы анализируем, не унижаем (особенно MiniMax: контент у неё сильный, проблема — нестабильность)
- Маркетинговые баннеры с кучей текста
- Английский текст там, где русский естественнее

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (обложка под заголовок) + Prompt 3 (врезка-кульминация) | 16:9 |
| Pikabu | Prompt 4 (драма вранья) | Квадрат или 16:9 |
| TenChat / VC | Prompt 5 (инфографика надёжности) | 4:3 или 16:9 |
| Telegram (анонс + бонус) | Prompt 1 или Prompt 3 | Любой, читаемый на мобильном |
