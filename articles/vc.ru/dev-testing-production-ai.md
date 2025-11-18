---
platform: vc.ru
title: "Как тестировать продакшн AI-систему: 397 тестов, 92% покрытие, детерминизм из недетерминизма"
author: Igor Maslennikov
date: 2025-11-18
length: 15847 characters
tags: testing, AI, LLM, production, coverage, testcontainers, vitest
language: ru
audience: Software Engineers, QA Engineers, DevOps
---

# Как тестировать продакшн AI-систему: 397 тестов, 92% покрытие, детерминизм из недетерминизма

Я последние 2 года занимаюсь разработкой AI-платформы для генерации образовательных курсов. В IT с 2013 года, руковожу AI Dev Team в компании DNA IT. За это время написал 397 тестовых файлов на 139 исходных файлов — покрытие 92%. Это не про красивые метрики ради слайдов на конференции. Это про реальную продакшн-систему, которая генерирует 10,000+ курсов в месяц и не может упасть.

Главная проблема: **как тестировать систему, которая каждый раз выдаёт разные результаты?** Один и тот же промпт → LLM возвращает разный контент. Классические unit-тесты с `expect(result).toBe(expectedValue)` здесь не работают. Нужна другая стратегия.

В этой статье я расскажу, как мы решили проблему недетерминизма в тестировании AI-систем, добились 92% покрытия и построили многослойную пирамиду тестирования: 195 unit-тестов, 130 интеграционных, 72 E2E. Всё на реальных примерах кода, без воды.

---

## Контекст: Почему тестирование AI-систем — это боль

Традиционные системы детерминированы:
```typescript
function add(a: number, b: number): number {
  return a + b;
}

// Тест простой:
expect(add(2, 3)).toBe(5); // Всегда 5
```

AI-системы недетерминированны:
```typescript
async function generateCourseMetadata(title: string): Promise<Metadata> {
  return await llm.generate({ prompt: `Analyze course: ${title}` });
}

// Тест невозможен классическим способом:
const result = await generateCourseMetadata('Neural Networks');
expect(result).toBe(???); // Что ожидать? Каждый раз разный результат!
```

**Проблема №1**: LLM возвращает разные значения при одинаковом промпте.
**Проблема №2**: Сложные многоэтапные пайплайны (5 фаз генерации, каждая зависит от предыдущей).
**Проблема №3**: Распределённая архитектура (job queue, FSM, БД, Redis, внешние API).
**Проблема №4**: Как проверить качество контента? Не только структуру, но и смысл.

Индустрия обычно идёт двумя путями:
1. **Вообще не тестируют AI-логику** — покрытие <60%, надеются на ручные проверки.
2. **Тестируют только вспомогательный код** (валидаторы, парсеры) — AI-генерация остаётся чёрным ящиком.

Мы выбрали третий путь: **тестируем всё, включая AI-логику**, но используем правильные метрики и стратегии для недетерминизма.

---

## Философия: Многослойная валидация вместо одного теста

Наша стратегия базируется на простом принципе: **если результат недетерминирован по контенту, проверяй структуру, семантику и контракты.**

**Три уровня валидации**:

1. **Структурная валидация** (дёшево, детерминированно):
   - Проверяем JSON-схему с Zod
   - Проверяем наличие обязательных полей
   - Проверяем типы данных
   - Проверяем границы значений (3-5 целей, 5-7 уроков и т.д.)

2. **Контрактная валидация** (дёшево, детерминированно):
   - tRPC обеспечивает type-safety между клиентом и сервером
   - Pydantic-валидация на стороне AI-генератора
   - Проверяем соответствие API-контрактам

3. **Семантическая валидация** (дорого, выборочно):
   - Semantic similarity через Jina-v3 embeddings (768-dim)
   - Golden files для критических сценариев
   - Реальные API-вызовы в E2E-тестах

**Ключевая идея**: 90% проблем ловим структурной валидацией (быстро, дёшево). 9% — контрактной валидацией. Только 1% требует семантической проверки (медленно, дорого, но точно).

---

## Архитектура тестирования: Пирамида 195-130-72

### Уровень 1: Unit-тесты (195 файлов, 45 секунд)

**Задача**: Тестировать чистые функции и бизнес-логику в изоляции.
**Подход**: Мокируем все внешние зависимости (LLM, БД, очереди).

**Пример: Тестирование генератора метаданных**

```typescript
// tests/unit/stage5/metadata-generator.test.ts
import { describe, it, expect, vi } from 'vitest';
import { generateMetadata } from '@/services/stage5/metadata-generator';

describe('Metadata Generator', () => {
  it('должен генерировать метаданные с обязательными полями', async () => {
    // Мокируем LLM-ответ (детерминированный результат)
    const mockLLM = vi.fn().mockResolvedValue({
      category: 'technology',
      contextual_language: 'academic_formal',
      topic_analysis: {
        complexity: 'intermediate',
        prerequisites: ['basic programming', 'math fundamentals'],
        learning_outcomes: ['understand neural networks', 'implement backprop']
      },
      recommended_structure: {
        sections: 8,
        lessons_per_section: 5,
        total_duration_hours: 12
      }
    });

    const result = await generateMetadata({
      title: 'Neural Networks',
      description: 'Deep learning course for developers',
      llmClient: mockLLM
    });

    // Проверяем структуру, а не конкретные значения
    expect(result.category).toBeDefined();
    expect(result.contextual_language).toMatch(/^[a-z_]+$/);
    expect(result.topic_analysis.complexity).toMatch(/^(beginner|intermediate|advanced)$/);
    expect(result.recommended_structure.sections).toBeGreaterThanOrEqual(3);
    expect(result.recommended_structure.sections).toBeLessThanOrEqual(12);

    // LLM должен быть вызван с правильными параметрами
    expect(mockLLM).toHaveBeenCalledWith(
      expect.objectContaining({
        prompt: expect.stringContaining('Neural Networks')
      })
    );
  });

  it('должен выбрасывать ошибку при невалидной структуре', async () => {
    const mockLLM = vi.fn().mockResolvedValue({
      category: 'invalid_category', // Нет в enum
      contextual_language: 'formal'
    });

    await expect(
      generateMetadata({
        title: 'Test',
        description: 'Test course',
        llmClient: mockLLM
      })
    ).rejects.toThrow('Invalid category');
  });
});
```

**Что тестируем**:
- ✅ Структура ответа соответствует схеме
- ✅ Валидация входных параметров
- ✅ Обработка ошибок
- ✅ Бизнес-правила (диапазоны значений, enum-ы)

**Что НЕ тестируем**:
- ❌ Реальное качество контента (это в E2E-тестах)
- ❌ Реальные API-вызовы (это в интеграционных тестах)

**Скорость**: 45 секунд на 195 тестов. Параллельное выполнение (4 worker'а), shared fixtures.

---

### Уровень 2: Интеграционные тесты (130 файлов, 4 минуты)

**Задача**: Тестировать взаимодействие компонентов с реальной БД и очередями.
**Подход**: Testcontainers (Docker-контейнеры с PostgreSQL + Redis).

**Зачем Testcontainers?**

Раньше использовали SQLite для тестов. Проблема: PostgreSQL-специфичные фичи (RLS, triggers, RPC functions) не работают в SQLite. Запускать общую PostgreSQL для всех тестов — проблемы с изоляцией и параллельностью.

**Решение**: Каждый тест получает свой Docker-контейнер с чистой БД.

```typescript
// tests/integration/setup.ts
import { GenericContainer, Wait } from 'testcontainers';
import { createClient } from '@supabase/supabase-js';
import type { StartedTestContainer } from 'testcontainers';

let postgresContainer: StartedTestContainer;
let redisContainer: StartedTestContainer;

export async function setupTestContainers() {
  // Запускаем PostgreSQL 15 в Docker
  postgresContainer = await new GenericContainer('postgres:15-alpine')
    .withExposedPorts(5432)
    .withEnvironment({
      POSTGRES_USER: 'test',
      POSTGRES_PASSWORD: 'test',
      POSTGRES_DB: 'courseai_test'
    })
    .withWaitStrategy(Wait.forLogMessage('database system is ready'))
    .start();

  const dbPort = postgresContainer.getMappedPort(5432);
  const dbHost = postgresContainer.getHost();
  const dbUrl = `postgresql://test:test@${dbHost}:${dbPort}/courseai_test`;

  // Применяем миграции Supabase
  const supabase = createClient(dbUrl, 'anon-key');
  await supabase.rpc('run_migrations'); // Supabase RPC для миграций

  // Запускаем Redis для BullMQ
  redisContainer = await new GenericContainer('redis:7-alpine')
    .withExposedPorts(6379)
    .withWaitStrategy(Wait.forLogMessage('Ready to accept connections'))
    .start();

  const redisPort = redisContainer.getMappedPort(6379);
  const redisHost = redisContainer.getHost();

  // Устанавливаем environment variables для тестов
  process.env.DATABASE_URL = dbUrl;
  process.env.REDIS_URL = `redis://${redisHost}:${redisPort}`;

  console.log(`✅ Testcontainers ready: Postgres ${dbHost}:${dbPort}, Redis ${redisHost}:${redisPort}`);
}

export async function teardownTestContainers() {
  await postgresContainer?.stop();
  await redisContainer?.stop();
}

// Vitest setup
beforeAll(async () => {
  await setupTestContainers();
}, 30_000); // 30 секунд на подъём контейнеров

afterAll(async () => {
  await teardownTestContainers();
});
```

**Преимущества Testcontainers**:
- ✅ **Изоляция**: Каждый тест получает чистую БД, никаких shared state
- ✅ **Параллельность**: Можно запускать тесты параллельно, у каждого свой контейнер
- ✅ **Реальная PostgreSQL**: Тестируем триггеры, RLS, RPC — всё как в проде
- ✅ **Автоматический cleanup**: Контейнеры уничтожаются после тестов

**Пример интеграционного теста: Transactional Outbox**

```typescript
// tests/integration/transactional-outbox.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { createClient } from '@supabase/supabase-js';
import { processOutbox } from '@/orchestrator/outbox-processor';

describe('Transactional Outbox Pattern', () => {
  let supabase: SupabaseClient;

  beforeEach(async () => {
    supabase = createClient(process.env.DATABASE_URL!, 'test-key');
    // Очищаем таблицы перед каждым тестом
    await supabase.from('outbox_events').delete().neq('id', 0);
    await supabase.from('courses').delete().neq('id', 0);
  });

  it('должен атомарно сохранять курс и событие в outbox', async () => {
    // Создаём курс в транзакции
    const { data: course, error } = await supabase.rpc('create_course_atomic', {
      title: 'Test Course',
      status: 'pending'
    });

    expect(error).toBeNull();
    expect(course).toBeDefined();

    // Проверяем, что событие появилось в outbox
    const { data: events } = await supabase
      .from('outbox_events')
      .select('*')
      .eq('aggregate_id', course.id)
      .eq('event_type', 'course.created');

    expect(events).toHaveLength(1);
    expect(events[0].payload).toMatchObject({
      course_id: course.id,
      title: 'Test Course'
    });
  });

  it('должен обрабатывать события из outbox и добавлять в BullMQ', async () => {
    // Вставляем событие в outbox вручную
    await supabase.from('outbox_events').insert({
      event_type: 'course.created',
      aggregate_id: 'test-123',
      payload: { course_id: 'test-123' }
    });

    // Запускаем outbox processor
    const processed = await processOutbox();

    expect(processed).toBe(1);

    // Проверяем, что событие помечено как processed
    const { data: event } = await supabase
      .from('outbox_events')
      .select('processed_at')
      .eq('aggregate_id', 'test-123')
      .single();

    expect(event.processed_at).not.toBeNull();
  });

  it('должен откатывать транзакцию при ошибке', async () => {
    // Симулируем ошибку валидации
    const { error } = await supabase.rpc('create_course_atomic', {
      title: '', // Пустой заголовок — ошибка валидации
      status: 'pending'
    });

    expect(error).toBeDefined();

    // Проверяем, что НИ курс, НИ событие не сохранились
    const { data: courses } = await supabase.from('courses').select('*');
    const { data: events } = await supabase.from('outbox_events').select('*');

    expect(courses).toHaveLength(0);
    expect(events).toHaveLength(0);
  });
});
```

**Что тестируем**:
- ✅ Транзакционность (атомарность операций)
- ✅ Supabase RPC functions
- ✅ PostgreSQL triggers
- ✅ Redis/BullMQ интеграцию
- ✅ Обработка ошибок с откатом

**Скорость**: 4 минуты на 130 тестов. Параллельное выполнение, каждый тест-файл получает свой контейнер.

---

### Уровень 3: E2E-тесты (72 файла, 3 минуты 15 секунд)

**Задача**: Тестировать полные пайплайны с реальными LLM API-вызовами.
**Подход**: Реальные API, семантическая валидация, golden files.

**Проблема**: LLM возвращает разный контент. Как проверить, что генерация качественная?

**Решение 1: Semantic Similarity (семантическое сходство)**

Вместо точного совпадения текста проверяем семантическую близость через embeddings.

```typescript
// tests/e2e/stage5-generation.test.ts
import { describe, it, expect } from 'vitest';
import { generateSection } from '@/services/stage5/section-generator';
import { calculateSemanticSimilarity } from '@/tests/utils/semantic-similarity';
import fs from 'fs/promises';

describe('E2E: Section Generation', () => {
  it('должен генерировать контент семантически близкий к golden file', async () => {
    // Реальный LLM-вызов
    const result = await generateSection({
      title: 'Backpropagation Algorithm',
      description: 'Explain gradient descent and chain rule in neural networks',
      contextual_language: 'academic_formal',
      complexity: 'intermediate'
    });

    // Загружаем эталонный результат
    const goldenFile = await fs.readFile(
      'tests/fixtures/golden/backpropagation-section.json',
      'utf-8'
    );
    const golden = JSON.parse(goldenFile);

    // Проверяем структуру (детерминированно)
    expect(result.lessons).toHaveLength(golden.lessons.length);
    expect(result.section_title).toBeDefined();

    // Проверяем семантическую близость (недетерминированно, но контролируемо)
    const similarity = await calculateSemanticSimilarity(
      result.lessons[0].lesson_content,
      golden.lessons[0].lesson_content
    );

    // Порог 75% — если меньше, значит модель сильно отклонилась от эталона
    expect(similarity).toBeGreaterThan(0.75);

    console.log(`Semantic similarity: ${(similarity * 100).toFixed(1)}%`);
  });
});

// Утилита для расчёта семантического сходства
async function calculateSemanticSimilarity(text1: string, text2: string): Promise<number> {
  // Используем Jina-v3 для embeddings (768-dim, late chunking)
  const embedding1 = await jinaEmbed(text1, { late_chunking: true });
  const embedding2 = await jinaEmbed(text2, { late_chunking: true });

  // Cosine similarity
  const dotProduct = embedding1.reduce((sum, val, i) => sum + val * embedding2[i], 0);
  const magnitude1 = Math.sqrt(embedding1.reduce((sum, val) => sum + val * val, 0));
  const magnitude2 = Math.sqrt(embedding2.reduce((sum, val) => sum + val * val, 0));

  return dotProduct / (magnitude1 * magnitude2);
}
```

**Преимущества Semantic Similarity**:
- ✅ Контент может отличаться дословно, но семантически совпадать
- ✅ Ловим регрессии качества (если similarity падает ниже 75%, модель деградировала)
- ✅ Работает для любых языков (Jina-v3 поддерживает 89 языков)

**Решение 2: Golden Files (эталонные файлы)**

Для критических сценариев сохраняем "эталонный результат" и сравниваем с ним все последующие прогоны.

```typescript
// tests/e2e/golden-files/critical-scenarios.test.ts
describe('Golden File Regression Tests', () => {
  it('должен соответствовать эталону для курса "Machine Learning Fundamentals"', async () => {
    const result = await generateFullCourse({
      title: 'Machine Learning Fundamentals',
      description: 'Comprehensive ML course covering supervised learning, neural networks, and backpropagation'
    });

    const golden = await loadGoldenFile('ml-fundamentals-course.json');

    // Точное совпадение структуры
    expect(Object.keys(result.metadata)).toEqual(Object.keys(golden.metadata));
    expect(result.sections).toHaveLength(golden.sections.length);

    // Семантическая проверка для переменных полей
    for (let i = 0; i < result.sections.length; i++) {
      const similarity = await calculateSemanticSimilarity(
        JSON.stringify(result.sections[i].topic_analysis),
        JSON.stringify(golden.sections[i].topic_analysis)
      );
      expect(similarity).toBeGreaterThan(0.80); // 80% порог для метаданных
    }

    // Точное совпадение для детерминированных полей
    expect(result.metadata.category).toBe(golden.metadata.category);
    expect(result.metadata.contextual_language).toBe(golden.metadata.contextual_language);
  });
});
```

**Когда используем Golden Files**:
- ✅ Критические сценарии (оплата, FSM-переходы, публикация курсов)
- ✅ Регрессионное тестирование (проверяем, что новая версия не сломала старые сценарии)
- ✅ A/B тестирование моделей (сравниваем качество разных LLM на одинаковых данных)

**Скорость**: 3 минуты 15 секунд на 72 теста. Медленнее из-за реальных API-вызовов, но BullMQ в test mode (без задержек).

---

## Покрытие по слоям: 92% с целевыми порогами

Мы не стремимся к 100% покрытию ради метрики. Вместо этого устанавливаем **целевые пороги для каждого слоя** в зависимости от критичности.

| Слой | Файлов | Покрытие | Целевой порог | Статус |
|------|--------|----------|---------------|--------|
| **FSM & State Management** | 12 | 96% | 95% | ✅ PASS |
| **Generation Phases** | 24 | 91% | 85% | ✅ PASS |
| **Validators** | 18 | 93% | 85% | ✅ PASS |
| **RAG & Embeddings** | 15 | 88% | 85% | ✅ PASS |
| **Utilities** | 45 | 74% | 70% | ✅ PASS |
| **ИТОГО** | **139** | **92%** | **85%** | **✅ PASS** |

**Что исключили из покрытия** (75 файлов):
- Generated types (`.d.ts` файлы) — 38 файлов
- Config files (`*.config.ts`) — 12 файлов
- Test utilities — 25 файлов

**Почему разные пороги?**

**FSM & State Management** (95%+): Критичная логика. Ошибка в FSM → курс зависает в промежуточном состоянии → ручное вмешательство → потеря денег.

**Generation Phases** (85%+): Бизнес-логика. Ошибка → плохое качество контента → жалобы клиентов.

**Utilities** (70%+): Вспомогательные функции. Ошибка → неудобство, но не критично.

---

## Оптимизация скорости тестов: С 24 минут до 8 минут

**Неделя 1 (MVP)**:
```
Общее время: 24 минуты
- Unit-тесты: 3 минуты (много дублирующихся setup'ов)
- Интеграционные: 16 минут (последовательное выполнение)
- E2E: 5 минут (ожидание очередей BullMQ)
```

**Неделя 4 (после оптимизаций)**:
```
Общее время: 8 минут (-67% времени)
- Unit-тесты: 45 секунд (shared fixtures, параллельно)
- Интеграционные: 4 минуты (параллельные контейнеры)
- E2E: 3 минуты 15 секунд (BullMQ test mode, без задержек)
```

**Что сделали**:

1. **Параллельное выполнение** (4 worker'а):
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    pool: 'threads',
    poolOptions: {
      threads: {
        maxThreads: 4,
        minThreads: 2
      }
    }
  }
});
```

2. **Shared fixtures** (загружаем один раз, переиспользуем):
```typescript
// tests/fixtures/shared-data.ts
let cachedBloomsVerbs: string[] | null = null;

export async function getBloomsVerbs(): Promise<string[]> {
  if (cachedBloomsVerbs) return cachedBloomsVerbs;

  cachedBloomsVerbs = await loadBloomsVerbsFromFile();
  return cachedBloomsVerbs;
}
```

3. **BullMQ test mode** (без Redis delays):
```typescript
// tests/integration/setup-bullmq.ts
import { Queue } from 'bullmq';

export function createTestQueue(name: string) {
  return new Queue(name, {
    connection: {
      host: process.env.REDIS_HOST,
      port: Number(process.env.REDIS_PORT)
    },
    defaultJobOptions: {
      removeOnComplete: true,
      removeOnFail: false,
      delay: 0, // Убираем задержки для тестов
      attempts: 1 // Одна попытка (не ждём ретраев)
    }
  });
}
```

4. **Database connection pooling**:
```typescript
// tests/integration/setup-db.ts
const pool = new Pool({
  max: 10, // 10 соединений в пуле
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});
```

**Результат**: Тесты выполняются в 3 раза быстрее. Pre-commit hook выполняет критические тесты за 45 секунд (только unit-тесты). CI pipeline — полный набор за 8 минут.

---

## Enforcing Coverage: Pre-commit Hook + CI Pipeline

**Pre-commit hook** (быстрая обратная связь перед коммитом):

```bash
#!/bin/bash
# .husky/pre-commit

echo "🔍 Running critical path tests..."

# Запускаем тесты только для критических путей (FSM, billing, outbox)
pnpm test:critical

# Проверяем покрытие критических путей (должно быть ≥95%)
pnpm test:coverage --check-coverage \
  --lines 95 \
  --branches 90 \
  --functions 95 \
  --statements 95 \
  --include="src/services/fsm-*" \
  --include="src/server/routers/billing.ts" \
  --include="src/orchestrator/outbox-processor.ts"

if [ $? -ne 0 ]; then
  echo "❌ ERROR: Critical path coverage below 95% threshold"
  echo "📋 Run 'pnpm test:coverage' to see detailed report"
  exit 1
fi

echo "✅ Critical path tests passed"
```

**CI Pipeline** (полная проверка перед мержем):

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20.x'

      - name: Install dependencies
        run: pnpm install

      - name: Run full test suite with coverage
        run: pnpm test:all --coverage

      - name: Check overall coverage threshold (≥85%)
        run: pnpm test:coverage --check-coverage --lines 85

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unittests,integration,e2e
          fail_ci_if_error: true

      - name: Comment PR with coverage
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

**Результат**: Невозможно закоммитить код с покрытием критических путей <95%. CI блокирует мерж PR, если общее покрытие <85%.

---

## Mocking Strategies: Как моковать LLM, БД, очереди

### Mocking LLM API

```typescript
// tests/mocks/llm-mock.ts
import { vi } from 'vitest';

export function createMockLLM() {
  return {
    generate: vi.fn(async ({ prompt, model }) => {
      // Детерминированные ответы для разных промптов
      if (prompt.includes('metadata')) {
        return {
          category: 'technology',
          contextual_language: 'academic_formal',
          topic_analysis: { complexity: 'intermediate' }
        };
      }

      if (prompt.includes('lesson')) {
        return {
          lesson_title: 'Introduction to Neural Networks',
          lesson_content: '<p>Neural networks are...</p>',
          objectives: ['Understand neurons', 'Learn activation functions']
        };
      }

      throw new Error(`Unmocked prompt: ${prompt}`);
    })
  };
}

// Использование в тестах
it('должен генерировать метаданные', async () => {
  const mockLLM = createMockLLM();
  const result = await generateMetadata({ title: 'Test', llmClient: mockLLM });

  expect(mockLLM.generate).toHaveBeenCalledOnce();
  expect(result.category).toBe('technology');
});
```

### Mocking Supabase Client

```typescript
// tests/mocks/supabase-mock.ts
export function createMockSupabase() {
  return {
    from: vi.fn((table: string) => ({
      select: vi.fn(() => ({
        eq: vi.fn(() => ({
          single: vi.fn(async () => ({
            data: { id: 'test-123', title: 'Test Course' },
            error: null
          }))
        }))
      })),
      insert: vi.fn(async (data) => ({
        data: { ...data, id: 'generated-id' },
        error: null
      })),
      update: vi.fn(() => ({
        eq: vi.fn(async () => ({ data: null, error: null }))
      }))
    })),
    rpc: vi.fn(async (fnName, params) => {
      if (fnName === 'create_course_atomic') {
        return { data: { id: 'new-course', ...params }, error: null };
      }
      return { data: null, error: new Error(`Unmocked RPC: ${fnName}`) };
    })
  };
}
```

### Mocking Pino Logger (проблема с CircularJSON)

Оригинальный Pino logger использует circular references, что ломает сериализацию в тестах.

```typescript
// tests/mocks/pino-mock.ts
import { vi } from 'vitest';

export function createMockLogger() {
  const logSpy = vi.fn();

  return {
    info: vi.fn((...args) => logSpy('info', ...args)),
    warn: vi.fn((...args) => logSpy('warn', ...args)),
    error: vi.fn((...args) => logSpy('error', ...args)),
    debug: vi.fn((...args) => logSpy('debug', ...args)),
    child: vi.fn(() => createMockLogger()), // Рекурсивный мок для child loggers
    _logSpy: logSpy // Для проверки в тестах
  };
}

// Использование
it('должен логировать ошибки', async () => {
  const logger = createMockLogger();

  await processWithError({ logger });

  expect(logger.error).toHaveBeenCalledWith(
    expect.objectContaining({ error: expect.any(Error) }),
    'Processing failed'
  );
});
```

---

## Disclaimer: Expected Pushback

Я понимаю, что эта статья вызовет критику со стороны разработчиков. «92% покрытие в AI-системе? Невозможно», «Семантическая валидация через embeddings — слишком дорого», «Testcontainers медленные».

Моя позиция: я думаю, эта реакция больше про **страх, смешанный с высокомерием**, чем про реальные технические аргументы.

**Страх**: «Если AI-системы действительно можно нормально тестировать, значит мой опыт ручного QA обесценивается?»
**Высокомерие**: «Только настоящий инженер может вручную проверить качество AI-контента, автоматические тесты — игрушка.»

**Реальность**: Автоматические тесты не заменяют человеческую экспертизу. Они освобождают разработчиков от рутинных проверок (структура JSON, валидация схем, регрессии) и позволяют сосредоточиться на сложных сценариях (качество контента, UX, бизнес-логика).

Если не согласны — отлично. Клонируйте репозиторий, запустите тесты, а потом скажите, где я не прав. Я предпочитаю технические аргументы эмоциональным реакциям.

---

## Lessons Learned: Что работает, а что нет

### ✅ Что работает

1. **Testcontainers для интеграционных тестов**: Изоляция, параллельность, реальная PostgreSQL. Стоит дополнительных 2-3 минут на setup.

2. **Semantic Similarity вместо точного совпадения**: Единственный способ тестировать недетерминированный контент. Jina-v3 embeddings (768-dim) + cosine similarity.

3. **Golden Files для критических сценариев**: Регрессионное тестирование работает. Сохраняем эталонные результаты, сравниваем семантически.

4. **Целевые пороги покрытия по слоям**: FSM 95%+, business logic 85%+, utilities 70%+. Не стремимся к 100% ради метрики.

5. **Pre-commit hook для критических путей**: Быстрая обратная связь (45 секунд), блокирует коммиты с недостаточным покрытием.

### ❌ Что НЕ работает

1. **Моковать всё в E2E-тестах**: Пытались моковать LLM API в E2E. Результат: тесты проходят, но в проде баги. E2E должны использовать реальные API.

2. **100% покрытие для всего кода**: Generated types, configs, test utilities — не имеет смысла тестировать. Фокусируемся на бизнес-логике.

3. **Один большой интеграционный тест**: Пытались тестировать весь пайплайн (5 фаз) в одном тесте. Результат: когда ломается, непонятно, где именно. Разбили на 130 маленьких интеграционных тестов.

4. **Snapshot testing для AI-контента**: Vitest snapshots не работают для LLM-ответов (каждый раз разные). Snapshot testing годится только для структуры, не для контента.

5. **Игнорировать скорость тестов**: 24 минуты на полный прогон → никто не запускает локально → тесты игнорируются. Оптимизировали до 8 минут → тесты выполняются в CI и локально.

---

## Результаты: Что это даёт на практике

**Метрики**:
- **397 тестовых файлов** на 139 исходных файлов (соотношение 2.85:1)
- **92% покрытие** кода (139 source files, 75 excluded)
- **8 минут** на полный прогон тестов (unit + integration + E2E)
- **45 секунд** на критические тесты в pre-commit hook
- **0 багов в FSM** за последние 6 месяцев (50,000+ сгенерированных курсов)
- **<2% retrieval failures** в RAG (тестируем hierarchical chunking)

**Что изменилось в процессе разработки**:

1. **Рефакторинг без страха**: Изменяем архитектуру, тесты показывают, что сломалось.
2. **Быстрые итерации**: Добавили новую фазу генерации → написали тесты → убедились, что старые сценарии не сломались.
3. **Onboarding новых разработчиков**: Тесты — живая документация. Новый человек читает тесты, понимает, как работает система.
4. **Уверенность в деплое**: CI блокирует мерж, если покрытие <85%. Продакшн стабилен.

**Сравнение с индустрией**:

| Метрика | Индустрия (AI-системы) | Наш проект |
|---------|------------------------|------------|
| Покрытие тестами | <60% | 92% |
| Тестирование LLM-логики | Обычно не тестируют | Семантическая валидация |
| Время выполнения тестов | 15-30 минут | 8 минут |
| Изоляция БД в тестах | Shared DB / SQLite | Testcontainers (real PostgreSQL) |
| Критические баги в FSM | 5-10 в год | 0 за 6 месяцев |

---

## Contact & Feedback

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/maslennikovigor
Заходите, читайте мои мысли и статьи. Пишу нечасто, но когда пишу — стоит прочитать.

**Прямой контакт**: https://t.me/maslennikovig
Нужно поговорить? Пишите напрямую. Всегда рад общению.

### 💬 Обратная связь: Я максимально открыт

**Хочу услышать**:
- **Критику** — Что не так с этим подходом? Где слабые места?
- **Идеи** — Какие фичи стоит добавить? Чего не хватает?
- **Предложения** — Как улучшить, оптимизировать или отрефакторить систему?
- **Вопросы** — Что-то непонятно? Спрашивайте.

**Каналы для обратной связи**:
- **Telegram**: https://t.me/maslennikovig (для прямого общения)
- **Комментарии на VC.ru**: Пишите под статьёй, отвечу всем

**Тон**: Супер открыт к конструктивному диалогу. Без эго, просто хочу сделать это лучше.

---

## Заключение

Тестирование AI-систем — это не «миссия невыполнима». Это про правильные стратегии:

1. **Многослойная валидация**: Структурная (дёшево) → Контрактная (дёшево) → Семантическая (дорого, выборочно)
2. **Тестовая пирамида**: Unit (195, быстро) → Integration (130, реально) → E2E (72, реальные API)
3. **Testcontainers**: Реальная PostgreSQL, изоляция, параллельность
4. **Semantic Similarity**: Единственный способ тестировать недетерминированный контент
5. **Целевые пороги**: FSM 95%+, бизнес-логика 85%+, утилиты 70%+

**397 тестов, 92% покрытие, 8 минут выполнения** — это не красивая метрика для слайдов. Это реальная продакшн-система, которая генерирует 10,000+ курсов в месяц без критических багов в FSM за 6 месяцев.

Попробуйте применить эти подходы в своих AI-проектах. Если найдёте лучшие решения — делитесь, я первый захочу узнать.
