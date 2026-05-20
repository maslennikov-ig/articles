# Промпты для обложек: Codex дайджест за 5 месяцев 2026

Генерируем обложки к статье `articles/habr/whats-new-codex-5-months-digest.md` — дайджест по changelog Codex CLI за январь-май 2026. Подходит Whisk / Midjourney / Imagen / другой генератор изображений с поддержкой длинных промптов и текста на изображении.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/whats-new-codex-5-months-digest/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: Before/After наблюдаемость субагентов ★★★★★

```
A wide cinematic illustration, 16:9 aspect ratio, split horizontally into two halves with a clean vertical divider in the middle.

Left half (warm, slightly chaotic): a developer's desk at night, dim warm light, multiple terminal windows scattered across two monitors, sticky notes everywhere, arrows drawn between terminals with a thin red marker, a coffee mug. Above the desk, a thought bubble showing tangled lines representing copy-paste between sessions. A faint label on the left half in Russian: "Раньше: ручное копирование между сессиями".

Right half (cool, organized): the same desk, but cleaner. One main monitor showing a clean modern desktop app interface with a vertical list of agent cards — each card has a small status indicator (green dot, spinner icon, paused icon), an agent name with path-style identifier like "/root/agent_a", "/root/agent_b", and a token counter. One card is highlighted as if just clicked. A faint label on the right half in Russian: "Сейчас: клик в карточку — виден весь трейс".

In the upper-center, spanning the divider, an editorial caption strip in Russian: "Codex за 5 месяцев 2026: что реально изменило работу".

Style: editorial cinematic illustration, slightly desaturated palette on the left (warm amber, brown), cool teal/blue on the right. No human faces visible (just hands, workspace details). No real company logos. No photorealism for the people — only their workspace.
```

**Когда использовать:** **Главный универсальный вариант для Habr.** Передаёт ключевой инсайт статьи (переход от ручного копирования к наблюдаемым spawned subagents) и мгновенно работает в ленте Хабра — контраст «было/стало» считывается с превью.

---

## Prompt 2: Топ-5 релизов как инфографика ★★★★☆

```
A modern editorial infographic, 16:9 aspect ratio, dark navy background with a subtle grid texture. Top of the image: a large title in Russian "Топ-5 моего рейтинга" rendered in clean bold sans-serif (Inter or Space Grotesk style).

Below the title, five horizontal cards arranged in a numbered vertical stack, each card has:
- A large rank number ("#1", "#2", "#3", "#4", "#5") on the left in glowing cyan
- A short label (mostly Russian, technical identifiers in Latin):
  Card #1: "GPT-5.5" with sublabel "Apr 2026 — на голову выше 5.4"
  Card #2: "Spawn subagents" with sublabel "Mar 2026 — путевая адресация, видимость"
  Card #3: "Browser Use" with sublabel "23 Apr — кликает в локальный UI"
  Card #4: "Desktop + mobile" with sublabel "Feb / May — мульти-устройство"
  Card #5: "Hooks + plugins" with sublabel "Apr — экосистема дозрела"
- Each card has a small icon on the right (model chip, branching tree, browser window, monitor+phone, plug-in puzzle piece)

At the bottom right, a small editorial caption in Russian: "Дайджест Codex Jan-May 2026 · habr.com/maslennikov-ig".

Color palette: dark navy background (#0a1530), accent cyan/turquoise (#00f5d4) for numbers and highlights, soft white for text. No human figures. No real company logos.

Style: clean editorial infographic, similar to product roadmap visualisations. Generous whitespace between cards. Typography-driven, not illustration-driven.
```

**Когда использовать:** Хороший вариант для **TenChat / VC.ru / Pikabu** (если будут адаптации) — инфографика-резюме, которая читается сама по себе и обещает структурированный контент. Для Habr тоже годится, но Prompt 1 эмоциональнее.

---

## Prompt 3: Workspace с несколькими активными агентами ★★★★☆

```
A cinematic illustration, 16:9 aspect ratio, a modern developer workspace shown from a slightly elevated angle. Dim ambient lighting with a single warm desk lamp and the cool glow of multiple screens.

On the desk: a large external monitor showing the Codex Desktop App interface — a clean dark UI with five horizontal agent cards visible, each card has a status indicator (some green/active, one paused, one in yellow review state) and a path-style identifier on the left (Russian context labels next to identifiers, e.g., "Тест UI" next to "/root/browser_use_agent", "Рефакторинг" next to "/root/refactor_a"). A laptop next to the monitor shows a terminal with a Codex CLI session in progress. A smartphone leaning against the monitor displays the ChatGPT mobile app with a Codex thread, screen labelled in Russian "Готов к ревью".

Above the workspace, faintly visible as if projected on the wall: five glowing icons representing the top-5 features (model chip, branching subagents tree, browser window, desktop+mobile pair, plugin puzzle piece) connected by thin glowing lines suggesting a system rather than scattered tools.

In the upper-left corner, an editorial caption strip in Russian: "Codex как agent workspace · Jan-May 2026".

Style: editorial cinematic, warm-cool contrast (warm desk lamp + cool screen glow), realistic objects with slightly stylised lighting. No human figures visible (just the implied user's workspace). No real company logos. No photorealistic faces.
```

**Когда использовать:** **Для Telegram-анонса.** Показывает «продукт в работе» — несколько активных агентов одновременно, мульти-устройство, видимая система. Хорошо читается на мобильном превью и провоцирует «хочу так же».

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** Prompt 1 — warm/cool split; Prompt 2 — dark navy + cyan; Prompt 3 — warm-cool workspace
- **Текст на изображении:** на русском, кроме имён моделей/продуктов (`GPT-5.5`, `Codex Desktop App`, `Browser Use`) и технических идентификаторов (`/root/agent_a`)

## Что НЕ нужно генерировать

- Логотипы OpenAI, Anthropic, GitHub — только generic UI/иллюстрации
- Фото реальных людей (включая упомянутых в статье — не визуализируем)
- Confused/sad faces у моделей — статья дайджест, не критика
- Маркетинговые баннеры с обилием текста
- Английские заголовки/подписи там, где русский был бы естественнее

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 (before/after) | 16:9 (превью в ленте) |
| TenChat | Prompt 2 (инфографика топ-5) | 4:3 или 16:9 |
| Pikabu | Prompt 1 или Prompt 3 | Квадрат или 16:9 |
| Telegram анонс | Prompt 3 (workspace) | 16:9, читается на мобильном |
