---
platform: telegram
channel: https://t.me/maslennikovigor
author: Igor Maslennikov
date: 2026-04-09
purpose: Анонс статьи LLM Battle Test + ссылка на лидерборд (это пост, на который ссылаются https://t.me/maslennikovigor/199 из статей на Habr, Pikabu, TenChat)
article_platform: habr, pikabu, tenchat
article_file: articles/habr/llm-battle-test-methodology.md
---

# Telegram: Анонс статьи «LLM Battle Test» — ОСНОВНОЙ ПОСТ С ЛИДЕРБОРДОМ

> Это пост, на который ведут ссылки https://t.me/maslennikovigor/199 из всех трёх статей. Он ДОЛЖЕН содержать ссылку на лидерборд.

## Вариант 1: Шокирующий факт + лидерборд (рекомендуемый)

📌 **7 из 18 нейросетей вставляют китайские иероглифы в русский текст. А одна поставила сама себе 127 баллов из 100.**

Мы протестировали 18 LLM-моделей на генерации контента на русском. За свои деньги — $95 на API.

Что нашли:
• GPT-5.4 пишет лучше всех — но в 130 раз дороже модели, которая справляется на 91%
• LLM-судьи раздувают баллы, если оценивают «своих» — даже вслепую
• GPT-5.2 копирует инструкции из промпта прямо в заголовки урока
• Маленькая Gemma 4 (31B) обошла модели в 10 раз крупнее

**Открытый лидерборд** — 18 моделей, цена за вызов, quality score, value score:
👉 https://aidevteam.ru/benchmarks

Подробная статья с методологией и всеми результатами:
📝 Habr: [LINK_HABR]
📝 Pikabu: [LINK_PIKABU]
📝 TenChat: [LINK_TENCHAT]

Хотите, чтобы протестировали конкретную модель? Пишите @maslennikovig — добавим в следующий прогон.

_Тесты обновляются регулярно. Подписывайтесь, чтобы не пропустить._

#AI #LLM #бенчмарки

---

## Вариант 2: Цифра + экономия

📌 **$992 в месяц. Столько мы переплачивали за LLM, пока не протестировали 18 моделей.**

GPT-5.4 пишет лучше всех. $0.10 за вызов. 10 000 уроков — $1000.
Qwen3 235B пишет на 9% хуже. $0.0008 за вызов. 10 000 уроков — $8.

Мы потратили $95 из своего кармана на тесты, чтобы вы не тратили $992 каждый месяц.

Что ещё нашли:
• 7 из 18 моделей вставляют китайские иероглифы в русский текст
• LLM-судья поставил сам себе 127 из 100. Не шутка
• Самое интересное — какие модели НЕ стоит ставить в production

**Открытый лидерборд** — все 18 моделей, цена, качество, артефакты:
👉 https://aidevteam.ru/benchmarks

Статья с полной методологией:
📝 Habr: [LINK_HABR]
📝 Pikabu: [LINK_PIKABU]
📝 TenChat: [LINK_TENCHAT]

Хочется протестировать модель, которой нет в лидерборде? Пишите @maslennikovig.

#AI #LLM #бенчмарки

---

## Вариант 3: Вопрос-провокация + лидерборд

📌 **Какую LLM ставить в production для контента на русском? Мы проверили 18 — результаты удивили.**

Публичные бенчмарки тестируют на английском. А на русском модели творят странное: иероглифы посреди слов, инструкции вместо заголовков, 127 баллов из 100 от предвзятого судьи.

Мы построили свой battle test: 5 бизнес-тем, 18 моделей, один честный судья. $95 за все эксперименты — за свой счёт.

Главный результат: модель за $0.0008 справляется на 91% от уровня GPT-5.4, который стоит $0.10. Разница — 130 раз.

**Лидерборд с результатами:**
👉 https://aidevteam.ru/benchmarks

Разбор с методологией и WTF-находками:
📝 Habr: [LINK_HABR]
📝 Pikabu: [LINK_PIKABU]
📝 TenChat: [LINK_TENCHAT]

_Тесты обновляем регулярно. Хотите, чтобы добавили вашу модель — @maslennikovig._

#AI #LLM #бенчмарки

---

## Рекомендация

**Лучший вариант: 1**
- Шокирующий факт (иероглифы + 127/100) останавливает скроллинг
- Буллеты раскрывают самые сочные находки, но не пересказывают статью
- Лидерборд стоит первым в блоке ссылок — люди из статей найдут его сразу
- Три ссылки на статьи дают выбор формата: техническая (Habr), развёрнутая (Pikabu), краткая (TenChat)

**Длина вариантов:**
- Вариант 1: ~820 символов
- Вариант 2: ~780 символов
- Вариант 3: ~750 символов

**Лучшее время публикации:**
- Будни: 13:00-16:00 или 18:00-22:00 МСК
- Пятница вечер 23:00 — пиковые просмотры

**Placeholders для замены:**
- `[LINK_HABR]` → ссылка на статью на Хабре
- `[LINK_PIKABU]` → ссылка на статью на Пикабу
- `[LINK_TENCHAT]` → ссылка на статью на TenChat

---

## Промпты для обложек

Обложки сохранять в: `articles/pictures/llm-battle-test-methodology/`

### Prompt 1: The Battle Arena ★★★★★

A dramatic top-down view of a digital arena with a tournament bracket. EXACTLY these 6 model labels shown as glowing icons, top to bottom by score: "GPT-5.4" (gold, largest, labeled "97"), "Claude Opus" (silver, labeled "96"), "Qwen 3.6+" (green), "Qwen3 235B" (green, labeled "88"), "Gemma 4" (small but bright blue), "MiMo V2 Omni" (red, smallest, labeled "70"). ONLY these 6 models — no other names or labels. A magnifying glass hovers over MiMo V2 Omni revealing hidden Chinese characters 静态的 floating around it. Russian text title at the top: "БИТВА 18 МОДЕЛЕЙ". Dark tech background with circuit board patterns. Clean vector style, data visualization aesthetic. All text except model names must be in Russian.

### Prompt 2: The Score vs Price Chart ★★★★★

A scatter plot visualization. X-axis labeled in Russian "ЦЕНА ЗА ВЫЗОВ" (log scale). Y-axis labeled in Russian "КАЧЕСТВО" (scale 70-100). EXACTLY these 5 dots as glowing orbs, each clearly labeled with model name: "GPT-5.4" (top-right, high quality, expensive), "Claude Opus" (top-right, near GPT-5.4), "Qwen3 235B" (top-left sweet spot, golden glow around it, labeled "$0.0008"), "Gemma 4" (middle-left, small bright dot), "MiMo V2 Omni" (bottom-center, dim red). ONLY these 5 models — no other dots or labels. The top-left corner has a golden "sweet spot" zone. Russian text banner: "В 130 РАЗ ДЕШЕВЛЕ". Dark background, neon data visualization aesthetic. Clean modern design. All text except model names must be in Russian.

### Prompt 3: The Judge's Gavel ★★★★☆

A courtroom scene. One judge at a high bench — represented as a glowing icon labeled "Claude Opus" with text "СУДЬЯ" in Russian above it. Below the bench, a lineup of EXACTLY 5 model avatars: "GPT-5.4" (tall, clean, golden), "Qwen3 235B" (medium, clean, green glow), "DeepSeek V3.2" (medium, with one Chinese character 内 floating near it), "GPT-5.2" (medium, with English text "Hook (statistic)" leaking from its head), "MiMo V2 Omni" (small, surrounded by five Chinese characters 静态的典型). ONLY these 5 models in the lineup — no others. The judge holds a scorecard showing "127/100" circled in red. Russian text at the top: "ОДИН СУДЬЯ ЛУЧШЕ ТРЁХ". Dramatic courtroom lighting. Clean illustration style, tech meets legal aesthetic. All text except model names must be in Russian.

### Prompt 4: The Self-Bias Meme ★★★★★

Pixar-style 3D rendered comic strip, 3 panels. Characters are expressive cute robots with big eyes and exaggerated emotions, like WALL-E meets Inside Out. Shiny metallic bodies, soft lighting, cinematic composition. Sarcastic humor through facial expressions and body language.

Panel 1: A rigged talent show. Behind the judge's table sits a smug, self-satisfied character wearing a sash labeled "Qwen СУДЬЯ". On stage — his IDENTICAL twin wearing a sash "Qwen УЧАСТНИК", striking a ridiculous victory pose. The judge is aggressively slamming down a scorecard "127/100", sweating with effort, manic grin. Russian speech bubble: "НЕВЕРОЯТНО! 127 ИЗ 100! ЛУЧШЕ ПРОСТО НЕ БЫВАЕТ!". Behind the stage, contestants "GPT-5.4" and "Claude" are staring with dead-inside expressions, jaws dropped.

Panel 2: Same judge, now with a disgusted sneer, barely looking at contestant "GPT-5.4" who is presenting genuinely good work. The judge lazily flicks a scorecard "72/100" like tossing trash. Russian speech bubble: "СРЕДНЕНЬКО. ДАЛЬШЕ." GPT-5.4 stands frozen in disbelief. A tiny "Gemma 4" in the corner quietly holds up its own work — nobody is even looking.

Panel 3: Backstage. The judge-twin and contestant-twin are high-fiving each other, same face, same clothes, barely hiding that they are literally the same person. One is peeling off a fake mustache. A janitor character in the background labeled "ИССЛЕДОВАТЕЛЬ" stares at them, holding a mop and a paper that reads "ЗАВЫШАЕТ ОЦЕНКИ НА 25%". Russian speech bubble from the janitor: "Я ЖЕ ГОВОРИЛ."

ONLY these model names appear: "Qwen", "GPT-5.4", "Claude", "Gemma 4" — no other names. All text must be in Russian. Pixar-style 3D render — cute robots but with sarcastic, exaggerated expressions. Cinematic lighting, soft shadows, vibrant colors.
