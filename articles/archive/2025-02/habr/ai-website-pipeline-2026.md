---
platform: habr
title: "AI-пайплайн для лендингов: от промпта до продакшена за 3 дня"
subtitle: "Whisk + Veo + Claude + Next.js: собираем сайт уровня студии без студии"
author: Igor Maslennikov
date: 2026-01-18
tags: [AI, Web Development, Next.js, Claude, Generative AI, Frontend, Motion, Animation]
language: ru
---

# AI-пайплайн для лендингов: от промпта до продакшена за 3 дня

Каждый второй предприниматель хочет "сайт как у Apple". На вопрос "какой бюджет?" — пауза и "ну, тысяч 50 максимум".

Окей.

Проблема в том, что "сайт как у Apple" — это команда из 5+ человек, несколько месяцев работы и бюджет с шестью нулями. Но в 2026 году появилась альтернатива: **AI-пайплайн**, который позволяет одному человеку собрать лендинг премиального уровня за дни, а не месяцы.

Эта статья — техническое руководство по сборке такого пайплайна. С кодом, промптами, граблями и реальными цифрами.

**Дисклеймер**: Здесь не будет скриншотов готового сайта. Намеренно. Вместо этого — рабочие промпты и конфигурации. Копируйте, адаптируйте, пробуйте. Лучший способ понять — сделать.

<cut />

## Оглавление

1. [Архитектура пайплайна](#architecture)
2. [Генерация визуалов (Whisk + Gemini 3)](#visuals)
3. [Видеогенерация (Google Flow / Veo)](#video)
4. [Оптимизация ассетов (WebP + Lazy Loading)](#optimization)
5. [Кодогенерация (Claude + структурированные промпты)](#code)
6. [UI-библиотеки (Hero UI + Motion.dev)](#ui)
7. [Деплой в России (Amvera Cloud)](#deploy)
8. [Итоговая архитектура и цифры](#summary)
9. [Грабли и как их обходить](#pitfalls)

---

<a name="architecture"></a>
## 1. Архитектура пайплайна

Типичный процесс создания лендинга в студии:

```
Бриф → Дизайнер (2 нед) → Разработчик (3 нед) → Тестировщик (1 нед) → Деплой
                                                                    ↓
                                                            6-8 недель, 300-500K ₽
```

AI-пайплайн:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AI WEBSITE PIPELINE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  │ Google Whisk │     │ Google Flow  │     │   FFmpeg     │            │
│  │   (Gemini 3) │────►│    (Veo)     │────►│  MP4→WebP    │            │
│  │              │     │              │     │              │            │
│  │ Prompt → PNG │     │ PNGs → MP4   │     │ Optimize     │            │
│  └──────────────┘     └──────────────┘     └──────────────┘            │
│         │                                         │                     │
│         │ Кадр А, Кадр Б                         │ animation.webp      │
│         ▼                                         ▼                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        Claude Code                               │   │
│  │                                                                  │   │
│  │  Structured Prompt (XML) → Next.js 15 + TypeScript + Tailwind   │   │
│  │                                                                  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │   │
│  │  │  Hero UI    │  │ Motion.dev  │  │  21st.dev   │             │   │
│  │  │ Components  │  │ Animations  │  │  Blocks     │             │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Amvera Cloud                                │   │
│  │                                                                  │   │
│  │  git push amvera main → Build → Deploy → SSL → CDN              │   │
│  │                                                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  Timeline: 3 дня        Cost: ~5 000 ₽        Quality: Premium          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Компоненты:**

| Этап | Инструмент | Вход | Выход |
|------|-----------|------|-------|
| Генерация изображений | Google Whisk (Gemini 3) | Текстовый промпт | PNG 2048x2048 |
| Генерация видео | Google Flow (Veo) | 2 PNG + промпт | MP4 5 секунд |
| Оптимизация | FFmpeg | MP4 | WebP (animated) |
| Кодогенерация | Claude | Structured prompt | Next.js project |
| UI | Hero UI + Motion.dev | Компоненты | Премиальный дизайн |
| Хостинг | Amvera Cloud | git push | Production URL |

---

<a name="visuals"></a>
## 2. Генерация визуалов (Whisk + Gemini 3)

### Проблема стоковых фото

Стоковые фото — это мгновенно распознаваемый "запах" дешёвого сайта. Ваши конкуренты используют те же кадры с Shutterstock. Уникальные фотосессии — от 30K ₽.

### Решение: Google Whisk

[labs.google/whisk](https://labs.google/whisk) — экспериментальный инструмент от Google на базе Gemini 3. Генерирует фотореалистичные изображения с контролем стиля и композиции.

**Ключевой паттерн промпта:**
```
[Объект], [техника съёмки], [освещение], [фон], [стиль], [качество]
```

### Промпты для кофейного лендинга

**Кадр А — зерно (начало анимации):**
```
Single roasted coffee bean, extreme macro photography, dark moody background,
cinematic lighting from above, shallow depth of field, rich brown texture details,
professional product photography style, 8K quality
```

**Кадр Б — чашка (конец анимации):**
```
Perfect espresso in white ceramic cup, top-down view matching previous angle,
dark moody background, cinematic lighting, steam rising gently, rich crema layer,
professional product photography style, 8K quality
```

**Важно:** `matching previous angle` — инструкция для сохранения ракурса между кадрами. Это критично для плавной анимации.

### Типичные грабли

1. **Слишком длинные промпты** — Gemini начинает игнорировать детали. Держите промпт до 50 слов.

2. **Противоречивые инструкции** — "bright lighting" + "moody atmosphere" = непредсказуемый результат.

3. **Отсутствие якоря качества** — без "8K quality" или "professional photography" результат может быть мультяшным.

### Стоимость

- Бесплатный tier: ~50 генераций/день
- Pro: $20/месяц (без лимитов)

---

<a name="video"></a>
## 3. Видеогенерация (Google Flow / Veo)

### Зачем анимация

Статистика: средняя глубина скролла на статичных лендингах — 40-50%. С scroll-triggered анимацией — 70-80%. Анимация удерживает внимание.

### Google Flow (Veo)

[deepmind.google/technologies/veo](https://deepmind.google/technologies/veo) — видеомодель от DeepMind. Flow — интерфейс для создания переходов между кадрами.

**Входные данные:**
- Start frame: Кадр А (PNG)
- End frame: Кадр Б (PNG)
- Prompt: описание перехода
- Duration: 5 секунд (оптимально для scroll-анимации)

### Промпт для перехода

```
Smooth cinematic transformation: coffee bean slowly roasts, cracks open releasing
aromatic particles, grinds into fine powder with swirling motion, powder flows
and transforms into liquid espresso filling the cup. Maintain dark moody lighting
throughout. Clockwise spiral motion. Professional commercial quality, 5 seconds.
```

### Уточняющий промпт (если анимация дёргается)

```
Keep consistent clockwise rotation direction throughout the entire transformation.
Smooth continuous motion, no sudden changes. Seamless morphing between states.
```

### Грабли

1. **Физика** — AI плохо понимает физику жидкостей. Если кофе льётся вверх — уточните направление в промпте.

2. **Цикличность** — для бесконечного loop нужно, чтобы последний кадр совпадал с первым. Добавьте "seamless loop" в промпт.

3. **Длина** — видео >5 секунд теряет качество. Лучше несколько коротких сегментов.

### Стоимость

~$30 за генерацию (зависит от длины и разрешения)

---

<a name="optimization"></a>
## 4. Оптимизация ассетов (WebP + Lazy Loading)

### Проблема: размер MP4

Типичное 5-секундное видео 1080p = 5-15 MB. На мобильном интернете это катастрофа.

### Решение: Animated WebP

WebP поддерживает анимацию и весит в 5-10 раз меньше MP4 при сопоставимом качестве.

**Конвертация через FFmpeg:**

```bash
# MP4 → WebP (animated)
ffmpeg -i coffee-transformation.mp4 \
  -vcodec libwebp \
  -lossless 0 \
  -compression_level 6 \
  -q:v 70 \
  -loop 0 \
  -preset picture \
  -an \
  -vsync 0 \
  coffee-transformation.webp

# Результат: 15 MB → 1.5 MB
```

**Параметры:**
- `-q:v 70` — качество (0-100, 70 — оптимальный баланс)
- `-compression_level 6` — уровень сжатия (0-6)
- `-loop 0` — бесконечный цикл
- `-an` — убрать аудиодорожку

### Lazy Loading в Next.js

```tsx
// components/CoffeeAnimation.tsx
import Image from 'next/image'
import { useInView } from 'motion/react'

export function CoffeeAnimation() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true })

  return (
    <div ref={ref}>
      {isInView && (
        <Image
          src="/coffee-transformation.webp"
          alt="Coffee transformation"
          width={1920}
          height={1080}
          priority={false}
          loading="lazy"
        />
      )}
    </div>
  )
}
```

### Scroll-triggered playback

```tsx
// components/ScrollAnimation.tsx
import { useScroll, useTransform, motion } from 'motion/react'

export function ScrollAnimation() {
  const { scrollYProgress } = useScroll()

  // Map scroll position (0-1) to animation frame
  const frame = useTransform(scrollYProgress, [0, 1], [0, 100])

  return (
    <motion.div style={{
      backgroundPosition: useTransform(frame, (f) => `0 ${-f * 10}px`)
    }}>
      {/* Sprite sheet или canvas-based animation */}
    </motion.div>
  )
}
```

---

<a name="code"></a>
## 5. Кодогенерация (Claude + структурированные промпты)

### Проблема: "сделай мне сайт"

Если просто сказать Claude "сделай сайт для кофейни" — получите generic bootstrap-стиль. AI не телепат.

### Решение: структурированные промпты

Claude отлично понимает XML-теги. Используйте их для организации контекста.

**Шаблон промпта:**

```xml
<context>
Project: [название и описание]
Assets: [какие файлы уже есть]
Brand: [цвета, шрифты, настроение]
</context>

<requirements>
- [технологический стек]
- [ключевые фичи]
- [ограничения]
</requirements>

<structure>
1. [секция 1]
2. [секция 2]
...
</structure>

<examples>
[примеры желаемого результата или референсы]
</examples>
```

### Реальный промпт для кофейного лендинга

```xml
<context>
Project: Landing page for premium craft coffee brand "Black Bean"
Assets: coffee-transformation.webp animation in /public folder (1.5MB, 5s loop)
Brand colors: #1a1a1a (dark), #8B4513 (coffee brown), #F5F5DC (cream)
Typography: Inter for body, Playfair Display for headings
Mood: Premium, artisan, warm, inviting
</context>

<requirements>
- Next.js 15 + TypeScript + Tailwind CSS
- Hero section with scroll-triggered animation using Motion.dev
- Animation plays as user scrolls (scrollytelling effect, not autoplay)
- Mobile-first responsive design (375px → 1440px)
- Hero UI components for buttons, cards, inputs
- Lighthouse score > 90 for Performance
- No external fonts loading (use next/font)
</requirements>

<structure>
1. Hero: Full-screen, coffee animation tied to scroll progress (0-100%)
   - Headline: "From Bean to Cup" with fade-in
   - Subheadline: "Craft coffee, roasted with precision"
   - CTA button: "Explore Menu" → scrolls to section 3

2. Story: "Our Process" - 3 cards with process steps
   - Card 1: "Select" - зерно, описание отбора
   - Card 2: "Roast" - процесс обжарки
   - Card 3: "Brew" - приготовление
   - Animation: cards fade in sequentially on scroll

3. Menu: Grid of signature drinks (2 columns mobile, 4 desktop)
   - Each item: image, name, description, price
   - Hover effect: scale 1.02, shadow increase

4. Contact: Location map + order form
   - Form fields: Name, Phone, Preferred drink
   - Submit → console.log (no backend)
</structure>
```

### Итеративные уточнения

После первой генерации обычно нужны уточнения. Примеры:

```
Fix: Hero section has horizontal scroll on mobile.
Add overflow-x-hidden to the container.
```

```
Change: Button color should be coffee brown (#8B4513)
with cream text (#F5F5DC), not the default blue.
```

```
Add: Smooth scroll behavior for anchor links.
Use scroll-behavior: smooth in global CSS.
```

---

<a name="ui"></a>
## 6. UI-библиотеки (Hero UI + Motion.dev)

### Hero UI (бывший NextUI)

[heroui.com](https://heroui.com) — React-компоненты в стиле Apple. Glassmorphism, мягкие тени, микро-анимации из коробки.

**Установка:**

```bash
npm install @heroui/react
```

**Конфигурация (tailwind.config.js):**

```javascript
const { heroui } = require("@heroui/react")

module.exports = {
  content: [
    // ...
    "./node_modules/@heroui/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  plugins: [heroui({
    themes: {
      coffee: {
        colors: {
          primary: {
            DEFAULT: "#8B4513",
            foreground: "#F5F5DC",
          },
          background: "#1a1a1a",
        }
      }
    }
  })],
}
```

**Промпт для Claude — внедрение Hero UI:**

```
Install Hero UI: npm install @heroui/react

Then replace these elements:
- All <button> → <Button> from @heroui/react with variant="shadow" color="primary"
- All card containers → <Card> with isBlurred shadow="lg"
- Contact form inputs → <Input> with variant="bordered" and validation
- Add <Navbar> with blur effect: isBlurred className="bg-background/60"

Keep existing layout, only upgrade visual components.
```

### Motion.dev (Framer Motion)

[motion.dev](https://motion.dev) — анимации для React. Декларативный API, привязка к скроллу.

**Установка:**

```bash
npm install motion
```

**Основные паттерны:**

```tsx
// 1. Fade in on scroll
import { motion } from 'motion/react'

<motion.div
  initial={{ opacity: 0, y: 20 }}
  whileInView={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
  viewport={{ once: true }}
>
  Content appears on scroll
</motion.div>

// 2. Stagger children
<motion.ul
  initial="hidden"
  whileInView="visible"
  variants={{
    visible: { transition: { staggerChildren: 0.2 } }
  }}
>
  {items.map(item => (
    <motion.li
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
      }}
    >
      {item}
    </motion.li>
  ))}
</motion.ul>

// 3. Scroll-linked animation
import { useScroll, useTransform } from 'motion/react'

const { scrollYProgress } = useScroll()
const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0])

<motion.div style={{ opacity }}>
  Fades as you scroll
</motion.div>
```

**Промпт для Claude — добавление анимаций:**

```
Add Motion.dev animations:

1. Hero: coffee animation plays based on scroll progress (0-100%)
   - useScroll() + useTransform() to map scroll to frame

2. Story cards: fade in + slide up on viewport enter
   - stagger: 0.2s delay between cards
   - whileInView={{ opacity: 1, y: 0 }}

3. Menu grid: scale from 0.95 to 1 on appear
   - hover: y: -5px, shadow increase

4. Stats: count-up animation when visible
   - animate from 0 to value over 2s
```

### 21st.dev — готовые блоки

[21st.dev](https://21st.dev) — библиотека React-компонентов с кнопкой "Copy Prompt for AI".

**Workflow:**
1. Выбираете блок (Testimonials, FAQ, Pricing)
2. Нажимаете "Copy Prompt"
3. Вставляете в Claude с адаптацией под ваш проект

**Пример адаптации:**

```
[Вставленный промпт с 21st.dev]

Adapt for coffee shop "Black Bean":
- Replace testimonials:
  1. "Лучший кофе в городе!" — Анна М.
  2. "Наконец-то настоящий эспрессо" — Дмитрий К.
  3. "Бариста знают своё дело" — Елена С.
- Colors: #1a1a1a, #8B4513, #F5F5DC
- Star ratings: all 5 stars
- Remove social media icons
```

---

<a name="deploy"></a>
## 7. Деплой в России (Amvera Cloud)

### Проблема с зарубежными хостингами

- **Vercel/Netlify**: оплата из России затруднена, санкционные риски
- **Cloudflare Pages**: Роскомнадзор рекомендовал отказаться от TLS ECH
- **Latency**: сервера в US/EU = 100-200ms для российских пользователей

### Amvera Cloud

[amvera.ru](https://amvera.ru) — российский хостинг с push-to-deploy (как Vercel).

**Преимущества:**
- Оплата рублями
- Сервера в России (низкий latency)
- Git-based deploy
- Бесплатный SSL
- Стартовый баланс 111 ₽

**Настройка проекта:**

1. **amvera.yml в корне проекта:**

```yaml
meta:
  environment: node
  toolchain:
    name: node
    version: 20

build:
  - npm ci
  - npm run build

run:
  persistenceMount: /data
  containerPort: 3000
  command: npm start
```

2. **Подключение репозитория:**

```bash
# Добавляем remote
git remote add amvera https://git.amvera.ru/<username>/<project>

# Деплоим
git push amvera main

# Автодеплой: каждый push в main → пересборка → публикация
```

3. **Подключение домена:**

```
Настройки проекта → Домены → Добавить домен
DNS: A-запись на IP Amvera или CNAME на <project>.amvera.app
SSL: выдаётся автоматически через Let's Encrypt
```

### Альтернативы

| Хостинг | Цена | Сложность | Для кого |
|---------|------|-----------|----------|
| Amvera Cloud | от 170 ₽/мес | Низкая | Лендинги, простые приложения |
| Selectel Cloud | от 500 ₽/мес | Средняя | Средние проекты, нужен SSH |
| Timeweb Cloud | от 300 ₽/мес | Средняя | VPS с Node.js |
| Self-hosted (Coolify) | от 500 ₽/мес | Высокая | Полный контроль |

---

<a name="summary"></a>
## 8. Итоговая архитектура и цифры

### Финальный стек

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION STACK                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Framework:     Next.js 15 (App Router)                     │
│  Language:      TypeScript                                   │
│  Styling:       Tailwind CSS + Hero UI                       │
│  Animations:    Motion.dev (Framer Motion)                   │
│  Assets:        WebP (animated), next/font                   │
│  Hosting:       Amvera Cloud                                 │
│  CDN:           Встроенный (Amvera)                         │
│  SSL:           Let's Encrypt (auto)                         │
│                                                              │
│  Bundle size:   ~150KB (gzipped)                            │
│  Lighthouse:    95+ Performance                              │
│  TTFB:          <200ms (для РФ)                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Экономика проекта

| Статья | AI-пайплайн | Студия |
|--------|-------------|--------|
| Визуалы (генерация) | ~$50 (3 000 ₽) | 80 000 ₽ (фотосессия) |
| Видеопродакшн | ~$30 (2 000 ₽) | 100 000 ₽ |
| Разработка | ~$20 (Claude Pro) | 200 000 ₽ |
| UI/UX дизайн | $0 (Hero UI) | 100 000 ₽ |
| Хостинг (год) | 2 040 ₽ | 60 000 ₽ |
| **Итого** | **~7 000 ₽** | **540 000 ₽** |

**Экономия: ~533 000 ₽ (98.7%)**

### Временные затраты

| Этап | AI-пайплайн | Студия |
|------|-------------|--------|
| Генерация визуалов | 2-3 часа | 1-2 недели |
| Видео | 1-2 часа | 1 неделя |
| Разработка | 1-2 дня | 3-4 недели |
| Тестирование | 2-4 часа | 1 неделя |
| **Итого** | **2-3 дня** | **6-8 недель** |

---

<a name="pitfalls"></a>
## 9. Грабли и как их обходить

### 1. "AI сгенерировал мусор"

**Причина:** слишком общий промпт.

**Решение:** структурируйте промпт через XML-теги. Указывайте конкретные технологии, размеры, цвета.

```diff
- "сделай сайт для кофейни"
+ "<context>Project: Landing for premium coffee brand...</context>"
```

### 2. "Анимация тормозит на мобильных"

**Причина:** тяжёлые ассеты, много одновременных анимаций.

**Решение:**
- WebP вместо MP4
- `will-change: transform` для анимируемых элементов
- Максимум 3-5 анимаций на viewport
- `viewport={{ once: true }}` — анимация только один раз

### 3. "Hero UI конфликтует с Tailwind"

**Причина:** не подключен плагин в tailwind.config.js.

**Решение:**
```javascript
plugins: [heroui()]
```

И добавить путь к компонентам в `content`.

### 4. "Amvera не билдит проект"

**Причина:** неправильный amvera.yml или отсутствует package-lock.json.

**Решение:**
```bash
# Убедитесь, что lock-файл в репозитории
git add package-lock.json
git commit -m "Add package-lock.json"
git push amvera main
```

### 5. "Lighthouse ругается на LCP"

**Причина:** анимация в Hero-секции грузится как eager.

**Решение:**
```tsx
<Image
  src="/animation.webp"
  priority={true}  // для Hero — priority
  loading="eager"  // не lazy для первого экрана
/>
```

---

## Disclaimer: Expected Pushback

Я понимаю, что эта статья вызовет критику.

**"Это не заменит нормального дизайнера"**

Не заменит. Для сложных проектов с уникальным UX нужен человек. Но для типовых лендингов малого бизнеса — AI-пайплайн даёт результат на уровне средней студии за 1% цены.

**"AI-генерации все одинаковые"**

Если использовать дефолтные промпты — да. Вся магия в кастомизации: уникальные визуалы (Whisk), кастомные цвета (Hero UI themes), осмысленные анимации (Motion.dev). Результат зависит от промптов.

**"Зачем такая сложность, если есть Tilda?"**

Tilda — отличный инструмент. Но: ограниченная кастомизация, шаблонный вид, проблемы с производительностью на сложных страницах. Next.js + кастомные компоненты дают больше контроля и лучший Lighthouse score.

Если у вас есть лучший подход — напишите в комментариях. Всегда открыт к улучшениям.

---

## Ссылки

**AI-инструменты:**
- Google Whisk: https://labs.google/whisk
- Google Veo: https://deepmind.google/technologies/veo
- Claude: https://claude.ai

**Библиотеки:**
- Next.js: https://nextjs.org
- Hero UI: https://heroui.com
- Motion.dev: https://motion.dev
- 21st.dev: https://21st.dev

**Хостинг (Россия):**
- Amvera Cloud: https://amvera.ru
- Selectel: https://selectel.ru
- Timeweb Cloud: https://timeweb.cloud

---

## Контакты

**Автор:** Игорь Масленников
*Пишу про AI-автоматизацию, LLM-инструменты и архитектуру веб-приложений.*

📢 **Мой канал в Telegram:** [@maslennikovigor](https://t.me/maslennikovigor) — там я публикую разборы AI-инструментов и DevOps-лайфхаки.

💬 **Личный контакт:** [@maslennikovig](https://t.me/maslennikovig) — для вопросов, идей и обратной связи.

🔧 **GitHub:** [claude-code-orchestrator-kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) — open-source инструменты для AI-автоматизации.

Если попробуете пайплайн — напишите, что сработало, что нет. Буду рад фидбеку.
