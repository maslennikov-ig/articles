# Промпты для обложек: DeepSeek V4 Pro paradox

Три варианта на английском для генерации (Midjourney / Whisk / Imagen / другой генератор). Рейтинг ★ — мой прогноз попадания в смысл статьи. Все апрельские релизы (включая Qwen) — фактически современники, без «прошлогодних» моделей.

После генерации — складываем готовые PNG в эту же папку (`articles/pictures/llm-battle-test-deepseek-v4-paradox/`). Анжела возьмёт оттуда нужную для каждой платформы.

---

## Prompt 1: David vs Goliath (Flash beats Pro on value) ★★★★★

```
A dramatic side-by-side comparison: on the left, a tiny but glowing "Flash" robot
character holding a piggy bank with "$0.0019" floating above. On the right, a massive
industrial-looking "Pro" robot with cogs and machinery, with "$0.0256 × 13" floating
above and a slightly tired expression. Between them, a scoreboard showing "83 vs 89"
with a small "+6" highlighted in subtle red. Dark tech background with glowing data
streams. Underdog narrative aesthetic. Clean vector style. 16:9 aspect ratio.
```

**Когда использовать:** Универсальный вариант — годится для Habr, Pikabu, TenChat. Главный смысл статьи передаётся одним кадром: маленький Flash побеждает большого Pro по экономике.

---

## Prompt 2: Score per Dollar Chart (Flash dominates) ★★★★★

```
A striking horizontal bar chart titled "Score per Dollar — кто реально эффективен?"
Bars represent: DeepSeek V4 Flash (longest, glowing gold, "43,684"), DeepSeek V4 Pro
(much shorter, gray, "3,477"), Kimi K2.6 (shortest, dim, "1,841"). Below each bar —
model name and price/call. Dark background, neon data viz aesthetic. Modern
infographic. 16:9 aspect ratio.
```

**Когда использовать:** Для Habr и TenChat — техническая/бизнес-аудитория любит наглядную аналитику. Хорошо работает как preview-картинка в ленте.

---

## Prompt 3: The Paradox (Earlier April Qwen beats Latest DeepSeek) ★★★★☆

```
A retro-futuristic award-ceremony scene: an "April 2 release" Qwen robot standing
tall on a podium with a gold medal "92". Below it, a sleek "April 24 release"
DeepSeek V4 Pro robot looking puzzled with a silver medal "89". A small calendar in
the background showing "April 2026" with both dates circled. Audience of other robots
watching. Dramatic spotlight, courtroom-meets-tech aesthetic. 16:9 aspect ratio.
```

**Когда использовать:** Если статья будет акцентировать парадокс «свежий флагман проиграл более раннему апрельскому релизу». Подойдёт для Pikabu (драматизм) и как альтернатива для Habr.

⚠️ ВАЖНО: оба робота — апрельские релизы 2026. Qwen вышел 2 апреля, DeepSeek V4 Pro — 24 апреля. Не «old vs new», а «3 weeks earlier vs latest».

---

## Технические требования

- **Размер:** минимум 1280×720 (16:9), оптимально 1920×1080
- **Формат:** PNG или JPG
- **Стиль:** без фотореализма людей, без лиц с распознаваемой внешностью
- **Цветовая палитра:** тёмный фон + неоновые/металлические акценты (под технический контент)
- **Текст на изображении:** допустимо, но минимум — статья сама объяснит цифры

## Что НЕ нужно генерировать

- Логотипы реальных компаний (DeepSeek, Qwen, Kimi) — только generic robot/AI characters
- Фото реальных людей
- Confused / sad faces у моделей — мы не критикуем, мы анализируем
- Маркетинговые баннеры с кучей текста

## Адаптация под платформы

| Платформа | Лучший промпт | Кроп |
|---|---|---|
| Habr | Prompt 1 или Prompt 2 | 16:9 (превью в ленте) |
| Pikabu | Prompt 1 или Prompt 3 | Квадрат или 16:9 |
| TenChat | Prompt 2 (инфографика) | 4:3 или 16:9 |
| Telegram анонс | Prompt 1 (универсальный) | Любой, главное — читается на мобильном |
