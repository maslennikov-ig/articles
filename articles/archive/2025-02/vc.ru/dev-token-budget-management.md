---
platform: vc.ru
title: "Token Budget Management: как архитектура с 120К токенов на батч позволяет генерировать курсы неограниченного размера"
author: Igor Maslennikov
date: 2025-11-18
length: 14500 characters
tags: AI, LLM, token budget, architecture, scalability, GPT-4, Gemini
language: ru
audience: developers
---

# Token Budget Management: как архитектура с 120К токенов на батч позволяет генерировать курсы неограниченного размера

Когда строишь систему генерации образовательного контента на LLM, первый вопрос — как масштабироваться? 8 разделов или 200 разделов — должна ли стоимость на раздел оставаться постоянной? Мы построили per-batch архитектуру с независимыми бюджетами по 120K токенов на батч. Результат: сложность O(1) на батч вместо O(n). Генерируешь 8 разделов или 200 — каждый батч получает одинаковые 120K токенов. Стоимость растет линейно и предсказуемо.

## Контекст: проблема context window в традиционных подходах

Большинство систем, работающих с LLM, накапливают контекст: раздел 1 → раздел 1 + раздел 2 → раздел 1 + раздел 2 + раздел 3... К 50-му разделу context window переполнен. Приходится обрезать старый контекст или переходить на более дорогие модели с 1M+ токенов.

**Типичная проблема**:
```typescript
// Традиционный подход — накопление контекста
let conversationHistory = [];

for (const section of sections) {
  conversationHistory.push(section);  // Контекст растет
  const result = await llm.generate({
    prompt: buildPrompt(),
    context: conversationHistory  // Раздел 1: 10K, Раздел 50: 500K+
  });
}

// Результат: context overflow после 20-30 разделов
```

Рост контекста — O(n²): каждый новый раздел добавляет не только свой контент, но и несет весь предыдущий. Стоимость растет экспоненциально.

## Решение: per-batch архитектура с изолированными бюджетами

Мы разделили генерацию на независимые батчи. **1 раздел = 1 батч = независимый бюджет 120K токенов**. Каждый батч получает:
- 90K токенов на вход (prompt + metadata + RAG + context)
- 30K токенов на выход (generated content)

**Ключевая идея**: раздел 1 стоит столько же, сколько раздел 200. Нет накопления. Нет экспоненциального роста. Только линейная зависимость: N разделов = N батчей = N × $0.084.

```typescript
// PRODUCTION PATTERN: изолированные батчи
const SECTIONS_PER_BATCH = 1;
const TOKEN_BUDGET_PER_BATCH = 120_000;

for (const section of sections) {
  const result = await generateSection(section, {
    tokenBudget: TOKEN_BUDGET_PER_BATCH,  // Независимый бюджет
    ragContext: await fetchRAGContext(section, 40_000)  // 0-40K токенов
  });

  // Контекст НЕ накапливается. Каждый батч изолирован.
}
```

## Детализация бюджета: 90K input + 30K output

120K токенов на батч — это не монолит. Внутри четкое распределение:

```typescript
const TOKEN_BUDGET = {
  TOTAL_BUDGET: 120_000,
  INPUT_BUDGET_MAX: 90_000,   // 75% на вход
  OUTPUT_BUDGET_MAX: 30_000,  // 25% на выход

  // Компоненты входа
  ESTIMATED_BASE_PROMPT: 5_000,       // Шаблон генерации
  ESTIMATED_STYLE_PROMPT: 1_000,      // Стайл-гайд
  ESTIMATED_ANALYZE_MIN: 10_000,      // Минимальная метадата
  ESTIMATED_ANALYZE_MAX: 15_000,      // Полная метадата
  ESTIMATED_SECTION_PROMPT: 3_000,    // Контекст раздела
  RAG_MAX_TOKENS: 40_000,             // Документы из базы знаний

  // Пороги для fallback
  GEMINI_TRIGGER_INPUT: 108_000,      // 90% от total
  GEMINI_TRIGGER_TOTAL: 115_000,      // 96% от total (страховка)
};
```

**90K входного бюджета распределяются**:
- **RAG контекст**: 0-40K токенов (адаптивный, зависит от сложности раздела)
- **Метадата курса**: 10-20K токенов (структура курса, предыдущие разделы)
- **System prompt**: 5-10K токенов (инструкции генерации)
- **Section context**: 5-10K токенов (контекст текущего раздела)

**30K выходного бюджета**:
- **Lesson content**: 15-20K токенов (основной контент урока)
- **Exercises**: 5-8K токенов (упражнения и тесты)
- **Metadata**: 2-5K токенов (теги, связи, навигация)

## Путь к per-batch: провал SECTIONS_PER_BATCH = 5

Первая неделя разработки — попытка генерировать 5 разделов за раз. Казалось логичным: потенциальное ускорение в 5 раз, меньше API вызовов.

**Проблема**: сложная вложенная JSON структура перегружала LLM.

```typescript
// BROKEN: генерация 5 разделов одновременно
const sections = await llm.generate({
  prompt: buildPrompt(),
  sections: [
    {
      title: "Section 1",
      lessons: [
        { title: "Lesson 1.1", objectives: [...], content: "...", exercises: [...] },
        { title: "Lesson 1.2", objectives: [...], content: "...", exercises: [...] },
        // ... 10+ уроков
      ]
    },
    // ... еще 4 раздела с таким же уровнем вложенности
  ]
});

// Результат: 45% success rate
// Типичные ошибки:
// - Missing fields (пропущены поля objectives или exercises)
// - Truncated JSON (обрезанный JSON из-за лимита токенов)
// - Wrong schema (перепутаны поля lessons и sections)
// - Field confusion (контент из Lesson 2.1 попал в Lesson 1.2)
```

**Инсайт после анализа 100+ неудач**: LLM плохо справляются с глубоко вложенными JSON массивами, содержащими объекты с 10+ полями каждый. Семантическая точность деградирует. Context window заполняется структурным оверхедом вместо логики генерации.

**Прорыв**: `SECTIONS_PER_BATCH = 1` для надежности + параллельная обработка для throughput.

```typescript
// PRODUCTION PATTERN: 95%+ success rate
const SECTIONS_PER_BATCH = 1;
const PARALLEL_BATCH_SIZE = 2;  // Обрабатываем 2 батча одновременно

for (let i = 0; i < totalSections; i += PARALLEL_BATCH_SIZE) {
  const batchPromises = [];

  for (let j = 0; j < PARALLEL_BATCH_SIZE && i + j < totalSections; j++) {
    batchPromises.push(
      generateSection(sections[i + j], {
        tokenBudget: 120_000,  // Независимый бюджет на батч
        ragContext: await fetchRAGContext(sections[i + j], 40_000)
      })
    );
  }

  const results = await Promise.all(batchPromises);
  await delay(2000);  // Соблюдение rate limit (0.5 req/sec)
}
```

**Результат**:
- **До**: SECTIONS_PER_BATCH = 5 → 45% success rate (nested JSON overload)
- **После**: SECTIONS_PER_BATCH = 1 → 95%+ success rate (простая структура)
- **Trade-off**: больше API вызовов, но выше надежность

## Динамическое управление RAG контекстом: 0-40K адаптивный бюджет

Проблема: большие курсы с множеством документов могут переполнить RAG бюджет в 40K токенов.

**Решение**: двухуровневая динамическая корректировка.

**Tier 1: расчет доступного бюджета ДО retrieval**:

```typescript
function calculateRAGBudget(
  baseTokens: number,
  styleTokens: number,
  analyzeTokens: number,
  sectionTokens: number
): number {
  const INPUT_THRESHOLD = 90_000;
  const usedTokens = baseTokens + styleTokens + analyzeTokens + sectionTokens;
  const availableForRAG = INPUT_THRESHOLD - usedTokens;

  // Ограничиваем RAG доступным бюджетом
  return Math.min(RAG_MAX_TOKENS, Math.max(0, availableForRAG));
}

// Пример: Analyze предоставил 15K токенов
// usedTokens = 24K → availableForRAG = 66K → ragBudget = min(40K, 66K) = 40K ✅

// Edge case: Analyze предоставил 30K токенов (большая метадата)
// usedTokens = 39K → availableForRAG = 51K → ragBudget = min(40K, 51K) = 40K ✅
```

**Tier 2: валидация после retrieval**:

```typescript
export function validateTokenBudget(input: {
  basePromptTokens: number;
  stylePromptTokens: number;
  analyzeTokens: number;
  sectionPromptTokens: number;
  ragTokens: number;
  estimatedOutputTokens: number;
}): {
  valid: boolean;
  totalInput: number;
  totalTokens: number;
  usagePercent: number;
  recommendation: 'OK' | 'WARNING' | 'GEMINI_FALLBACK';
  message: string;
} {
  const totalInput =
    input.basePromptTokens +
    input.stylePromptTokens +
    input.analyzeTokens +
    input.sectionPromptTokens +
    input.ragTokens;

  const totalTokens = totalInput + input.estimatedOutputTokens;
  const usagePercent = (totalTokens / TOKEN_BUDGET.TOTAL_BUDGET) * 100;

  if (totalTokens > TOKEN_BUDGET.GEMINI_TRIGGER_TOTAL) {
    return {
      valid: false,
      totalInput,
      totalTokens,
      usagePercent,
      recommendation: 'GEMINI_FALLBACK',
      message: `Total ${totalTokens} превышает порог ${TOKEN_BUDGET.GEMINI_TRIGGER_TOTAL} (использовано ${usagePercent.toFixed(1)}%). Переключение на Gemini 2.5 Flash.`
    };
  } else if (usagePercent > 85) {
    return {
      valid: true,
      totalInput,
      totalTokens,
      usagePercent,
      recommendation: 'WARNING',
      message: `Использование токенов: ${usagePercent.toFixed(1)}%. Рекомендуется сократить RAG контекст.`
    };
  } else {
    return {
      valid: true,
      totalInput,
      totalTokens,
      usagePercent,
      recommendation: 'OK',
      message: `Использование токенов: ${usagePercent.toFixed(1)}%. В пределах бюджета.`
    };
  }
}
```

## Предсказуемость стоимости: N разделов = N батчей

Главное преимущество per-batch архитектуры — **линейная зависимость стоимости от количества разделов**.

**Примеры**:
- **8 разделов**: 8 батчей × $0.084 = $0.67
- **50 разделов**: 50 батчей × $0.084 = $4.20
- **200 разделов**: 200 батчей × $0.084 = $16.80

**Нет скрытых множителей**. Нет экспоненциального роста контекста. Нет сюрпризов.

Сравнение с традиционным подходом (накопление контекста):
- **8 разделов**: ~$1.20 (контекст растет от 10K до 80K)
- **50 разделов**: ~$45.00 (контекст растет от 10K до 500K+, требует GPT-4 128K)
- **200 разделов**: невозможно (context overflow, нужна модель с 1M+ токенов)

## Неограниченный размер курса: 200-секционные курсы реальны

С per-batch архитектурой нет максимального размера курса. **Проверено на продакшене**:
- **Типичные курсы**: 8-50 разделов
- **Крупные курсы**: до 100 разделов (тестировали)
- **Теоретический предел**: нет (200+ разделов технически возможны)

**95%+ success rate** на всех размерах курсов. Изоляция батчей гарантирует, что раздел 200 генерируется с той же надежностью, что и раздел 1.

## Параллельная обработка: 2 батча с rate limits

Для увеличения throughput используем параллельную обработку — 2 батча одновременно.

```typescript
const PARALLEL_BATCH_SIZE = 2;
const RATE_LIMIT_DELAY = 2000;  // 2 секунды между партиями

async function generateAllSections(sections: Section[]): Promise<Result[]> {
  const results: Result[] = [];

  for (let i = 0; i < sections.length; i += PARALLEL_BATCH_SIZE) {
    const batchPromises = [];

    // Запускаем 2 батча параллельно
    for (let j = 0; j < PARALLEL_BATCH_SIZE && i + j < sections.length; j++) {
      const section = sections[i + j];

      batchPromises.push(
        generateSection(section, {
          tokenBudget: 120_000,
          ragContext: await fetchRAGContext(section, 40_000),
          model: 'openai/gpt-4o-mini'  // Или Gemini fallback
        })
      );
    }

    // Ждем завершения обоих батчей
    const batchResults = await Promise.all(batchPromises);
    results.push(...batchResults);

    // Соблюдаем rate limit: 0.5 req/sec
    if (i + PARALLEL_BATCH_SIZE < sections.length) {
      await delay(RATE_LIMIT_DELAY);
    }
  }

  return results;
}
```

**Параметры**:
- **PARALLEL_BATCH_SIZE = 2**: оптимальный баланс throughput vs rate limits
- **RATE_LIMIT_DELAY = 2000ms**: соблюдение лимита 0.5 requests/sec
- **Fallback**: если rate limit exceeded → увеличиваем delay до 3000ms

## Production метрики: 4 сценария валидации

Мы протестировали 4 основных сценария использования токенов:

| Сценарий | Input | Output | Total | Утилизация | Статус |
|----------|-------|--------|-------|------------|--------|
| **Standard (no RAG)** | 24K | 20K | 44K | 37% | ✅ PASS |
| **RAG-heavy (40K docs)** | 64K | 25K | 89K | 74% | ✅ PASS |
| **Minimal Analyze** | 12K | 20K | 32K | 27% | ✅ PASS |
| **RAG overflow (60K)** | 84K | 32K | 116K | 97% | ⚠️ GEMINI FALLBACK |

**Standard (no RAG)**: базовый сценарий без RAG контекста.
- Input: 5K base + 1K style + 15K analyze + 3K section = 24K
- Output: 20K (generated content)
- Утилизация: 37% (комфортный запас)

**RAG-heavy (40K docs)**: максимальный RAG контекст.
- Input: 24K base + 40K RAG = 64K
- Output: 25K (сложный раздел с упражнениями)
- Утилизация: 74% (в пределах нормы)

**Minimal Analyze**: минимальная метадата курса.
- Input: 5K base + 1K style + 3K analyze + 3K section = 12K
- Output: 20K
- Утилизация: 27% (минимальный сценарий)

**RAG overflow (60K)**: переполнение RAG бюджета.
- Input: 24K base + 60K RAG = 84K
- Output: 32K (очень сложный технический раздел)
- Total: 116K (97% утилизация)
- **Trigger**: GEMINI_FALLBACK → переключение на Gemini 2.5 Flash с 1M context window

## Gemini Fallback: неожиданная экономия

Изначально думали, что overflow сценарии обойдутся дороже. Оказалось наоборот.

**Сравнение стоимости**:
- **OSS 120B** (openai/gpt-4o-mini): $0.084 за 120K токенов (обычный случай)
- **Gemini 2.5 Flash**: $0.002 за 120K токенов (overflow случай)

**Gemini в 42 раза дешевле** для overflow сценариев! Изначально думали, что переполнение приведет к увеличению стоимости. Ошиблись. Context window Gemini в 1M токенов + цена $0.002 делают его идеальным для редких overflow случаев.

**Реальный overflow сценарий**:
```
Пользователь загрузил технический мануал на 100 страниц (350K токенов после chunking).
Retrieval для раздела вернул 10 наиболее релевантных chunks (60K токенов).
Total input: 24K base + 60K RAG = 84K.
Estimated output: 35K (сложный технический раздел с детальными примерами).
Total: 119K (99% утилизация).

Trigger: GEMINI_FALLBACK
Model: google/gemini-2.5-flash
Cost: $0.0024 (vs $0.084 если бы принудительно использовали OSS 120B)
Экономия: 97% снижение стоимости на overflow сценариях
```

## Конкурентный контекст: vs Fixed Batch vs Streaming

**vs Fixed Batch Approach** (традиционный подход):
- **Проблема**: накопление контекста → O(n²) рост токенов
- **Ограничение**: context window лимитирует размер курса (максимум 20-30 разделов)
- **Стоимость**: экспоненциальная

**vs Streaming Approach**:
- **Сложность**: сложнее валидировать (частичный JSON)
- **State management**: требуется сложная логика управления состоянием
- **Надежность**: ниже (парсинг incomplete JSON)

**Our Per-Batch Approach**:
- **Простота**: изолированные батчи, простая структура
- **Масштабируемость**: неограниченный размер курса
- **Надежность**: 95%+ success rate (простой JSON, легко валидировать)

## Уроки, которые мы извлекли

**1. Простота побеждает оптимизацию**
SECTIONS_PER_BATCH = 5 казалось эффективнее. На практике — 45% success rate. SECTIONS_PER_BATCH = 1 проще и надежнее — 95%+ success rate. Меньше API вызовов — не всегда лучше.

**2. LLM плохо справляются с deep nesting**
Глубоко вложенные JSON структуры (5 разделов × 10 уроков × 5 objectives каждый = 250+ объектов) перегружают контекст. Модели путают поля, пропускают данные, генерируют некорректный JSON.

**3. Изоляция батчей = предсказуемость**
Каждый батч с независимым бюджетом → линейная стоимость, линейная масштабируемость. Нет сюрпризов, нет экспоненциального роста.

**4. Overflow может быть дешевле**
Gemini 2.5 Flash в 42 раза дешевле OSS 120B для overflow сценариев. Не бойтесь fallback на более дешевые модели с большим context window.

**5. Параллелизм + Rate Limits**
2 батча параллельно — оптимальный баланс. Соблюдение rate limits (0.5 req/sec) критично для стабильности.

## Заключение: O(1) на батч vs O(n) на курс

Per-batch архитектура превращает экспоненциальную проблему в линейную.

**Результат**:
- **Неограниченный размер курса**: 8 разделов или 200 — без разницы, система справляется
- **Линейная стоимость**: N разделов = N × $0.084 (предсказуемая экономика)
- **95%+ success rate**: изоляция батчей гарантирует надежность
- **Адаптивный RAG**: 0-40K токенов в зависимости от доступного бюджета
- **Gemini fallback**: автоматическое переключение при overflow с экономией 97%

Если строишь систему генерации контента на LLM — задумайся о per-batch архитектуре. Простота, масштабируемость, предсказуемость. Именно то, что нужно для продакшена.

---

## Дисклеймер: ожидаемая критика

Понимаю, что эта статья вызовет pushback у части разработчиков. "Слишком много API вызовов", "Можно оптимизировать через streaming", "LLM справятся с nested JSON, если правильно настроить prompt".

Моя позиция: **я предпочитаю простоту и надежность оптимизации ради оптимизации**.

**Простота**: SECTIONS_PER_BATCH = 1 проще понять, проще отладить, проще масштабировать.
**Надежность**: 95%+ success rate против 45% — разница очевидна.
**Масштабируемость**: линейная стоимость против экспоненциальной — выбор понятен.

Если не согласны — отлично. Реализуйте свой подход. Если получите 95%+ success rate с SECTIONS_PER_BATCH = 5 или streaming — поделитесь опытом. Я с радостью пересмотрю свою позицию на основе технических аргументов, а не теоретических предположений.

---

## Контакты и обратная связь

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/maslennikovigor
Заходите, читайте мои мысли и статьи. Пишу нечасто, но метко.

**Прямой контакт**: https://t.me/maslennikovig
Нужно поговорить? Пишите напрямую. Всегда рад общению.

### 💬 Обратная связь: открыт на максимум

**Мне интересно услышать**:
- **Критика** — что не так с этим подходом? Где слабые места?
- **Идеи** — какие фичи добавить? Чего не хватает?
- **Предложения** — как улучшить, оптимизировать, рефакторить систему?
- **Вопросы** — что непонятно? Спрашивайте.

**Каналы для обратной связи**:
- **GitHub Issues**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/issues (для багов, фич)
- **GitHub Discussions**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/discussions (для идей, вопросов)
- **Telegram**: https://t.me/maslennikovig (для прямого общения)

**Тон**: максимально открыт к конструктивному диалогу. Без эго, просто хочу сделать систему лучше.
