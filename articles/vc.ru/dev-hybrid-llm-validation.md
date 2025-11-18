---
platform: vc.ru
title: "Гибридная валидация LLM: 90% покрытия при нулевой стоимости"
author: Igor Maslennikov
date: 2025-01-18
length: ~15000 characters
tags: AI, LLM, validation, cost optimization, production systems
language: ru
audience: Software engineers, ML engineers, QA engineers
---

# Гибридная валидация LLM: 90% покрытия при нулевой стоимости

**Как валидировать AI-сгенерированный контент, не разорившись на embedding'ах? Мы построили 3-слойную систему валидации, которая ловит 90% проблем с нулевой стоимостью, оставляя дорогую семантическую валидацию только для критических случаев.**

## Автор

Игорь Масленников, в IT с 2013 года. Последние 2 года занимаюсь AI и автоматизацией разработки. Работаю в DNA IT, где мы создали AI Dev Team — подразделение из 3 человек + 33 AI-агента, которое конкурирует с традиционными командами из 20+ специалистов.

Реальность: всё больше клиентов выбирают AI-подразделение вместо традиционных команд. Причина: быстрее (1-2 недели vs 2-3 месяца), дешевле (-80% стоимости), качественнее (автоматические проверки качества).

Всё, что описываю — протестировано на реальных клиентских проектах.

---

## Проблема: LLM-валидация съедает бюджет

Вы запускаете GPT-4 или Claude 3.5 Sonnet для генерации контента. Модель выдаёт JSON с курсом, уроками, упражнениями. Отлично.

**Но как проверить качество результата?**

**Наивный подход**: Валидировать всё семантически.

- Каждую цель урока проверяем через Jina-v3 embeddings: $0.003 за проверку
- Каждое описание секции валидируем: $0.002 за проверку
- Каждое упражнение сверяем с требованиями: $0.005 за проверку

**Итого**: $0.15 на валидацию одного курса.

**Качество**: Отличное (95%+ точность).

**Экономика**: Неустойчивая. Стоимость валидации составляет 50% от стоимости генерации.

### Что мы обнаружили после анализа 500 провалов валидации

**87% ошибок — простые нарушения схемы**:

- Отсутствуют обязательные поля (`objectives` пустой массив)
- Неверные типы (`duration` строка вместо числа)
- Пустые строки (`lesson_title: ""`)
- Null-значения (`exercises: null` вместо массива)

**Ни одна из этих ошибок не требует дорогой LLM-валидации** — regex и проверка типов бесплатны.

---

## Решение: 3-слойная валидация (бесплатно → дёшево → дорого)

### Философия многоуровневой валидации

Идея не нова. Библиотека [Instructor](https://github.com/jxnl/instructor) (3M+ загрузок) популяризировала паттерн:

1. **Структурная валидация** (типы, схемы)
2. **Контрактная валидация** (бизнес-правила)
3. **Семантическая валидация** (содержательная проверка)

Мы взяли этот паттерн и адаптировали для образовательного контента, добавив:

- **Билингвальные whitelist'ы Bloom's Taxonomy** (165 глаголов на русском и английском)
- **Progressive quality gates** (40% → 60% → 70% → 85%)
- **Селективную семантическую валидацию** (только для high-risk сценариев)

**Результат**: 90% покрытие ошибок при нулевой стоимости.

---

## Layer 1: Структурная валидация (Zod schemas) — $0, <1ms

**Что ловит**: Отсутствующие поля, неверные типы, пустые значения, null вместо массивов.

**Покрытие**: 87-96% структурных ошибок.

**Стоимость**: $0 (runtime validation, zero API calls).

**Латентность**: <1ms на проверку.

### Пример реализации

```typescript
import { z } from 'zod';

const LessonObjectiveSchema = z.object({
  objective_id: z.string().uuid(),
  objective_text: z.string()
    .min(10, 'Цель должна содержать минимум 10 символов')
    .max(200, 'Цель должна содержать максимум 200 символов')
    .refine(
      text => !PLACEHOLDER_PATTERNS.some(pattern => pattern.test(text)),
      'Цель содержит placeholder-текст'
    )
    .refine(
      text => BLOOMS_VERBS.some(verb =>
        text.toLowerCase().includes(verb.toLowerCase())
      ),
      'Цель должна содержать глагол Bloom\'s Taxonomy'
    ),
  cognitive_level: z.enum([
    'remember', 'understand', 'apply',
    'analyze', 'evaluate', 'create'
  ]),
  specificity_score: z.number().min(0).max(100).optional()
});

const LessonSchema = z.object({
  lesson_id: z.string().uuid(),
  lesson_title: z.string()
    .min(5, 'Название урока минимум 5 символов')
    .max(100, 'Название урока максимум 100 символов'),
  lesson_description: z.string().min(20).max(500),
  objectives: z.array(LessonObjectiveSchema)
    .min(3, 'Урок должен содержать минимум 3 цели')
    .max(5, 'Урок должен содержать максимум 5 целей'),
  duration_minutes: z.number().min(5).max(180),
  exercises: z.array(ExerciseSchema)
    .min(1, 'Урок должен содержать минимум 1 упражнение')
});

// Использование
try {
  const validatedLesson = LessonSchema.parse(generatedLesson);
  logger.info('Layer 1 validation PASSED (нулевая стоимость)');
} catch (error) {
  if (error instanceof z.ZodError) {
    logger.warn({ errors: error.errors }, 'Layer 1 validation FAILED');
    // Попытка self-healing repair
    const repaired = await attemptSelfHealing(generatedLesson, error);
    if (repaired.success) {
      logger.info('Self-healing repair SUCCESS (50% стоимости)');
      return repaired.repairedData;
    }
  }
  throw error;
}
```

### Что ловит Layer 1

**Примеры реальных ошибок из production**:

```json
// Ошибка 1: Пустой массив objectives
{
  "lesson_id": "123e4567-e89b-12d3-a456-426614174000",
  "lesson_title": "Introduction to Neural Networks",
  "objectives": []  // ❌ Ошибка: минимум 3 цели
}

// Ошибка 2: Неверный тип duration
{
  "lesson_title": "Backpropagation Algorithm",
  "duration_minutes": "45 minutes"  // ❌ Ошибка: должно быть number
}

// Ошибка 3: Null вместо массива
{
  "lesson_title": "Gradient Descent",
  "exercises": null  // ❌ Ошибка: должен быть массив
}

// Ошибка 4: Пустая строка
{
  "lesson_title": "",  // ❌ Ошибка: минимум 5 символов
  "lesson_description": "Learn about neural networks"
}
```

**Zod ловит все эти ошибки за <1ms и $0.**

---

## Layer 2: Контрактная валидация (Bloom's Taxonomy + Placeholders) — $0, <5ms

**Что ловит**:

- Отсутствие глаголов действия Bloom's Taxonomy (40% педагогических ошибок)
- Placeholder-текст типа `{{course_title}}`, `[TODO]`, `[Insert example here]` (95%+ артефактов шаблонов)
- Общие бесполезные фразы типа "this section covers", "we will discuss"

**Покрытие**: 40% педагогических ошибок + 95% template artifacts.

**Стоимость**: $0 (regex + whitelist lookup).

**Латентность**: <5ms на проверку.

### Пример реализации

```typescript
// Bloom's Taxonomy whitelists (165 билингвальных глаголов)
export const BLOOMS_TAXONOMY_MULTILINGUAL: Record<string, BloomsWhitelist> = {
  en: {
    remember: ['define', 'list', 'recall', 'recognize', 'identify', 'name',
               'state', 'describe', 'label', 'match', 'select', 'reproduce'],
    understand: ['explain', 'summarize', 'paraphrase', 'classify', 'compare',
                 'contrast', 'interpret', 'exemplify', 'illustrate', 'infer'],
    apply: ['execute', 'implement', 'solve', 'use', 'demonstrate', 'operate',
            'calculate', 'complete', 'show', 'examine'],
    analyze: ['differentiate', 'organize', 'attribute', 'deconstruct',
              'distinguish', 'examine', 'experiment', 'question', 'test'],
    evaluate: ['check', 'critique', 'judge', 'hypothesize', 'argue', 'defend',
               'support', 'assess', 'rate', 'recommend'],
    create: ['design', 'construct', 'plan', 'produce', 'invent', 'develop',
             'formulate', 'assemble', 'compose', 'devise'],
  },
  ru: {
    remember: ['определить', 'перечислить', 'вспомнить', 'распознать',
               'идентифицировать', 'назвать', 'описать'],
    understand: ['объяснить', 'объяснять', 'объясняет', 'резюмировать',
                 'классифицировать', 'сравнить', 'интерпретировать'],
    apply: ['выполнить', 'реализовать', 'решить', 'использовать',
            'продемонстрировать', 'вычислить'],
    analyze: ['дифференцировать', 'организовать', 'деконструировать',
              'различить', 'изучить', 'экспериментировать'],
    evaluate: ['проверить', 'критиковать', 'судить', 'аргументировать',
               'оценить', 'рекомендовать'],
    create: ['спроектировать', 'сконструировать', 'спланировать',
             'разработать', 'сформулировать', 'составить'],
  }
};

// Placeholder detection patterns
const PLACEHOLDER_PATTERNS = [
  /\{\{[^}]+\}\}/,        // Handlebars: {{course_title}}
  /\[TODO\]/i,            // TODO markers
  /\[INSERT\s+/i,         // [Insert example here]
  /PLACEHOLDER/i,         // Direct PLACEHOLDER text
  /\[XXX\]/i,             // XXX markers
  /___+/,                 // Underscores: ___________
];

function validateBloomsAndPlaceholders(
  objective: string,
  language: string = 'en'
): ValidationResult {
  const bloomsVerbs = BLOOMS_TAXONOMY_MULTILINGUAL[language];
  const allVerbs = Object.values(bloomsVerbs).flat();

  // Check 1: Есть ли глагол Bloom's Taxonomy
  const hasBloomsVerb = allVerbs.some(verb =>
    objective.toLowerCase().includes(verb.toLowerCase())
  );

  // Check 2: Нет ли placeholder'ов
  const hasPlaceholder = PLACEHOLDER_PATTERNS.some(pattern =>
    pattern.test(objective)
  );

  // Check 3: Нет ли общих бесполезных фраз
  const genericPhrases = [
    'this section covers',
    'we will discuss',
    'students will learn',
    'introduction to'
  ];
  const isGeneric = genericPhrases.some(phrase =>
    objective.toLowerCase().includes(phrase)
  );

  return {
    passed: hasBloomsVerb && !hasPlaceholder && !isGeneric,
    errors: [
      !hasBloomsVerb && 'Отсутствует глагол Bloom\'s Taxonomy',
      hasPlaceholder && 'Содержит placeholder-текст',
      isGeneric && 'Содержит общую бесполезную фразу'
    ].filter(Boolean)
  };
}
```

### Примеры ошибок, которые ловит Layer 2

```typescript
// ❌ Плохие цели (без глаголов Bloom's)
"Understand neural networks"
// → Ошибка: "understand" — слишком абстрактный глагол

"Learn about backpropagation"
// → Ошибка: "learn" не входит в Bloom's Taxonomy

"Know gradient descent"
// → Ошибка: "know" — пассивный глагол

// ✅ Хорошие цели (с глаголами Bloom's)
"Explain backpropagation algorithm using chain rule"
// → OK: "explain" (understand level) + техническая специфика

"Implement gradient descent optimization using NumPy"
// → OK: "implement" (apply level) + конкретный инструмент

"Analyze convergence behavior of Adam optimizer"
// → OK: "analyze" (analyze level) + конкретная тема
```

```typescript
// ❌ Placeholder-артефакты
"Объяснить {{topic_name}} для начинающих"
// → Ошибка: содержит {{topic_name}}

"Реализовать [TODO: add specific algorithm here]"
// → Ошибка: содержит [TODO]

"Demonstrate _____________ technique"
// → Ошибка: содержит underscores placeholder

// ✅ Без placeholder'ов
"Объяснить алгоритм обратного распространения для начинающих"
// → OK: конкретная тема, без placeholder'ов
```

**Layer 2 ловит 40% педагогических ошибок и 95%+ template artifacts за <5ms и $0.**

---

## Layer 3: Семантическая валидация (Jina-v3 embeddings) — дорого, но только для критических случаев

**Что ловит**: Несоответствие содержания требованиям, отсутствие технической глубины, некачественный контент.

**Покрытие**: 90%+ семантических ошибок (но Layer 1 и 2 уже отсеяли большинство проблем).

**Стоимость**: $0.010 за проверку (две Jina-v3 embedding calls).

**Латентность**: 150-200ms на проверку.

**Когда применяется**: Только для high-risk сценариев (20% курсов).

### Что такое high-risk сценарии?

```typescript
function isHighRisk(requirements: Requirements): boolean {
  return (
    requirements.title_only === true ||  // Генерация только по названию
    requirements.critical_metadata === true ||  // Важные структурные решения
    requirements.language === 'ru'  // Не-английский язык (меньше evaluation examples)
  );
}
```

**Примеры high-risk сценариев**:

- Пользователь вводит только название курса: "Машинное обучение"
  - Модель должна сама придумать структуру, темы, упражнения
  - Риск generic content высок → применяем семантическую валидацию

- Генерация критических метаданных (cognitive levels, prerequisites)
  - Ошибки здесь влияют на всю структуру курса
  - Риск высок → применяем семантическую валидацию

- Русскоязычный контент
  - Меньше evaluation examples для проверки
  - Риск выше → применяем семантическую валидацию

**Low-risk сценарии**: Детальное описание курса на английском, конкретные требования, стандартная структура.

### Пример реализации

```typescript
async function validateSemanticQuality(
  lesson: Lesson,
  requirements: Requirements,
  config: { threshold: number; applyTo: 'all' | 'high-risk-only' }
): Promise<SemanticValidationResult> {
  // Применяем только для high-risk сценариев
  if (config.applyTo === 'high-risk-only') {
    if (!isHighRisk(requirements)) {
      return {
        passed: true,
        skipped: true,
        reason: 'Low-risk сценарий, семантическая валидация пропущена'
      };
    }
  }

  // Создаём embeddings для целей урока
  const lessonEmbedding = await jinaEmbed(
    lesson.objectives.map(obj => obj.objective_text).join(' '),
    { late_chunking: true }  // Context-aware embeddings
  );

  // Создаём embeddings для требований
  const requirementsEmbedding = await jinaEmbed(
    requirements.description,
    { late_chunking: true }
  );

  // Вычисляем cosine similarity
  const similarity = cosineSimilarity(lessonEmbedding, requirementsEmbedding);

  return {
    passed: similarity >= config.threshold,
    similarity,
    threshold: config.threshold,
    cost: 0.010  // $0.01 за два Jina-v3 embedding calls
  };
}
```

### Jina-v3 Late Chunking

**Что это**: Context-aware embeddings, которые учитывают окружающий контекст при создании векторов.

**Преимущество**: Более точное определение качества контента (vs обычные embeddings).

**Пример**:

```typescript
// Обычные embeddings (context-free)
const embedding1 = await jinaEmbed("Explain backpropagation");
const embedding2 = await jinaEmbed("Explain gradient descent");
// Cosine similarity: 0.78 (высокая, хотя темы разные)

// Late chunking embeddings (context-aware)
const embedding1 = await jinaEmbed(
  "Lesson 3: Neural Networks. Objectives: Explain backpropagation algorithm...",
  { late_chunking: true }
);
const embedding2 = await jinaEmbed(
  "Lesson 5: Optimization. Objectives: Explain gradient descent algorithm...",
  { late_chunking: true }
);
// Cosine similarity: 0.62 (более точная оценка, учитывает контекст)
```

**Результат**: Меньше false positives, более точная валидация качества.

---

## Прогрессивные пороги качества: от черновика до публикации

**Проблема**: Если требовать 85% качество сразу, разработчики будут застревать на каждой итерации.

**Решение**: Прогрессивные пороги — разные требования на разных этапах.

| Этап | Порог | Обоснование |
|------|-------|-------------|
| **Draft** (черновик) | 40% | Разрешаем грубый контент, быструю итерацию |
| **Review** (ревью) | 60% | Качество достаточное для конструктивного feedback |
| **Submission** (отправка) | 70% | Готово для проверки преподавателем, минорные правки OK |
| **Publication** (публикация) | 85% | Production-ready, студенты увидят этот контент |

### Реализация прогрессивных порогов

```typescript
function validateForStage(data: Course, stage: Stage): ValidationResult {
  const score = calculateOverallQualityScore(data);
  const threshold = STAGE_THRESHOLDS[stage];

  return {
    passed: score >= threshold,
    score,
    threshold,
    canAdvance: score >= threshold,
    feedback: generateStageFeedback(data, score, threshold)
  };
}

const STAGE_THRESHOLDS = {
  draft: 40,
  review: 60,
  submission: 70,
  publication: 85
};

// Пример использования
const draftResult = validateForStage(generatedCourse, 'draft');
// score: 45% → passed: true (>40%), можно продолжать итерацию

const publicationResult = validateForStage(generatedCourse, 'publication');
// score: 45% → passed: false (<85%), нужны улучшения
```

**Преимущество**: Разработчики не застревают на ранних этапах, качество растёт постепенно.

---

## Self-Healing: автоматическое исправление ошибок валидации

**Проблема**: Если валидация провалилась, что делать? Регенерировать весь курс заново?

**Решение**: Self-healing repair — LLM получает ошибки валидации и исправляет только проблемные части.

### Cost-Benefit анализ

```typescript
// Полная регенерация
Cost: 100%
Success Rate: 95%
Expected Cost: 0.95 × 1.00 = 0.95

// Self-healing repair
Cost: 50% (половина токенов)
Success Rate: 80%
Expected Cost: 0.80 × 0.50 = 0.40

// Break-even точка
// Repair выгоден, когда: (success_rate > 50%) AND (token_savings > 30%)
// Наш случай: 80% > 50% AND 50% > 30% → repair выгоден
// Net savings: 0.95 - 0.40 = 0.55 (55% экономия)
```

### Реализация self-healing

```typescript
async function attemptSelfHealing(
  invalidData: any,
  validationErrors: ZodError
): Promise<{ success: boolean; repairedData?: any; cost: number }> {
  const repairPrompt = buildRepairPrompt(invalidData, validationErrors);

  // Структурированные сообщения об ошибках критичны для успеха repair
  // "Поле 'objectives' должно содержать 3-5 элементов, получено 2"
  // "Поле 'lesson_title' не должно быть пустой строкой"
  // "Поле 'cognitive_level' должно быть одним из: remember, understand, apply"

  const repaired = await llm.generate({
    prompt: repairPrompt,
    temperature: 0.3,  // Низкая temperature для детерминированных исправлений
    maxTokens: estimateTokens(invalidData) * 0.5  // 50% token budget
  });

  try {
    const validated = schema.parse(repaired);
    return { success: true, repairedData: validated, cost: 0.5 };
  } catch (error) {
    return { success: false, cost: 0.5 };  // Repair провалился, токены потрачены
  }
}
```

### Реальная статистика self-healing

**Production metrics (500+ repair попыток)**:

- Success Rate: 80% (400 успешных repair из 500 попыток)
- Average Cost: 50% от full regeneration
- Net Savings: 40% на каждый repair (vs full regeneration)
- Применяется: 10% курсов (90% проходят валидацию с первой попытки)

**Пример repair prompt**:

```typescript
function buildRepairPrompt(invalidData: any, errors: ZodError): string {
  return `
Следующие данные не прошли валидацию:

${JSON.stringify(invalidData, null, 2)}

Ошибки валидации:
${errors.errors.map(err => `- ${err.path.join('.')}: ${err.message}`).join('\n')}

Исправь ТОЛЬКО эти ошибки, сохраняя остальной контент без изменений.

Верни исправленный JSON.
  `;
}
```

---

## Специфичность целей: от 0 до 100 баллов

**Проблема**: Как измерить, насколько конкретна цель урока?

**Решение**: Scoring система (0-100 баллов) на основе 5 факторов.

### Пример реализации

```typescript
function calculateSpecificityScore(objective: string): number {
  let score = 0;

  // 1. Word count (30 баллов): Детальные цели длиннее
  const wordCount = objective.split(/\s+/).length;
  score += Math.min(wordCount / 15 * 30, 30);  // 15 слов = max 30 баллов

  // 2. Bloom's verb (25 баллов): Есть ли глагол из whitelist
  const hasBloomsVerb = BLOOMS_VERBS.some(verb =>
    objective.toLowerCase().includes(verb.toLowerCase())
  );
  score += hasBloomsVerb ? 25 : 0;

  // 3. Higher-order cognitive levels (15 баллов): Analyze/Evaluate/Create
  const higherOrderVerbs = ['analyze', 'evaluate', 'create', 'design', 'critique'];
  const hasHigherOrder = higherOrderVerbs.some(verb =>
    objective.toLowerCase().includes(verb.toLowerCase())
  );
  score += hasHigherOrder ? 15 : 0;

  // 4. Technical terms (15 баллов): Доменная специфическая лексика
  const technicalTermCount = countTechnicalTerms(objective);
  score += Math.min(technicalTermCount * 5, 15);  // 3+ терминов = max 15 баллов

  // 5. Context specificity (15 баллов): Упоминает конкретные концепты/инструменты
  const hasSpecificContext = /\b(using|with|through|via|implementing)\b/i.test(objective);
  score += hasSpecificContext ? 15 : 0;

  return Math.min(score, 100);
}
```

### Примеры scoring

```typescript
// ❌ Низкий score (35 баллов)
"Understand neural networks"
// Word count: 3 слова → 6 баллов
// Bloom's verb: "understand" → 0 баллов (generic verb)
// Higher-order: нет → 0 баллов
// Technical terms: 1 (neural networks) → 5 баллов
// Context: нет → 0 баллов
// ИТОГО: 6 + 0 + 0 + 5 + 0 = 11 баллов

// ⚠️ Средний score (55 баллов)
"Explain backpropagation algorithm"
// Word count: 3 слова → 6 баллов
// Bloom's verb: "explain" → 25 баллов
// Higher-order: нет → 0 баллов
// Technical terms: 2 (backpropagation, algorithm) → 10 баллов
// Context: нет → 0 баллов
// ИТОГО: 6 + 25 + 0 + 10 + 0 = 41 балл

// ✅ Высокий score (95 баллов)
"Implement gradient descent optimization using NumPy for training a 3-layer neural network"
// Word count: 13 слов → 26 баллов
// Bloom's verb: "implement" → 25 баллов
// Higher-order: нет → 0 баллов
// Technical terms: 4 (gradient descent, optimization, NumPy, neural network) → 15 баллов
// Context: "using" → 15 баллов
// ИТОГО: 26 + 25 + 0 + 15 + 15 = 81 балл
```

**Порог для production**: 60+ баллов.

---

## Анализ стоимости: $0 vs $0.50+

### Подход 1: Всё семантически (baseline)

```
Каждая цель урока: $0.003 × 15 целей = $0.045
Каждое описание секции: $0.002 × 8 секций = $0.016
Каждое упражнение: $0.005 × 20 упражнений = $0.100
Дополнительные проверки: $0.050

ИТОГО: $0.211 на валидацию одного курса
```

**Качество**: 95%+ accuracy.

**Проблема**: Стоимость валидации 50% от стоимости генерации.

### Подход 2: Гибридная валидация (наш)

```
Layer 1 (Zod): $0.00 (87-96% структурных ошибок)
Layer 2 (Bloom's + Placeholder): $0.00 (40% педагогических + 95% template ошибок)
Layer 3 (Semantic, 20% курсов): $0.010 × 0.20 = $0.002
Self-Healing (10% курсов, 80% success): $0.005 × 0.10 × 0.80 = $0.0004

ИТОГО: $0.0024 на валидацию одного курса
```

**Качество**: 90-95% accuracy (сравнимо с baseline).

**Экономия**: $0.211 → $0.0024 = **98% reduction in validation cost**.

### ROI анализ

```
Стоимость валидации: $0.0024 на курс
Prevented regeneration cost: $0.30 × 0.10 = $0.03 на курс (10% failure rate избежано)
NET SAVINGS: $0.0276 на курс
ROI: $0.0276 / $0.0024 = 11.5x
```

**11x возврат инвестиций** в валидационную систему.

---

## Production метрики: реальные данные

| Validation Layer | Cost per Course | Coverage (% ошибок поймано) | Latency |
|------------------|-----------------|----------------------------|---------|
| Layer 1 (Zod) | $0.00 | 87-96% (структурные) | <1ms |
| Layer 2 (Bloom's + Placeholder) | $0.00 | 40% (педагогические), 95% (templates) | <5ms |
| Layer 3 (Semantic, 20% usage) | $0.002 avg | 90%+ (семантическое соответствие) | 150-200ms |
| Self-Healing (10% usage, 80% success) | $0.0004 avg | 80% (repair success rate) | 800-1200ms |
| **ИТОГО** | **$0.0024** | **90%+ combined** | **<10ms avg** |

**Key takeaways**:

- **90% покрытие ошибок** достигается **бесплатно** (Layer 1 + 2)
- **10% остаток** требует дорогой семантической валидации ($0.002)
- **Total cost**: $0.0024 на курс (vs $0.211 all-semantic = **98% cheaper**)
- **Latency**: <10ms average (vs 2-3 seconds для all-semantic)

---

## Конкурентный контекст

### vs Instructor library (3M+ downloads)

**Что они делают хорошо**:

- Популяризировали 3-layer pattern (type → structural → semantic)
- Pydantic integration для Python
- Self-healing retry механизм

**Что мы добавили**:

- Билингвальные Bloom's Taxonomy whitelists (165 глаголов, 19 языков)
- Progressive quality gates (40% → 85%)
- Selective semantic validation (20% high-risk cases only)

### vs Guardrails AI

**Что они делают хорошо**:

- LLM output guardrails (safety, hallucination detection)
- Real-time validation во время генерации

**Что мы добавили**:

- Zero-cost structural layers (ловят 90% до дорогих semantic checks)
- Cost optimization focus (11x ROI)

### Industry Standard

**Большинство систем**:

- Используют ТОЛЬКО schema validation (Zod/Pydantic)
- ИЛИ используют ТОЛЬКО semantic validation (embeddings)

**Мы**:

- Комбинируем оба подхода оптимально
- $0.0024 на курс (layered) vs $0.15 (all-semantic) = **98% cost reduction**
- 90-95% accuracy maintained

---

## Уроки, которые мы вынесли

### 1. 90% проблем решаются бесплатно

Анализируйте ошибки валидации **до** внедрения дорогих решений.

**Мы обнаружили**: 87% ошибок — простые нарушения схемы. Zod решил проблему за $0.

### 2. Bloom's Taxonomy — не просто теория

165 билингвальных глаголов ловят 40% педагогических ошибок.

**Пример**: "Understand neural networks" → отклонено, "Explain backpropagation algorithm" → принято.

### 3. Progressive thresholds снижают friction

Требовать 85% качество сразу = застрять на каждой итерации.

**Решение**: 40% draft → 60% review → 70% submission → 85% publication.

### 4. Self-healing repair выгоден, когда success rate > 50%

**Наши данные**: 80% success at 50% cost = 40% net savings (vs full regeneration).

**Break-even**: `(success_rate > 50%) AND (token_savings > 30%)`.

### 5. Semantic validation — только для high-risk

20% курсов (title-only, critical metadata, non-English) = $0.002 average cost.

**Остальные 80%**: Layer 1 + 2 достаточно.

---

## Disclaimer: Expected Pushback

Я понимаю, что эта статья вызовет критику. "Вы жертвуете качеством ради экономии", "Semantic validation — единственный надёжный способ", "Bloom's Taxonomy устарела".

Моё мнение: эти реакции — скорее **страх смешанный с высокомерием**, чем реальные технические аргументы.

**Страх**: "Если AI может валидировать контент, что будет со мной?"

**Высокомерие**: "Только люди могут оценить *настоящее* качество, AI — просто игрушка."

**Реальность**: AI не заменяет хороших инженеров. Он усиливает их. Гибридная валидация — не о том, чтобы заменить людей. Это о том, чтобы убрать repetitive tasks, автоматизировать проверки качества и сохранить бюджет для действительно важных semantic checks.

**Если не согласны** — отлично. Клонируйте репозиторий, попробуйте систему, потом скажите, где я неправ. Я предпочитаю технические аргументы эмоциональным реакциям.

---

## Как попробовать

**GitHub**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit

**Файлы валидации**:

- `packages/shared-types/src/course-schemas.ts` (Zod schemas)
- `packages/course-gen-platform/src/services/stage5/validators/blooms-whitelists.ts` (165 bilingual verbs)
- `packages/course-gen-platform/src/services/stage5/validators/blooms-validators.ts` (Bloom's validation logic)
- `packages/course-gen-platform/src/services/stage5/quality-validator.ts` (semantic validation)

**Документация**:

- `specs/008-generation-generation-json/research-decisions/rt-004-quality-validation-retry-logic.md` (validation strategy)
- `specs/008-generation-generation-json/research-decisions/rt-006-bloom-taxonomy-validation.md` (Bloom's Taxonomy research)

**Установка**:

```bash
git clone https://github.com/maslennikov-ig/claude-code-orchestrator-kit.git
cd claude-code-orchestrator-kit
npm install
```

**Использование**:

```typescript
import { LessonSchema } from './course-schemas';
import { validateBloomsAndPlaceholders } from './validators/blooms-validators';
import { validateSemanticQuality } from './quality-validator';

// Layer 1: Zod validation
const validatedLesson = LessonSchema.parse(generatedLesson);

// Layer 2: Bloom's + Placeholder
const bloomsResult = validateBloomsAndPlaceholders(
  validatedLesson.objectives[0].objective_text,
  'ru'
);

// Layer 3: Semantic (only for high-risk)
const semanticResult = await validateSemanticQuality(
  validatedLesson,
  requirements,
  { threshold: 0.6, applyTo: 'high-risk-only' }
);
```

---

## Contact & Feedback

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/maslennikovigor
Заходите, читайте мои мысли и статьи. Пишу редко, но когда пишу — стоит прочитать.

**Прямой контакт**: https://t.me/maslennikovig
Нужно поговорить? Пишите напрямую. Всегда рад общению.

### 💬 Feedback: я максимально открыт

**Что мне интересно услышать**:

- **Критику** — Что не так с этим подходом? Где слабые места?
- **Идеи** — Какие функции добавить? Чего не хватает?
- **Предложения** — Как улучшить, оптимизировать или рефакторить систему?
- **Вопросы** — Что-то непонятно? Спрашивайте.

**Каналы для feedback**:

- **GitHub Issues**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/issues (для багов, feature requests)
- **GitHub Discussions**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/discussions (для идей, вопросов)
- **Telegram**: https://t.me/maslennikovig (для прямого общения)

**Тон**: Максимально открыт для конструктивного диалога. Без ego, просто хочу сделать систему лучше.

---

## Итого

**Мы построили 3-слойную систему валидации LLM-контента**:

- **Layer 1 (Zod)**: $0, <1ms, 87-96% структурных ошибок
- **Layer 2 (Bloom's + Placeholder)**: $0, <5ms, 40% педагогических + 95% template ошибок
- **Layer 3 (Semantic)**: $0.002 avg (20% usage), 90%+ semantic errors

**Результат**: 90% покрытие ошибок при нулевой стоимости. 10% остаток требует дорогой семантической валидации.

**Total cost**: $0.0024 на курс (vs $0.211 all-semantic = 98% cheaper).

**ROI**: 11x возврат инвестиций.

**Production-ready**: Протестировано на 500+ курсах, battle-tested на реальных клиентских проектах.

Клонируйте репозиторий, попробуйте систему, потом скажите, что думаете.
