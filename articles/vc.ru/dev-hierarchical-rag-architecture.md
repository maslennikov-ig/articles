---
platform: vc.ru
title: "Иерархическая RAG-архитектура: Снижение ошибок извлечения на 67% через двухуровневую систему чанкинга"
author: Igor Maslennikov
date: 2025-11-18
length: 15840
tags: RAG, Machine Learning, AI, Vector Search, Architecture, Production
language: ru
audience: Software Engineers, ML Engineers, System Architects
---

# Иерархическая RAG-архитектура: Снижение ошибок извлечения на 67% через двухуровневую систему чанкинга

## Проблема: Точность против контекста

Классические RAG-системы ставят вас перед выбором: либо точное извлечение (маленькие чанки), либо достаточный контекст для LLM (большие чанки). Оба варианта плохие.

Я столкнулся с этой проблемой год назад, когда работал над платформой генерации образовательного контента в AI Dev Team. Мы индексировали техническую документацию, учебники по машинному обучению, API-референсы. Пользователь задаёт вопрос: **"Объясни алгоритм обратного распространения ошибки"**.

RAG извлекает чанк из 400 токенов:

```
Backpropagation updates network weights using gradients calculated
through the chain rule. The algorithm propagates error backwards
from output to input layers.
```

Технически корректно. Семантически релевантно. Но **недостаточно для генерации качественного ответа**. LLM не знает из этого чанка:
- Что такое градиенты?
- Как они вычисляются?
- Что за chain rule?
- Какая математическая основа?

Потому что вся эта информация была **два абзаца выше** в оригинальном документе. Но мы разрезали документ на чанки по 400 токенов, и контекст потерялся.

Мы проанализировали 100 неудачных извлечений. **67% содержали правильный чанк, но недостаточный контекст для генерации**. Это называется "The Missing Context Problem".

Решение, которое мы построили, снизило ошибки извлечения с 5-6% до <2% (-67%). Плюс дало улучшение качества на 35-49% **бесплатно** через late chunking. Про это ниже.

---

## Три неудачные попытки

Я не сразу пришёл к иерархической архитектуре. Было три провальных итерации.

### Попытка 1: Плоские чанки по 800 токенов

Казалось разумным: 800 токенов — больше чем 400 (точность), меньше чем 1500 (контекст). Золотая середина.

**Результат**: Precision@5 = 70%.

**Режим отказа**: Чанки содержали слишком много нерелевантного контента. Semantic similarity scores размывались. Запрос "backpropagation algorithm" извлекал чанки про "neural networks", где backpropagation упоминался один раз в 800 токенах. Остальное — про архитектуру сетей, активационные функции, всё что угодно.

### Попытка 2: Маленькие чанки по 400 токенов

Логика: оптимизируем под точность. Меньше чанк → больше плотность информации → выше semantic similarity.

**Результат**: Precision@5 = 85% (отлично!).

**Режим отказа**: LLM не могли генерировать качественный контент. Контекст недостаточен. Запрос "Explain backpropagation" извлекал чанк: "Backpropagation updates weights using gradients." Но **что такое градиенты? Как вычисляются? Chain rule? Calculus foundation?** — всё это было за пределами 400 токенов.

### Попытка 3: Большие чанки по 1500 токенов

Переворачиваем стратегию: оптимизируем под контекст. Больше токенов → больше информации → LLM могут генерировать качественные ответы.

**Результат**: Context sufficiency = 92% (LLM генерируют отличный контент).

**Режим отказа**: Precision деградировала до 65%. Извлекали нерелевантный контент, потому что чанки слишком широкие. Semantic similarity разбавлялась посторонней информацией.

---

## Прорыв: Индексируй малое, возвращай большое

Инсайт пришёл из документации Anthropic по RAG: **"index small, retrieve large"**. Но они не объясняли **КАК**.

Я протестировал 4 архитектуры (задокументировал в `docs/generation/RAG1-ANALYSIS.md`):

### Вариант 1: Overlapping windows

400-токеновые чанки с 200-токеновым перекрытием.

**Плюсы**: Лучшая непрерывность контекста.
**Минусы**: 2x storage overhead, отсутствие иерархических связей.

### Вариант 2: Recursive summarization

Чанк → summary → embed both.

**Плюсы**: Многоуровневое извлечение.
**Минусы**: Суммаризация добавляет стоимость ($0.01 per doc) и потенциальную потерю информации.

### Вариант 3: Sentence-window retrieval

Индексируй предложения, возвращай ±5 предложений вокруг.

**Плюсы**: Точное извлечение.
**Минусы**: Фиксированный размер окна не учитывает семантические границы (параграфы, секции).

### Вариант 4: Parent-child hierarchical chunking ✅ ПОБЕДИТЕЛЬ

**Индексируй точные 400-токеновые children, возвращай контекстные 1500-токеновые parents.**

**Плюсы**:
- Precision через маленькие чанки (400 токенов)
- Context sufficiency через большие родительские чанки (1500 токенов)
- Heading-aware boundaries уважают структуру документа
- Metadata enrichment для advanced retrieval strategies

**Минусы**:
- +30% storage overhead (но ROI валидирован через снижение failure rate)

---

## Двухпроходная иерархическая система чанкинга

Архитектура состоит из двух проходов:

**Pass 1**: `MarkdownHeaderTextSplitter` уважает структуру документа.
**Pass 2**: `RecursiveCharacterTextSplitter` с `tiktoken` достигает целевых размеров.

Вот полная реализация:

```typescript
import { MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { encode } from 'gpt-tokenizer'; // tiktoken wrapper
import { v4 as uuidv4 } from 'uuid';

interface Chunk {
  chunk_id: string;
  parent_chunk_id: string | null;
  content: string;
  parent_content: string;
  metadata: {
    heading_path?: string;
    parent_chunk_id?: string;
    chunk_size: number;
    parent_size: number;
    h1?: string;
    h2?: string;
    h3?: string;
  };
}

async function createHierarchicalChunks(markdown: string): Promise<Chunk[]> {
  // Pass 1: MarkdownHeaderTextSplitter respects structure
  const headerSplitter = new MarkdownHeaderTextSplitter({
    headers_to_split_on: [
      ["#", "h1"],
      ["##", "h2"],
      ["###", "h3"],
    ],
  });

  const structuredDocs = await headerSplitter.splitText(markdown);

  // Pass 2: RecursiveCharacterTextSplitter with tiktoken hits target sizes
  const tokenSplitter = new RecursiveCharacterTextSplitter({
    chunk_size: 1500,  // Parent size
    chunk_overlap: 200,
    length_function: (text) => encode(text).length,  // tiktoken
    separators: ["\n\n", "\n", ". ", " ", ""],
  });

  const parents = await tokenSplitter.splitDocuments(structuredDocs);

  // Create children from each parent (400-token sub-chunks)
  const childSplitter = new RecursiveCharacterTextSplitter({
    chunk_size: 400,
    chunk_overlap: 50,
    length_function: (text) => encode(text).length,
  });

  const hierarchicalChunks: Chunk[] = [];

  for (const parent of parents) {
    const parentId = uuidv4();
    const children = await childSplitter.splitDocuments([parent]);

    for (const child of children) {
      hierarchicalChunks.push({
        chunk_id: uuidv4(),
        parent_chunk_id: parentId,
        content: child.pageContent,
        parent_content: parent.pageContent,  // Store for retrieval
        metadata: {
          ...child.metadata,
          heading_path: extractHeadingPath(child.metadata),
          parent_chunk_id: parentId,
          chunk_size: encode(child.pageContent).length,
          parent_size: encode(parent.pageContent).length,
        },
      });
    }
  }

  return hierarchicalChunks;
}

function extractHeadingPath(metadata: any): string {
  const parts = [];
  if (metadata.h1) parts.push(metadata.h1);
  if (metadata.h2) parts.push(metadata.h2);
  if (metadata.h3) parts.push(metadata.h3);
  return parts.join(' > ');
}
```

### Магия heading hierarchy

Каждый чанк получает метаданные с `heading_path`:

```
"Ch1: Introduction > Section 1.2: Neural Networks > Backpropagation"
```

Это даёт:
- **Semantic breadcrumb navigation**: Пользователи понимают, откуда чанк.
- **Sibling chunk awareness**: Можно извлекать related sections.
- **Parent-child relationships**: Fallback к более широкому контексту при необходимости.

---

## Hybrid Search: Dense + Sparse с Reciprocal Rank Fusion

Только semantic search недостаточно. Keyword matching тоже нужен.

**Проблема**: Запрос "ReLU activation function" семантически близок к "activation functions", но **терм "ReLU"** критичен. Если документ использует только "Rectified Linear Unit" без аббревиатуры, pure semantic search может его пропустить.

**Решение**: Hybrid search — комбинация Jina-v3 dense vectors (768-dim) и BM25 sparse vectors с Reciprocal Rank Fusion (RRF).

```typescript
import { QdrantClient } from '@qdrant/js-client-rest';
import { BM25 } from 'natural';

interface SearchResult {
  chunk_id: string;
  content: string;
  parent_content: string;
  score: number;
  metadata: any;
}

async function hybridSearch(query: string, k: number = 5): Promise<SearchResult[]> {
  // Dense vector search (Jina-v3 with late chunking)
  const queryEmbedding = await jinaEmbed(query, { late_chunking: true });

  const qdrant = new QdrantClient({ url: process.env.QDRANT_URL });
  const denseResults = await qdrant.search('document_chunks', {
    vector: queryEmbedding,
    limit: k * 2,  // Over-retrieve for RRF
    with_payload: true,
  });

  // Sparse keyword search (BM25)
  const sparseResults = await bm25Search(query, k * 2);

  // Reciprocal Rank Fusion
  const fused = reciprocalRankFusion(
    [denseResults.map(r => r.id), sparseResults.map(r => r.id)],
    k
  );

  // Fetch full chunks and return parent content
  const chunks = await fetchChunksByIds(fused);

  return chunks.map(chunk => ({
    ...chunk,
    content: chunk.parent_content,  // 1500 tokens for LLM
    indexed_content: chunk.content,  // 400 tokens (transparency)
  }));
}

function reciprocalRankFusion(rankings: string[][], k: number, c: number = 60): string[] {
  const scores = new Map<string, number>();

  rankings.forEach(ranking => {
    ranking.forEach((id, index) => {
      const score = 1 / (c + index + 1);
      scores.set(id, (scores.get(id) || 0) + score);
    });
  });

  return Array.from(scores.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, k)
    .map(([id]) => id);
}
```

**Почему RRF?**

Альтернативы:
- **Weighted average**: Требует ручной настройки весов (0.7 dense + 0.3 sparse?).
- **Linear combination**: Scores имеют разные scales (dense 0-1, BM25 0-∞).
- **RRF**: Rank-based, не зависит от scale, works out of the box.

---

## Late Chunking: Бесплатное улучшение на 35-49%

Это **самая важная находка**.

Jina AI опубликовали whitepaper про late chunking. Суть: вместо того, чтобы эмбеддить каждый чанк независимо, сначала эмбеддим весь документ, **потом** чанкуем embeddings.

Звучит слишком хорошо. Я был скептичен.

Добавил **один параметр**:

```typescript
const embedding = await jinaEmbed(text, { late_chunking: true });
```

**Результат**: Retrieval failure rate упал с 3-4% до <2%. **ZERO additional cost**. BOOM.

**Почему работает?**

Обычный chunking:

```
Doc = "Neural networks learn through backpropagation. Backpropagation computes gradients."
Chunk 1: "Neural networks learn through backpropagation."
Chunk 2: "Backpropagation computes gradients."

Embed(Chunk 1) → embedding изолирован, теряет связь с "gradients"
Embed(Chunk 2) → embedding изолирован, теряет связь с "neural networks"
```

Late chunking:

```
Embed(Full Doc) → единый context-aware embedding
Затем chunk embedding matrix → сохраняет cross-chunk relationships
```

**Этот single parameter сэкономил бы месяцы архитектурной работы, если бы я узнал про него раньше.**

---

## Multilingual Optimization: 2.5 chars/token для русского

Jina-v3 поддерживает 89 языков. Но **token density различается**.

**Английский**: 4-5 chars/token
**Русский**: 2.5 chars/token

Это значит:
- 400-токеновый чанк на английском = ~1600-2000 chars
- 400-токеновый чанк на русском = ~1000 chars

Если использовать character-based splitting, русские чанки будут **больше по токенам**. Поэтому критично использовать `tiktoken` для token-aware splitting:

```typescript
const tokenSplitter = new RecursiveCharacterTextSplitter({
  chunk_size: 400,
  length_function: (text) => encode(text).length,  // tiktoken
});
```

Мы тестировали на смешанном корпусе (60% русский, 40% английский). С character-based splitting русские чанки выходили на ~600 токенов вместо 400. С `tiktoken` — ровно 400±10.

---

## 99.7% снижение latency через Redis caching

Первый embedding call: **2344ms**.
Cached retrieval: **7ms**.

Разница: **99.7%**.

Архитектура caching:

```typescript
import { createHash } from 'crypto';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

async function embedWithCache(text: string, metadata: object): Promise<number[]> {
  // Content-addressed caching: sha256(content + metadata)
  const contentHash = createHash('sha256')
    .update(text + JSON.stringify(metadata))
    .digest('hex');

  // Check Redis cache (24h TTL)
  const cached = await redis.get(`embedding:${contentHash}`);
  if (cached) {
    logger.info({ contentHash }, 'Embedding cache HIT');
    return JSON.parse(cached);
  }

  // Check database for duplicate content (deduplication)
  const { data: existing } = await supabase
    .from('document_chunks')
    .select('embedding')
    .eq('content_hash', contentHash)
    .limit(1);

  if (existing?.[0]?.embedding) {
    logger.info({ contentHash }, 'Embedding deduplication HIT');
    // Cache for future requests
    await redis.setex(
      `embedding:${contentHash}`,
      86400,  // 24 hours
      JSON.stringify(existing[0].embedding)
    );
    return existing[0].embedding;
  }

  // Call Jina-v3 API (cache MISS)
  logger.info({ contentHash }, 'Embedding cache MISS');
  const embedding = await jinaEmbed(text, { late_chunking: true });

  // Cache for 24 hours
  await redis.setex(
    `embedding:${contentHash}`,
    86400,
    JSON.stringify(embedding)
  );

  return embedding;
}
```

### Content-Addressed Caching

Ключевая идея: **хэшируем content + metadata**.

**Почему metadata?**

Потому что один и тот же content с разными metadata может иметь разные embeddings при late chunking (зависит от окружающего контекста).

### Deduplication Savings

Проверяем, был ли уже этот content embedded **до вызова API**:

```typescript
const { data: existing } = await supabase
  .from('document_chunks')
  .select('chunk_id, embedding')
  .eq('content_hash', contentHash)
  .limit(1);

if (existing) {
  // Reuse embedding, update only metadata
  return existing.embedding;
}
```

**Результат**: Embedding 500 chunks normally costs $0.01. С 60% cache hit rate → **$0.004 actual cost** (60% savings).

Комбинация content-hash caching + deduplication → **70% reduction в embedding API calls** для документов с общим контентом (учебники, API docs, reference materials).

---

## Production Metrics: До и После

| Metric | Before (Flat 800-token) | After (Hierarchical) | Improvement |
|--------|-------------------------|----------------------|-------------|
| Retrieval failure rate | 5-6% | <2% | **-67%** |
| Precision@5 | 70% | 85-90% | +15-20pp |
| Context sufficiency | 75% | 92% | +17pp |
| Avg latency (first call) | 2344ms | 2311ms | -1.4% |
| Avg latency (cached) | 2344ms | 7ms | **-99.7%** |
| Embedding cost per doc | $0.01 | $0.003 | **-70%** |
| Storage overhead | Baseline | +30% | Trade-off validated |

### Storage Trade-Off Math

**Вопрос**: Стоит ли +30% storage overhead?

**Анализ**:
- Иерархический RAG: +30% storage (храним parent и child chunks)
- Стоимость неудачного retrieval: 3x (новый API call, потраченные токены, ожидание пользователя)
- Break-even: 10% failure rate (0.30 storage cost / 3.0 regeneration cost)
- **Наш failure rate: <2%** → ROI validated (сэкономили 5x больше на regeneration, чем потратили на storage)

---

## Конкурентный контекст

### vs LlamaIndex

**LlamaIndex**: Fixed chunk sizes с overlap.
**Мы**: Adaptive hierarchical chunking с heading-aware boundaries.

LlamaIndex не учитывает структуру документа. Если параграф разрезан посередине, контекст теряется.

### vs Pinecone RAG

**Pinecone RAG**: Standard approach — выбор между precision и context.
**Мы**: Решаем обе проблемы через parent-child architecture.

Pinecone рекомендует фиксированные размеры чанков (512 tokens), что работает для simple use cases, но недостаточно для technical documentation с complex hierarchies.

### vs Industry Benchmarks (2024 RAG Report)

**Типичная retrieval accuracy**: 60-75% (Precision@5).
**Мы**: 85-90%.

**Late chunking advantage**: Недоступен в standard RAG libraries. Exclusive Jina-v3 feature, который мы leveraged для 35-49% improvement at zero cost.

---

## Lessons Learned: Что бы я сделал иначе

### 1. Узнал бы про late chunking раньше

Я потратил **3 месяца** на архитектуру hierarchical chunking. Late chunking дал **comparable improvement с одним параметром**. Если бы узнал раньше, начал бы с late chunking + flat chunks, потом добавил бы hierarchy только если нужно.

### 2. Тестировал бы на production data с первого дня

Мои первые тесты были на synthetic datasets (10 documents, 50 queries). Когда перешёл на production (500+ documents, 5000+ queries), обнаружил **совершенно другие failure modes**.

Synthetic data не показывает:
- Duplicate content (deduplication savings)
- Query diversity (long-tail queries)
- Real user intent (vague vs precise queries)

**Совет**: Соберите хотя бы 100 real user queries перед архитектурными решениями.

### 3. Измерял бы Context Sufficiency, а не только Precision

Первые 2 месяца я оптимизировал только Precision@5. Достиг 85%. Думал, что победил. Потом понял, что **LLM генерируют плохой контент**, потому что извлечённых чанков недостаточно.

**Метрика Context Sufficiency**: Может ли LLM сгенерировать качественный ответ на основе извлечённых чанков? Измеряется через LLM-as-judge (GPT-4 оценивает completeness ответа).

### 4. Не недооценивал бы caching

Первая версия вообще без caching. Latency 2-3 секунды на запрос. Пользователи жаловались. Добавил Redis → latency упал до 7ms для cached queries.

**ROI caching огромен**: 99.7% latency reduction, 70% cost reduction. Реализация заняла **1 день**.

---

## Disclaimer: Expected Pushback

Я понимаю, что эта статья вызовет pushback от разработчиков.

"30% storage overhead — это слишком дорого."
"Late chunking — это хак, а не реальная архитектура."
"Hybrid search — overengineering, semantic search достаточно."

Моё мнение: Эта реакция больше про **страх, смешанный с высокомерием**, чем про технические аргументы.

**Страх**: "Если AI может делать мою работу, что будет со мной?"
**Высокомерие**: "Только люди могут писать *настоящий* код, AI — это игрушка."

**Реальность**: AI не заменяет хороших разработчиков. Он их усиливает. RAG-системы не про замену программистов — про **removing repetitive tasks**, автоматизацию quality checks, сохранение контекста, чтобы разработчики могли фокусироваться на архитектуре и сложных проблемах.

Если не согласны — нормально. Клонируйте репо, попробуйте, потом скажите, где я ошибся. Я предпочитаю технические аргументы эмоциональным реакциям.

---

## Как воспроизвести архитектуру

**1. Установите зависимости**:

```bash
npm install langchain @qdrant/js-client-rest gpt-tokenizer natural ioredis uuid
```

**2. Используйте код выше** для hierarchical chunking + hybrid search + caching.

**3. Конфигурация**:

```typescript
// .env
JINA_API_KEY=your_key
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379
```

**4. Создайте Qdrant collection**:

```typescript
await qdrant.createCollection('document_chunks', {
  vectors: {
    size: 768,  // Jina-v3 embedding dimension
    distance: 'Cosine',
  },
});
```

**5. Индексируйте документы**:

```typescript
const chunks = await createHierarchicalChunks(markdown);

for (const chunk of chunks) {
  const embedding = await embedWithCache(chunk.content, chunk.metadata);
  await qdrant.upsert('document_chunks', {
    points: [{
      id: chunk.chunk_id,
      vector: embedding,
      payload: {
        content: chunk.content,
        parent_content: chunk.parent_content,
        metadata: chunk.metadata,
      },
    }],
  });
}
```

**6. Запрос**:

```typescript
const results = await hybridSearch("Explain backpropagation algorithm", 5);
console.log(results.map(r => r.content));  // 1500-token parents
```

---

## Contact & Feedback

### 📱 Telegram

**Channel** (редкие, но интересные посты): https://t.me/maslennikovigor
Заходите, читайте мои мысли и статьи. Я не постю часто, но когда делаю — это стоит внимания.

**Direct Contact**: https://t.me/maslennikovig
Нужно поговорить? Пишите мне напрямую. Всегда рад пообщаться.

### 💬 Feedback: Я максимально открыт

**Я хотел бы услышать**:
- **Критику** — Что не так с этим подходом? Где слабые места?
- **Идеи** — Какие features нужно добавить? Чего не хватает?
- **Предложения** — Как улучшить, оптимизировать или рефакторить систему?
- **Вопросы** — Что-то непонятно? Спрашивайте.

**Каналы для фидбека**:
- **GitHub Issues**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/issues (for bugs, features)
- **GitHub Discussions**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/discussions (for ideas, questions)
- **Telegram**: https://t.me/maslennikovig (for direct conversation)

**Tone**: Super open to constructive dialogue. No ego, just want to make this better.

---

## Заключение

Hierarchical RAG architecture решает fundamental trade-off между precision и context sufficiency.

**Key takeaways**:
1. **Index small (400 tokens), retrieve large (1500 tokens)** через parent-child chunking
2. **Late chunking** даёт 35-49% improvement бесплатно (один параметр)
3. **Hybrid search** (dense + sparse) покрывает semantic + keyword matching
4. **Content-addressed caching** + deduplication снижают cost на 70%
5. **Storage overhead (+30%)** окупается через снижение failure rate (-67%)

Я построил эту систему за последние 2 года в AI Dev Team. Протестировал на реальных клиентских проектах. Снизил ошибки извлечения на 67%. Достиг Precision@5 85-90% (vs industry 60-75%).

Если вы строите RAG-систему — попробуйте этот подход. Клонируйте код, запускайте, измеряйте метрики. Потом скажите, где я ошибся.

**GitHub**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit
**NPM**: `npm install -g claude-code-orchestrator-kit`

---

**Автор**: Игорь Масленников
**Компания**: DNA IT / AI Dev Team
**Опыт**: В IT с 2013 года, последние 2 года — AI-системы
**Telegram**: https://t.me/maslennikovig
