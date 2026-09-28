# Промты иллюстраций: «GPT-6 Luna и Sol: проверили новинки OpenAI на своих задачах»

Слаг: `gpt-6-luna-i-sol` · площадка: сайт `aidevteam.ru` · 28.09.2026

**Смысл цветов:** бирюзовый — предыдущая версия, ровная и предсказуемая; янтарно-оранжевый — новинка, которая выглядит свежее, но на наших задачах ведёт себя хуже.

**Чего не повторяем:** весы и две шкалы уже есть в `stoit-li-obnovlyat-model-ii`, чат-бабл и остывающая кружка — в соседних статьях цикла.

---

## Сводный промт (скопировать целиком)

```
Generate 2 separate images for a website article, one file per frame. Not a collage, not a grid, not variants of one frame in a single file.

SHARED STYLE (every frame): near-black background #0b1018 with a faint blue cast; exactly two accent colours — calm cyan #29a8d0 (the older, steady version) and amber-orange #f5a623 (the newer, less reliable one); objects glow from within and cast coloured light on the surface below; clean 3D render, not photorealism, not flat icons; 16:9, at least 1920x1080.

SHARED BANS: no text, no letters, no digits anywhere in frame; no third colour; no external light source, no lens flares, no beams; no people; no brains, neural graphs, robots or other "this is about AI" badges.

FRAMES:

1. 01-hero.png — article cover.
Cinematic 3D render, 16:9, near-black background #0b1018 with faint blue tint. A dark wooden office desk in a dim room seen at eye level. On the desk stand two identical round desk lamps shaped like small moons. The left lamp is slightly older, with a worn matte base, and glows a steady, even cyan #29a8d0, lighting a clean circle on the desk. The right lamp is brand new, glossy, still with a sliver of protective film on its base, and glows amber-orange #f5a623, but its light is uneven and flickers, leaving a patchy, broken pool on the desk. Plenty of dark empty space around the desk. No text, no digits, no logos, no people. Studio product-render quality, shallow depth of field.

2. 02-oshibka-v-10-raz.png — for the section "Арифметика подвела обеих".
Cinematic 3D render, 16:9, near-black background #0d1420. Top-down view of a dark desk with a paper invoice-style folder lying open. On the left page stands a single short stack of coins glowing cyan #29a8d0. On the right page stands a stack of identical coins exactly ten times taller, glowing amber-orange #f5a623, towering and slightly leaning as if it might topple. Both stacks use the same coin size so the ratio is obvious. The pages are blank — no writing, no numbers. Soft coloured light pools under each stack. No text, no digits, no people.

SAVE TO: /home/me/code/articles/articles/pictures/gpt-6-luna-i-sol/
RETURN: list of created files with pixel sizes.
```

---

## Обложка (01-hero)

### Вариант A — две лампы-луны ★★★★★ (в сводном промте)

Название моделей — Luna, и обложка обыгрывает это без текста. Старая лампа светит ровно, новая — глянцевая, с плёнкой, но мерцает. Мысль «новее не значит лучше» считывается без подписи.

- **alt:** «GPT-6 Luna и GPT-5.6 Luna: две настольные лампы-луны, старая светит ровно, новая мерцает»
- (обложке подпись не нужна)

### Вариант B — новая коробка на складе ★★★☆☆

```
Cinematic 3D render, 16:9, near-black background #0b1018. A warehouse shelf with two identical shipping boxes. The older box, slightly scuffed, glows steady cyan #29a8d0 from inside through its seams. The newer box is crisp and glossy, glowing amber-orange #f5a623, but the glow leaks unevenly through a half-open flap. No text, no labels, no digits, no people.
```

Слабее: коробки уже встречались в ленте, и метафора «упаковка» не связана с Luna.

---

## Внутренний кадр 02-oshibka-v-10-raz

- **Раздел:** после таблицы в «Арифметика подвела обеих».
- **Проверка пользы:** показывает соотношение предметами (тип 2) — одна стопка против стопки в десять раз выше. Читатель видит масштаб ошибки быстрее, чем из таблицы с рублями.
- **alt:** «Ошибка GPT-6 Luna в расчёте в 10 раз: одна низкая стопка монет и стопка в десять раз выше»
- **подпись:** «Так выглядит ошибка в 10 раз: 16 170 ₽ вместо 161 700 ₽ в месяц. Её сделали обе Luna — в разных прогонах.»

---

## Сводная таблица

| Файл | Куда | alt | Подпись |
|---|---|---|---|
| 01-hero.png | обложка (`featuredImage`) | GPT-6 Luna и GPT-5.6 Luna: две настольные лампы-луны, старая светит ровно, новая мерцает | — |
| 02-oshibka-v-10-raz.png | после таблицы в «Арифметика подвела обеих» | Ошибка GPT-6 Luna в расчёте в 10 раз: одна низкая стопка монет и стопка в десять раз выше | Так выглядит ошибка в 10 раз: 16 170 ₽ вместо 161 700 ₽ в месяц. Её сделали обе Luna — в разных прогонах. |

## Технические требования

- 16:9, не меньше 1920×1080 (пайплайн режет до 1600).
- Никаких цифр и надписей в кадре: цифры живут в подписи.
