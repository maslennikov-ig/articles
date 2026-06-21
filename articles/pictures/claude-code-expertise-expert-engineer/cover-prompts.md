# Промпты для обложек: обзор исследования Anthropic про экспертизу + спор «эксперт vs инженер»

Обложки для статьи `articles/habr/claude-code-expertise-expert-engineer.md` («Разработчики больше не нужны? Новое исследование Anthropic на 400 000 сессий — и мой спор с ним»). Промты — на английском, текст НА картинке — на русском (кроме имён моделей/продуктов и цифр). Поддерживаются Whisk / Midjourney / Imagen / любой генератор по тексту.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/claude-code-expertise-expert-engineer/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Связка «эксперт + инженер» против одиночки ★★★★★

```
Editorial vector illustration, 16:9, clean modern tech-magazine style.
Split composition.

LEFT side (smaller, dimmer): a single abstract human figure standing proudly
on top of a tall, glittering but visibly cracking tower made of glowing
mismatched blocks — it tilts and a few blocks are falling. A small caption
plate below in Russian reads: "Эксперт в одиночку".

RIGHT side (larger, confident): TWO abstract human figures building together a
solid, well-engineered structure — one figure clearly a domain person (holding
a small briefcase / headset icon), the other an engineer (holding a wrench /
schematic icon). Their tower is lower but rock-solid, with visible foundation,
support beams and a green checkmark. Caption plate in Russian: "Эксперт + инженер".

Large headline text at the top, in Russian: "Кто соберёт продукт, который выживет?"
Color palette: deep navy/charcoal background, warm gold accents on the cracking
tower, calm teal/green accents on the solid one. No real logos, no real faces,
abstract geometric characters only. No sad faces.
```

**Когда использовать:** Универсал — главный смысл статьи (спор с Anthropic в одном кадре). Лучшая для Habr-превью и Telegram-анонса.

---

## Prompt 2: Инфографика по цифрам исследования ★★★★★

```
Clean data-visualization cover, 16:9, dark editorial dashboard style.
Title at top in Russian: "400 000 сессий Claude Code — что показали".

Two compact bar-chart blocks side by side.

BLOCK 1 titled in Russian "Подтверждённый успех":
- Bar "Новичок" — short, gray, label "15%"
- Bar "Эксперт" — tall, glowing gold, label "30%"

BLOCK 2 titled in Russian "Профессия почти не важна":
- Bar "Разработчики" — label "30%"
- Bar "Не-разработчики" — label "26%"
- a small bracket between them with Russian note "разница 4 пункта"

A bold side stat in a circle: "2.4×" with Russian caption underneath
"больше действий агента у эксперта".

Color palette: near-black background, gold + teal data accents, thin grid lines,
crisp sans-serif. Identifiers and numbers stay as-is (Claude Code, 400 000, 2.4×,
30%, 26%, 15%). Everything human-readable — in Russian. No logos, no faces.
```

**Когда использовать:** TenChat и Habr — для тех, кто кликает на конкретику и цифры. Хорошо смотрится как второе изображение внутри статьи.

---

## Prompt 3: Метафора «эйфория первой недели» ★★★★☆

```
Conceptual editorial illustration, 16:9, slightly dramatic but not gloomy.
A gorgeous, glowing app/product "castle" built on a small island of SAND,
confetti still floating in the air around it — it looks impressive and brand-new.
But hairline cracks are spreading from the base, one corner is starting to sink,
and a stylized wave/storm cloud approaches from the right with a small Russian
label on it: "нагрузка".

Big headline text, top-left, in Russian: "Эйфория первой недели".
A smaller subtitle plate, bottom: "Работает. Вопрос — на чём и до какого момента".

Color palette: festive warm glow (gold, soft pink confetti) on the castle,
cooler ominous blue-gray on the incoming wave — the contrast between celebration
and the coming load. Abstract, no real logos, no real faces, no sad characters.
```

**Когда использовать:** Pikabu и эмоциональные соцсети — метафора краткосрочного вау-эффекта, который не держит нагрузку. Цепляет тех, кто проходил вайб-кодинг.

---

## Prompt 4: Реалистичная сцена «вместе = результат» ★★★★☆

```
Photorealistic editorial photograph, 16:9, warm modern startup office, soft
natural window light, shallow depth of field — looks like a real candid team
shot, not a posed stock cliché.

THREE collaborators around one desk with a large monitor, all engaged and
leaning in together:
- an ENGINEER (casual hoodie, sticker-covered laptop) — hands on the keyboard
- a DOMAIN EXPERT (smart-casual business look, holding a notebook or wearing a
  sales headset) — pointing at the screen, explaining something
- the AI AGENT represented NOT as a person but as a glowing assistant panel on
  the monitor between them (a clean chat/agent UI with a subtle blue glow)

On the central monitor: a finished, polished working product (a clean dashboard
UI) with a small green badge in Russian reading "готово" — the result they built
together. The mood is collaborative and satisfied: it works because all three
are in it.

Headline text overlaid top-left, in Russian: "Результат — там, где они вместе".

IMPORTANT: people must be GENERIC and anonymous (diverse, ordinary
professionals) — NOT any recognizable real person or celebrity, no real company
logos on screens or clothing. Invented/anonymous faces only.
Color palette: warm, optimistic, trustworthy — amber window light plus a calm
blue glow from the screen. Any numbers/identifiers stay in latin; all
human-readable overlay text — in Russian.
```

**Опциональный вариант (диптих):** слева — одинокий эксперт радуется яркому прототипу, у которого по краю идут трещины; справа — та же тройка (инженер + эксперт + AI) и крепкий работающий продукт. Подпись слева «В одиночку», справа «Вместе».

**Когда использовать:** реалистичная hero-обложка для Habr и Telegram-анонса, когда хочется живых людей вместо схемы. Эмоционально показывает главный тезис статьи (результат — только в связке), а не парадокс или цифры.

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** Prompt 1–3 — векторная / editorial-иллюстрация без фотореализма людей; Prompt 4 — фотореалистичная сцена с обобщёнными, анонимными людьми (без узнаваемых реальных лиц и знаменитостей)
- **Цветовая палитра:** тёмный фон + золотые/бирюзовые акценты (контраст «хрупкое vs надёжное»)
- **Текст на изображении:** **на русском**, кроме имён моделей/продуктов (Claude Code) и цифр (400 000, 2.4×, 30%, 26%, 15%)

## Что НЕ нужно генерировать

- Логотипы реальных компаний (в т.ч. Anthropic) — только абстрактные фигуры/структуры
- Узнаваемые реальные люди и знаменитости, фото конкретных упомянутых персон (обобщённые анонимные люди в Prompt 4 — можно)
- Грустные / сконфуженные «лица» у фигур или людей — мы спорим с выводом, а не высмеиваем
- Маркетинговые баннеры с кучей текста
- Английские подписи там, где русский естественнее

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (превью в ленте) | 16:9 |
| Pikabu | Prompt 3 | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 (универсальный) | Любой, читается на мобильном |

**Prompt 4 (реалистичная сцена с людьми)** — альтернативная hero-обложка для Habr или Telegram, если хочется живых людей вместо схемы. Можно поставить вместо Prompt 1.
