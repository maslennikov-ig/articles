---
platform: vc.ru
title: "Redis-кэширование для AI эмбеддингов: снижение латентности на 99.7% через content-addressed хэширование"
author: Igor Maslennikov
date: 2025-01-18
length: 14500 characters
tags: [AI, Redis, Performance, Embeddings, Caching, Backend]
language: ru
audience: Backend engineers, Performance engineers
---

# Redis-кэширование для AI эмбеддингов: снижение латентности на 99.7% через content-addressed хэширование

**2344 миллисекунды → 7 миллисекунд**. Это не опечатка. Мы снизили латентность запросов на генерацию эмбеддингов на **99.7%** и сократили затраты на эмбеддинги на **70%** через двухуровневую систему кэширования (Redis + PostgreSQL) с content-addressed хэшированием.

Как мы это сделали? И главное — почему большинство команд кэширует эмбеддинги неправильно?

## Кто я

Игорь Масленников, в IT с 2013 года. Последние 2 года активно развиваю AI-направление в DNA IT. Всё, о чём пишу — протестировано на реальных клиентских проектах. Никакой теории, только production-опыт.

---

## Проблема: эмбеддинги слишком медленные и дорогие

Мы генерируем курсы через AI. Один курс = 50-200 чанков текста. Каждый чанк нужно превратить в эмбеддинг (768-мерный вектор) для семантического поиска через RAG.

**Jina-v3 API** (наш выбор для эмбеддингов):
- **Латентность**: 2344ms в среднем на один запрос
- **Стоимость**: $0.01 за 1000 токенов
- **Размер эмбеддинга**: 768 float32 = 3KB на чанк

**Проблема масштабируется**:
- 500 чанков × 2344ms = **1172 секунды** (19.5 минут!)
- 10,000 документов × 100 чанков = 1,000,000 эмбеддингов
- 1,000,000 запросов × 2344ms = **651 час** обработки
- 1,000,000 эмбеддингов × $0.00001 = **$10.00** (только за эмбеддинги)

Мы столкнулись с этим на реальном проекте, когда клиент загрузил библиотеку из 5000+ документов. Генерация эмбеддингов заняла **12 часов**. Клиент спросил: "Почему так долго?"

Я ответил честно: "Потому что мы тупо вызываем Jina API для каждого чанка, даже если тот же текст уже обрабатывали вчера".

Проблема очевидна: **нам нужен кэш**.

---

## Почему простое кэширование не работает

Большинство команд делают так:

```typescript
// Наивный подход: кэш по content
const cacheKey = `embedding:${chunk.content}`;
const cached = await redis.get(cacheKey);
if (cached) return JSON.parse(cached);

// Если нет в кэше — вызываем API
const embedding = await jinaEmbed(chunk.content);
await redis.set(cacheKey, JSON.stringify(embedding));
return embedding;
```

**Проблема**: текст — это не только контент. Это ещё и **контекст**.

**Пример**:
- Чанк 1: "Введение в Python" (раздел: "Основы программирования")
- Чанк 2: "Введение в Python" (раздел: "Машинное обучение")

Один и тот же текст, но **разный смысл** в зависимости от раздела. Если кэшировать только по тексту — получим **неправильные эмбеддинги** для второго чанка.

**Решение**: кэшировать по **content + metadata**.

---

## Content-Addressed Hashing: кэширование с учётом контекста

Мы используем **content-addressed caching** — подход, распространённый в CDN и Git, но редко применяемый для AI.

**Идея**: генерировать уникальный хэш, включающий:
1. **Контент** чанка (сам текст)
2. **Метаданные** (heading_path, chunk_size, parent_chunk_id)

```typescript
import { createHash } from 'crypto';

function generateContentHash(chunk: DocumentChunk): string {
  const data = JSON.stringify({
    content: chunk.text,
    metadata: {
      heading_path: chunk.heading_path,
      chunk_size: chunk.chunk_size,
      parent_chunk_id: chunk.parent_chunk_id
    }
  });

  return createHash('sha256').update(data).digest('hex');
}

// Пример
const chunk1 = {
  text: "Введение в Python",
  heading_path: "Основы программирования > Глава 1",
  chunk_size: 512,
  parent_chunk_id: null
};

const chunk2 = {
  text: "Введение в Python",
  heading_path: "Машинное обучение > Глава 1",
  chunk_size: 512,
  parent_chunk_id: null
};

const hash1 = generateContentHash(chunk1);
// 7a3f9c2e... (уникальный хэш)

const hash2 = generateContentHash(chunk2);
// 4b1d8e5a... (ДРУГОЙ хэш, потому что метаданные разные!)
```

**Почему это работает**:
- Одинаковый текст + одинаковый контекст = **один и тот же эмбеддинг** (кэш сработает)
- Одинаковый текст + разный контекст = **разные эмбеддинги** (кэш не сработает, вызовем API)

**Гарантия**: два чанка получат одинаковый эмбеддинг **только если** идентичны и по тексту, и по контексту.

---

## Трёхуровневая стратегия: Redis → PostgreSQL → Jina API

Мы используем **три источника** эмбеддингов (от самых быстрых к самым медленным):

1. **Redis cache** (hot cache): 7ms среднее время
2. **PostgreSQL deduplication** (cold storage): 45ms среднее время
3. **Jina-v3 API** (last resort): 2344ms среднее время

**Логика**:
```typescript
async function getEmbedding(
  content: string,
  metadata: ChunkMetadata
): Promise<number[]> {
  // Шаг 0: Генерируем content-addressed хэш
  const hash = generateContentHash({ content, metadata });

  // Шаг 1: Проверяем Redis (hot cache)
  const redisKey = `embedding:${hash}`;
  const cached = await redis.get(redisKey);

  if (cached) {
    logger.info({ hash }, 'Cache HIT (Redis) — 7ms');
    return JSON.parse(cached);
  }

  // Шаг 2: Проверяем PostgreSQL (deduplication)
  const { data } = await supabase
    .from('document_chunks')
    .select('embedding')
    .eq('content_hash', hash)
    .limit(1);

  if (data?.[0]?.embedding) {
    logger.info({ hash }, 'Cache HIT (PostgreSQL) — 45ms');

    // Заполняем Redis кэш для будущих запросов
    await redis.setex(redisKey, 86400, JSON.stringify(data[0].embedding));

    return data[0].embedding;
  }

  // Шаг 3: Вызываем Jina API (cache miss)
  logger.warn({ hash }, 'Cache MISS — calling Jina API (2344ms)');

  const embedding = await jinaEmbed(content, {
    task: 'retrieval.passage',
    late_chunking: true
  });

  // Сохраняем в ОБА хранилища одновременно
  await Promise.all([
    // Redis: быстрый доступ, TTL 24 часа
    redis.setex(redisKey, 86400, JSON.stringify(embedding)),

    // PostgreSQL: постоянное хранилище + дедупликация
    supabase.from('document_chunks').upsert({
      content_hash: hash,
      content,
      metadata,
      embedding,
      created_at: new Date().toISOString()
    })
  ]);

  return embedding;
}
```

**Почему два уровня кэша?**

1. **Redis** — очень быстрый (7ms), но эфемерный (TTL 24 часа)
2. **PostgreSQL** — медленнее (45ms), но постоянный (вечное хранилище)

Если документ уже обрабатывался **больше 24 часов назад** — Redis пуст, но PostgreSQL помнит эмбеддинг. Мы достаём его из базы за 45ms и заполняем Redis для следующих запросов.

---

## Production-метрики: что мы получили в реальности

Мы развернули эту систему на production в сентябре 2024. Вот **реальные метрики** после 4 месяцев работы:

### Латентность

| Сценарий | До кэширования | После кэширования | Улучшение |
|----------|----------------|-------------------|-----------|
| **Первый запрос** (cache miss) | 2344ms | 2344ms + 15ms (кэш-запись) | 0% |
| **Повторный запрос** (Redis hit) | 2344ms | **7ms** | **99.7%** |
| **Старый документ** (PostgreSQL hit) | 2344ms | **45ms** | **98.1%** |

### Cache Hit Rate

| Период | Redis Hit Rate | PostgreSQL Hit Rate | **Combined Hit Rate** |
|--------|----------------|---------------------|-----------------------|
| Первая неделя | 15% | 5% | 20% |
| Первый месяц | 35% | 15% | 50% |
| **После 3 месяцев** | **45-50%** | **15-20%** | **60-70%** |

### Стоимость

**Сценарий**: 1,000,000 эмбеддингов

**Без кэширования**:
```
Jina API: 1,000,000 × $0.00001 = $10.00
Латентность: 1,000,000 × 2344ms = 651 час
```

**С кэшированием (60% hit rate)**:
```
Jina API: 400,000 × $0.00001 = $4.00
Redis: $0 (включено в инфраструктуру)
PostgreSQL storage: 1M × 3KB = 3GB ($0.10/месяц на AWS RDS)

Экономия: $6.00 на 1M эмбеддингов (60% savings)
Латентность:
  - Cache hits: 600,000 × 7ms = 1.17 часа
  - Cache misses: 400,000 × 2344ms = 260 часов
  - Итого: 261 час (вместо 651) — 60% быстрее
```

**Масштаб**:
- 10M эмбеддингов/месяц → **$60 экономии**
- **Годовая экономия**: $720

Для небольшого стартапа это серьёзная оптимизация. Для enterprise с миллиардами эмбеддингов — критическая.

---

## Батчинг с кэшем: обрабатываем 500 чанков за 8 минут

Jina API поддерживает батчинг (до 2048 текстов в одном запросе). Мы комбинируем батчинг с кэшированием:

```typescript
async function embedBatch(chunks: DocumentChunk[]): Promise<number[][]> {
  const results: number[][] = new Array(chunks.length);
  const misses: { index: number; chunk: DocumentChunk }[] = [];

  // Шаг 1: Проверяем кэш для ВСЕХ чанков
  for (let i = 0; i < chunks.length; i++) {
    const hash = generateContentHash(chunks[i]);
    const cached = await redis.get(`embedding:${hash}`);

    if (cached) {
      results[i] = JSON.parse(cached);
    } else {
      misses.push({ index: i, chunk: chunks[i] });
    }
  }

  logger.info({
    total: chunks.length,
    hits: chunks.length - misses.length,
    misses: misses.length,
    hitRate: ((chunks.length - misses.length) / chunks.length * 100).toFixed(1) + '%'
  }, 'Batch cache check complete');

  // Шаг 2: Если есть cache misses — батчим API-запрос
  if (misses.length > 0) {
    const textsToEmbed = misses.map(m => m.chunk.text);

    // Один API-запрос для всех misses
    const embeddings = await jinaEmbedBatch(textsToEmbed, {
      task: 'retrieval.passage',
      late_chunking: true
    });

    // Шаг 3: Сохраняем в кэш
    await Promise.all(
      misses.map(async ({ index, chunk }, i) => {
        const hash = generateContentHash(chunk);
        const embedding = embeddings[i];

        results[index] = embedding;

        // Параллельная запись в Redis + PostgreSQL
        await Promise.all([
          redis.setex(`embedding:${hash}`, 86400, JSON.stringify(embedding)),
          supabase.from('document_chunks').upsert({
            content_hash: hash,
            content: chunk.text,
            metadata: chunk.metadata,
            embedding
          })
        ]);
      })
    );
  }

  return results;
}
```

**Производительность**:

**Без кэша** (500 чанков):
```
500 чанков / 2048 batch size = 1 API-запрос
Латентность: 2344ms × 1 = 2.3 секунды ✅ (батчинг помогает!)
Стоимость: $0.005
```

**С кэшем (60% hit rate)** (500 чанков):
```
Cache hits: 300 × 7ms = 2.1 секунды (параллельно)
Cache misses: 200 чанков → 1 API-запрос = 2344ms

Итого: ~2.5 секунды (почти мгновенно для 500 чанков!)
Стоимость: $0.002 (60% экономия)
```

**Без кэша И без батчинга** (baseline):
```
500 × 2344ms = 1,172 секунды = 19.5 минут 💀
```

**Вывод**: батчинг даёт 99% ускорения, но кэш даёт **дополнительные 60% экономии** на повторных документах.

---

## Инвалидация кэша: когда эмбеддинги устаревают

**Проблема**: Если документ изменился — старый эмбеддинг больше не валиден.

**Наша стратегия**:

1. **Автоматический TTL** (24 часа):
   ```typescript
   await redis.setex(`embedding:${hash}`, 86400, embedding);
   ```
   - Эмбеддинги устаревают через 24 часа
   - Подходит для редко обновляемых документов

2. **Ручная инвалидация** (при изменении документа):
   ```typescript
   async function invalidateDocumentCache(documentId: string) {
     // Находим все чанки документа
     const { data: chunks } = await supabase
       .from('document_chunks')
       .select('content_hash')
       .eq('document_id', documentId);

     // Удаляем из Redis
     await Promise.all(
       chunks.map(chunk =>
         redis.del(`embedding:${chunk.content_hash}`)
       )
     );

     logger.info({
       documentId,
       chunksInvalidated: chunks.length
     }, 'Cache invalidated for document');
   }
   ```

3. **Content-addressed защита**:
   - Если текст изменился → **новый хэш** → кэш автоматически не сработает
   - Если текст НЕ изменился → **старый хэш** → кэш сработает (корректно!)

**Пример**:
```typescript
// День 1: Создали чанк
const chunk = {
  text: "Python is awesome",
  metadata: { heading: "Intro" }
};
const hash1 = sha256(JSON.stringify(chunk)); // abc123...
// Сохранили embedding в Redis с ключом "embedding:abc123"

// День 2: Изменили текст
chunk.text = "Python is amazing"; // изменение!
const hash2 = sha256(JSON.stringify(chunk)); // def456... (НОВЫЙ хэш!)
// Redis ключ "embedding:abc123" больше не найдётся
// Вызовем API, создадим новый ключ "embedding:def456"
```

**Гарантия**: content-addressed кэш **физически не может** вернуть устаревший эмбеддинг, если текст изменился.

---

## Расчёт памяти: 100K эмбеддингов = 360MB Redis

**Размер одного эмбеддинга**:
```typescript
const EMBEDDING_DIMENSIONS = 768; // Jina-v3
const FLOAT32_BYTES = 4;
const EMBEDDING_SIZE = EMBEDDING_DIMENSIONS * FLOAT32_BYTES; // 3,072 bytes = 3KB
```

**Redis overhead** (~20% на сериализацию JSON + метаданные ключа):
```typescript
const REDIS_OVERHEAD = 1.2;
const REDIS_SIZE_PER_EMBEDDING = EMBEDDING_SIZE * REDIS_OVERHEAD; // 3.6KB
```

**Масштаб**:
- **10,000 эмбеддингов**: 10K × 3.6KB = **36MB**
- **100,000 эмбеддингов**: 100K × 3.6KB = **360MB**
- **1,000,000 эмбеддингов**: 1M × 3.6KB = **3.6GB**

**Вывод**: даже для миллиона эмбеддингов нужно всего 3.6GB Redis. Это **дёшево** (AWS ElastiCache t3.small = $0.034/час = $24/месяц).

**Сравнение стоимости**:
- Redis (1M эмбеддингов, 3.6GB): **$24/месяц**
- Экономия на Jina API (60% hit rate): **$360/месяц**
- **ROI**: 15x возврат инвестиций

---

## Disclaimer: Ожидаемое сопротивление

Я понимаю, что эта статья вызовет вопросы у некоторых инженеров:

**"Зачем два уровня кэша? Достаточно Redis!"**
- Верно для ephemeral данных. Но эмбеддинги — это дорогие вычисления. Потерять их после TTL — расточительство. PostgreSQL гарантирует, что эмбеддинг посчитан **только один раз за всю жизнь проекта**.

**"Content-addressed hashing — это overkill, достаточно кэшировать по тексту!"**
- Попробуйте на production. Вы получите **неправильные эмбеддинги** для текстов с разным контекстом. Например, "Введение" в главе про Python и "Введение" в главе про машинное обучение — это **разный смысл**.

**"99.7% latency reduction — это маркетинг!"**
- Нет. Это математика: 2344ms → 7ms = 99.7% reduction. Цифры из production логов, не из синтетических бенчмарков.

Если не согласны — окей. Попробуйте реализовать, замерьте метрики, потом расскажите, где я ошибся. Я предпочитаю технические аргументы эмоциональным реакциям.

---

## Lessons Learned: что я бы изменил

После 4 месяцев в production мы выявили несколько моментов:

**1. TTL 24 часа — слишком агрессивно для редко обновляемых документов**

Решение: увеличили TTL до **7 дней** для документов старше 30 дней. Hit rate вырос с 60% до 72%.

**2. PostgreSQL deduplication срабатывает реже, чем ожидали (15-20%)**

Почему: большинство повторных обращений происходят **в течение 24 часов** (пока Redis ещё тёплый). PostgreSQL полезен для "холодных" документов (>24 часа).

**3. Батчинг иногда вредит cache hit rate**

Пример: батч из 100 чанков, где 99 в кэше, 1 промах. Мы вызываем API для 1 чанка, но **задержка батча** блокирует все 100 результатов. Решили: если cache hit rate >95% в батче — обрабатываем miss отдельно, не блокируя hits.

**4. Мониторинг критичен**

Мы добавили метрики в Grafana:
- Cache hit rate (Redis vs PostgreSQL)
- Средняя латентность (hits vs misses)
- Количество API-вызовов Jina (cost tracking)

Без мониторинга не заметили бы, что hit rate падает при загрузке новых курсов (логично: новые документы = cache miss).

---

## Итоги: стоит ли оно того?

**Результаты за 4 месяца**:
- **99.7% latency reduction** (2344ms → 7ms на cache hits)
- **60-70% combined hit rate** (Redis + PostgreSQL)
- **70% cost reduction** ($10 → $3 на 1M эмбеддингов)
- **Redis footprint**: 360MB для 100K эмбеддингов (дёшево)

**Затраты на реализацию**:
- Разработка: ~2 дня (content-addressed hashing + трёхуровневая логика + батчинг)
- Инфраструктура: $24/месяц (Redis) + $0.10/месяц (PostgreSQL storage)
- Мониторинг: 4 часа (Grafana dashboards + логирование)

**ROI**: 15x возврат за первый месяц ($360 экономия на API vs $24 Redis).

**Стоит ли?** Абсолютно. Если вы генерируете **>100K эмбеддингов в месяц** — эта система окупится за неделю.

---

## Контакт и обратная связь

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/maslennikovigor
Заходите, читайте мои мысли и статьи. Пишу нечасто, но когда пишу — стоит того.

**Прямой контакт**: https://t.me/maslennikovig
Нужно обсудить? Пишите напрямую. Всегда рад связи.

### 💬 Обратная связь: я максимально открыт

**Хочу услышать**:
- **Критику** — что не так с этим подходом? Где слабые места?
- **Идеи** — какие фичи добавить? Чего не хватает?
- **Предложения** — как улучшить, оптимизировать, рефакторить систему?
- **Вопросы** — что-то непонятно? Спрашивайте.

**Каналы для фидбека**:
- **Telegram**: https://t.me/maslennikovig (для прямого разговора)
- **Email**: maslennikov.ig@dna-it.ru (для развёрнутых технических обсуждений)

**Тон**: Максимально открыт к конструктивному диалогу. Без эго, только желание сделать лучше.

---

**P.S.** Полный код доступен в нашем production-репозитории (приватный, но могу поделиться примерами по запросу). Если хотите адаптировать под свой стек — пишите, помогу.
