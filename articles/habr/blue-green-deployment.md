---
platform: habr
title: "0 секунд простоя, 30 секунд откат: Blue/Green на одном сервере"
subtitle: "Как настроить zero-downtime деплой с docker-compose и nginx без Kubernetes"
author: Igor Maslennikov
date: 2026-01-18
tags: [Blue-Green, DevOps, CI/CD, Docker, GitHub Actions, Deployment, Zero-Downtime]
language: ru
---

# 0 секунд простоя, 30 секунд откат: Blue/Green на одном сервере

## Боль

Признаюсь: я деплоил в 3 часа ночи. Выбирал время, когда пользователей меньше всего. Откладывал релизы на выходные. Держал в браузере закладку с командой отката. Это классика.

**Проблема очевидна:**
- Деплой = downtime (5-30 секунд, пока контейнеры перезапускаются)
- Откат = паника (остановить новую версию, запустить старую, проверить, дышать в пакет)
- Тестирование на dev ≠ поведение на stage (разные очереди, разные данные, разные условия)
- Страх деплоить в рабочее время = накопление изменений = большие релизы = ещё больший страх

В [предыдущей статье](https://habr.com/ru/articles/XXX/) я обещал рассказать про Blue/Green и изоляцию окружений. Выполняю обещание.

## Что я сделал

**Коротко:**
- Настроил **Dev и Staging окружения** (полная изоляция, разные очереди, разные данные)
- Добавил **Blue/Green деплой** для Staging (zero-downtime, откат за 30 секунд)
- Автоматизировал через **CI/CD** (8 стадий, параллельные проверки, автоматический откат)
- Деплою **в любое время дня**. Спокойно.

**Результаты:**
- Деплой: 10-15 минут от `git push` до production
- Downtime: 0 секунд (пользователи не замечают)
- Откат: 30 секунд (если что-то пошло не так)
- Страх деплоить: нет

## Disclaimer: Expected Pushback

Я понимаю, что эта статья вызовет критику. "Blue/Green — это база, чему тут учить?", "Зачем такая сложность для небольшого проекта?", "У нас Kubernetes, зачем нам docker-compose?"

**Моя позиция**: Blue/Green — действительно не новая идея. Но большинство статей показывают теорию или корпоративные решения с Kubernetes. Я показываю **рабочую реализацию на одном сервере с docker-compose**, которую можно скопировать и запустить.

Если у вас Kubernetes — отлично, там Blue/Green встроен. Если у вас Vercel/Netlify — вообще не проблема. Эта статья для тех, у кого **один сервер, docker-compose, и желание деплоить без страха**.

Если вы знаете лучший способ — напишите в комментариях. Я всегда открыт к улучшениям.

---

## Архитектура: Dev, Staging, Blue/Green

### Общая схема

```
┌─────────────────────────────────────────────────────────────────┐
│                        Production Server                         │
│                    (8 CPU, 11GB RAM)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  Shared Infrastructure                      │ │
│  │    docker-compose.infra.yml (runs continuously)            │ │
│  │                                                             │ │
│  │  ┌─────────┐  ┌──────────────┐  ┌─────────────────────┐   │ │
│  │  │  Redis  │  │ Docling MCP  │  │  Workers (stages)   │   │ │
│  │  │  :6379  │  │    :8000     │  │  1-6, stage7        │   │ │
│  │  └─────────┘  └──────────────┘  └─────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │    BLUE Slot        │    │    GREEN Slot       │            │
│  │  docker-compose     │    │  docker-compose     │            │
│  │  .app.yml           │    │  .app.yml           │            │
│  │                     │    │                     │            │
│  │  ┌───────────────┐  │    │  ┌───────────────┐  │            │
│  │  │ web (Next.js) │  │    │  │ web (Next.js) │  │            │
│  │  │    :3001      │  │    │  │    :3002      │  │            │
│  │  └───────────────┘  │    │  └───────────────┘  │            │
│  │  ┌───────────────┐  │    │  ┌───────────────┐  │            │
│  │  │ api (Express) │  │    │  │ api (Express) │  │            │
│  │  │    :4001      │  │    │  │    :4002      │  │            │
│  │  └───────────────┘  │    │  └───────────────┘  │            │
│  └─────────────────────┘    └─────────────────────┘            │
│           ▲                          ▲                          │
│           │                          │                          │
│           └──────────┬───────────────┘                          │
│                      │                                          │
│              ┌───────────────┐                                  │
│              │    NGINX      │                                  │
│              │  (switches    │                                  │
│              │  traffic)     │                                  │
│              └───────────────┘                                  │
│                      │                                          │
└──────────────────────┼──────────────────────────────────────────┘
                       │
              ai.megacampus.ru
```

### Стратегия окружений

| Domain | Environment | Branch | Deploy Strategy | Назначение |
|--------|-------------|--------|-----------------|------------|
| dev.ai.megacampus.ru | Dev | develop | Simple rolling | Быстрая итерация, тестирование |
| ai.megacampus.ru | Staging | master | Blue/Green | Zero-downtime, откат |
| TBD | Production | TBD | Blue/Green | Будущее расширение |

**Почему такая схема:**

**Dev**: Простой деплой (docker-compose restart). Downtime на 10-20 секунд — не критично, это окружение для разработки. Главное — скорость обновления.

**Staging**: Blue/Green деплой. Здесь проверяем финальные изменения перед production. Нужен zero-downtime и моментальный откат на случай проблем.

**Production** (пока нет): Когда появится, будет использовать ту же Blue/Green стратегию, что и Staging.

### Распределение портов

| Environment | Web Port | API Port |
|-------------|----------|----------|
| Blue (Staging) | 3001 | 4001 |
| Green (Staging) | 3002 | 4002 |
| Dev | 3010 | 4010 |

---

## Blue/Green: как это работает

### Принцип

**Blue и Green** — два идентичных слота для приложения:
- **Blue**: Текущая активная версия (обслуживает пользователей)
- **Green**: Новая версия (деплоится, проверяется)

**Процесс деплоя:**
1. Определяем активный цвет (читаем `active_color` файл)
2. Деплоим новую версию в **неактивный** слот
3. Проверяем здоровье (health checks)
4. **Переключаем nginx** на новый слот (мгновенно)
5. Останавливаем старый слот

**Ключевое**: Пользователи всё это время видят **стабильную версию**. Переключение трафика занимает ~100ms (nginx reload).

### Скрипт деплоя (упрощённо)

Полный скрипт: `scripts/deploy_blue_green.sh` (145 строк)

**Основная логика:**

```bash
#!/bin/bash
set -e

ENV=${1:-production}
TAG=${2:-latest}
BASE_PATH="/opt/megacampus"

# 1. Determine Active Color (Default to blue if first run)
if [ -f "$BASE_PATH/active_color" ]; then
    CURRENT_COLOR=$(cat "$BASE_PATH/active_color")
else
    CURRENT_COLOR="blue"
fi

# 2. Calculate New Color
if [ "$CURRENT_COLOR" == "blue" ]; then
    NEW_COLOR="green"
    NEW_WEB_PORT=3002
    NEW_API_PORT=4002
else
    NEW_COLOR="blue"
    NEW_WEB_PORT=3001
    NEW_API_PORT=4001
fi

echo "Current: $CURRENT_COLOR"
echo "Target:  $NEW_COLOR (web:$NEW_WEB_PORT, api:$NEW_API_PORT)"

# 3. Ensure Infrastructure is Running
docker compose -f "$BASE_PATH/docker-compose.infra.yml" up -d

# 4. Prepare Environment Configuration
cp "$BASE_PATH/.env.$ENV" "$BASE_PATH/.env.$NEW_COLOR"
{
    echo "COLOR=$NEW_COLOR"
    echo "WEB_PORT=$NEW_WEB_PORT"
    echo "API_PORT=$NEW_API_PORT"
    echo "COMPOSE_PROJECT_NAME=megacampus-$NEW_COLOR"
} >> "$BASE_PATH/.env.$NEW_COLOR"

# 5. Pull and Start New Version
docker compose -f "$BASE_PATH/docker-compose.app.yml" \
    --env-file "$BASE_PATH/.env.$NEW_COLOR" pull
docker compose -f "$BASE_PATH/docker-compose.app.yml" \
    --env-file "$BASE_PATH/.env.$NEW_COLOR" up -d --remove-orphans

# 6. Health Check (API + Web)
API_HEALTHY=false
for i in {1..12}; do
    if curl -s -f "http://localhost:$NEW_API_PORT/health" > /dev/null 2>&1; then
        echo "API health check passed!"
        API_HEALTHY=true
        break
    fi
    echo "Waiting for API... ($i/12)"
    sleep 5
done

WEB_HEALTHY=false
for i in {1..12}; do
    if curl -s -f "http://localhost:$NEW_WEB_PORT" > /dev/null 2>&1; then
        echo "Web health check passed!"
        WEB_HEALTHY=true
        break
    fi
    echo "Waiting for Web... ($i/12)"
    sleep 5
done

# 7. Rollback if Health Check Failed
if [ "$API_HEALTHY" = false ] || [ "$WEB_HEALTHY" = false ]; then
    echo "Health check failed!"
    docker compose -f "$BASE_PATH/docker-compose.app.yml" \
        --env-file "$BASE_PATH/.env.$NEW_COLOR" down
    exit 1
fi

# 8. Switch Traffic
sed -e "s/{{WEB_PORT}}/$NEW_WEB_PORT/g" \
    -e "s/{{API_PORT}}/$NEW_API_PORT/g" \
    "$BASE_PATH/nginx.conf.template" | sudo tee /etc/nginx/sites-enabled/megacampus > /dev/null

sudo nginx -t && sudo nginx -s reload

# 9. Update State
echo "$NEW_COLOR" > "$BASE_PATH/active_color"

# 10. Stop Old Version
docker compose -f "$BASE_PATH/docker-compose.app.yml" \
    -p "megacampus-$CURRENT_COLOR" down

echo "Deployment Complete! Active: $NEW_COLOR"
```

### Что происходит под капотом

**1. State Tracking**

Файл `active_color` хранит текущий активный слот:
```bash
$ cat /opt/megacampus/active_color
blue
```

При следующем деплое скрипт читает этот файл и деплоит в **green**.

**2. Environment Isolation**

Каждый слот получает свой `.env.$COLOR` файл с уникальными портами и project name:

```bash
# .env.blue
COLOR=blue
WEB_PORT=3001
API_PORT=4001
COMPOSE_PROJECT_NAME=megacampus-blue

# .env.green
COLOR=green
WEB_PORT=3002
API_PORT=4002
COMPOSE_PROJECT_NAME=megacampus-green
```

**3. Health Checks**

Проверяем **оба сервиса** (API + Web):
- **12 попыток**, интервал 5 секунд
- **Timeout**: 60 секунд общий
- Проверки:
  - API: `curl http://localhost:$PORT/health` (возвращает JSON с версией, uptime)
  - Web: `curl http://localhost:$PORT` (проверка статуса 200)

Если хотя бы одна проверка не прошла — **откат** (останавливаем новый слот, выходим с ошибкой).

**4. Traffic Switch**

Nginx конфигурация использует **template** с подстановкой портов:

```nginx
# nginx.conf.template
upstream web_backend {
    server localhost:{{WEB_PORT}};
}

upstream api_backend {
    server localhost:{{API_PORT}};
}

server {
    listen 443 ssl;
    server_name ai.megacampus.ru;

    location / {
        proxy_pass http://web_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://api_backend;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }
}
```

При деплое:
```bash
sed -e "s/{{WEB_PORT}}/3002/g" \
    -e "s/{{API_PORT}}/4002/g" \
    nginx.conf.template > /etc/nginx/sites-enabled/megacampus

nginx -t  # Проверка конфигурации
nginx -s reload  # Применение (без downtime)
```

**Reload nginx**: ~100ms, пользователи не замечают переключения.

### Откат (Rollback)

Скрипт: `scripts/rollback_blue_green.sh` (138 строк)

**Логика:**

```bash
#!/bin/bash
set -e

BASE_PATH="/opt/megacampus"

# 1. Determine Current Active Color
CURRENT_COLOR=$(cat "$BASE_PATH/active_color")

# 2. Calculate Target (Previous) Color
if [ "$CURRENT_COLOR" == "blue" ]; then
    TARGET_COLOR="green"
    TARGET_WEB_PORT=3002
    TARGET_API_PORT=4002
else
    TARGET_COLOR="blue"
    TARGET_WEB_PORT=3001
    TARGET_API_PORT=4001
fi

echo "Rollback: $CURRENT_COLOR → $TARGET_COLOR"

# 3. Ensure Target is Running
docker compose -f "$BASE_PATH/docker-compose.app.yml" \
    --env-file "$BASE_PATH/.env.$TARGET_COLOR" up -d --remove-orphans

# 4. Health Check (6 retries, 30s timeout)
# ... (аналогично deploy_blue_green.sh, но 6 попыток вместо 12)

# 5. Switch Traffic
sed -e "s/{{WEB_PORT}}/$TARGET_WEB_PORT/g" \
    -e "s/{{API_PORT}}/$TARGET_API_PORT/g" \
    "$BASE_PATH/nginx.conf.template" | sudo tee /etc/nginx/sites-enabled/megacampus > /dev/null

sudo nginx -t && sudo nginx -s reload

# 6. Update State
echo "$TARGET_COLOR" > "$BASE_PATH/active_color"

# 7. Stop Broken Version
docker compose -f "$BASE_PATH/docker-compose.app.yml" \
    -p "megacampus-$CURRENT_COLOR" down

echo "Rollback Complete! Active: $TARGET_COLOR"
```

**Timing:**
- Если предыдущая версия ещё запущена: **~10 секунд**
- Если нужно поднять контейнеры: **~30 секунд**

**Вызов:**
```bash
ssh megacampus-prod "bash /opt/megacampus/scripts/rollback_blue_green.sh"
```

---

## Изоляция окружений: Dev vs Staging

### Зачем нужен отдельный Dev?

**Проблема**: Если dev и staging используют **одну и ту же инфраструктуру**, изменения на dev могут сломать staging:
- Общая **BullMQ очередь** → задачи с dev попадают в staging (или наоборот)
- Общая **папка uploads** → тестовые файлы смешиваются с реальными
- Общая **база данных** → миграции на dev ломают staging

**Решение**: Полная изоляция через отдельные docker-compose конфигурации и переменные окружения.

### Изоляция очередей (BullMQ)

**Dev:**
```bash
# .env.dev
BULLMQ_QUEUE_NAME=course-generation-dev
```

**Staging:**
```bash
# .env.production
BULLMQ_QUEUE_NAME=course-generation-prod
```

**Результат**: Задачи с dev не попадают в staging. Можно тестировать генерацию курсов на dev, не боясь затронуть production.

### Изоляция данных

**Dev:**
```bash
# docker-compose.dev.yml
volumes:
  - ./uploads-dev:/app/uploads
```

**Staging:**
```bash
# docker-compose.app.yml
volumes:
  - ./uploads:/app/uploads
```

**Результат**: Тестовые файлы с dev не смешиваются со staging файлами.

### Изоляция проектов Docker Compose

**Dev:**
```bash
# .env.dev
COMPOSE_PROJECT_NAME=megacampus-dev
```

**Staging (Blue/Green):**
```bash
# .env.blue
COMPOSE_PROJECT_NAME=megacampus-blue

# .env.green
COMPOSE_PROJECT_NAME=megacampus-green
```

**Результат**: Docker видит это как **разные проекты**. Можно остановить dev, не затронув staging.

### Разделение ресурсов

**Dev** (меньше ресурсов, для быстрых итераций):
```yaml
# docker-compose.dev.yml
services:
  web-dev:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
  api-dev:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

**Staging** (полные ресурсы, как в production):
```yaml
# docker-compose.app.yml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

**Результат**: Dev использует **2 CPU, 2GB RAM**. Staging (Blue + Green) использует **4 CPU, 4GB RAM** (во время деплоя), затем освобождает половину.

---

## CI/CD Pipeline: Автоматизация деплоя

### Общая схема (8 стадий)

```
Push to branch
      │
      ▼
┌─────────────────┐
│ Stage 1: Setup  │  Install pnpm dependencies with caching
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 2: Parallel Checks                                     │
│   ├─ Lint (5min timeout)                                    │
│   ├─ Type-check (10min timeout)                             │
│   ├─ Security audit (5min timeout)                          │
│   └─ Tests (10min timeout, skippable)                       │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Stage 3: Build  │  Build all packages (shared-types, platform, web)
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Stage 4: CI Gate    │  Verify type-check + build passed
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 5: Docker Builds (parallel matrix)                     │
│   ├─ ghcr.io/maslennikov-ig/mc-2/web:{branch}               │
│   └─ ghcr.io/maslennikov-ig/mc-2/api:{branch}               │
│   (with gha cache for fast rebuilds)                         │
└─────────────────────────────────────────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌─────────────┐
│ master  │ │  develop    │
│         │ │             │
│Stage 6: │ │Stage 7b:    │
│Deploy   │ │Deploy Dev   │
│Prod     │ │             │
│(B/G)    │ │(simple)     │
└────┬────┘ └──────┬──────┘
     │             │
     │  ┌──────────┘
     │  │
     ▼  ▼
┌──────────────────────┐
│ Stage 7: Rollback    │  (only if deploy fails)
└──────────────────────┘
         │
         ▼
┌──────────────────────┐
│ Stage 8: Notify      │  Telegram notification
└──────────────────────┘
```

### Stage 1: Setup

**Цель**: Установить зависимости и закэшировать для последующих стадий.

```yaml
setup:
  name: Setup Dependencies
  runs-on: ubuntu-latest
  timeout-minutes: 10

  steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Setup pnpm
      uses: pnpm/action-setup@v4
      with:
        version: 8.15.0

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: 20
        cache: 'pnpm'

    - name: Get pnpm store directory
      shell: bash
      run: echo "STORE_PATH=$(pnpm store path --silent)" >> $GITHUB_ENV

    - name: Cache pnpm store
      uses: actions/cache@v4
      with:
        path: ${{ env.STORE_PATH }}
        key: ${{ runner.os }}-pnpm-store-${{ hashFiles('**/pnpm-lock.yaml') }}
        restore-keys: |
          ${{ runner.os }}-pnpm-store-

    - name: Install dependencies
      run: pnpm install --frozen-lockfile
```

**Кэширование**: pnpm store сохраняется и переиспользуется в других jobs. **Экономия**: 2-3 минуты на каждой стадии.

### Stage 2: Parallel Checks

**Цель**: Запустить lint, type-check, security audit, tests **параллельно**.

**Ключевой момент**: `needs: setup` означает, что все jobs в Stage 2 начнутся **одновременно** после завершения setup.

```yaml
lint:
  name: Lint
  runs-on: ubuntu-latest
  needs: setup
  timeout-minutes: 5
  steps:
    # Restore cache from setup
    - uses: actions/checkout@v4
    - uses: pnpm/action-setup@v4
    - uses: actions/setup-node@v4
    - name: Restore pnpm store
      uses: actions/cache@v4
      # ... (restore cache)
    - name: Install dependencies
      run: pnpm install --frozen-lockfile
    - name: Run lint
      run: pnpm lint
      continue-on-error: true

type-check:
  name: Type Check
  runs-on: ubuntu-latest
  needs: setup
  timeout-minutes: 10
  steps:
    # ... (аналогично lint)
    - name: Build shared packages
      run: |
        pnpm --filter @megacampus/shared-types build
        pnpm --filter @megacampus/shared-logger build
    - name: Run type check
      run: pnpm type-check

security:
  name: Security Audit
  runs-on: ubuntu-latest
  needs: setup
  timeout-minutes: 5
  steps:
    # ... (аналогично lint)
    - name: Run security audit
      run: pnpm audit --audit-level=high
      continue-on-error: true

test:
  name: Run Tests
  runs-on: ubuntu-latest
  needs: setup
  if: ${{ !inputs.skip_tests }}
  timeout-minutes: 10
  steps:
    # ... (аналогично type-check)
    - name: Run tests
      run: pnpm test
      continue-on-error: true
```

**Параллелизм**: Все 4 проверки выполняются **одновременно**. Общее время = max(lint, type-check, security, test) ≈ **10 минут** (вместо суммы ~30 минут).

**continue-on-error**: Lint, security, tests могут **упасть**, но pipeline продолжится. Type-check — **блокирующий** (если упал, pipeline остановится на Stage 4).

### Stage 3: Build

**Цель**: Собрать все пакеты (shared-types, shared-logger, course-gen-platform, web).

```yaml
build:
  name: Build Packages
  runs-on: ubuntu-latest
  needs: [type-check]
  timeout-minutes: 15

  steps:
    # ... (restore cache)
    - name: Build shared packages
      run: |
        pnpm --filter @megacampus/shared-types build
        pnpm --filter @megacampus/shared-logger build

    - name: Build course-gen-platform
      run: pnpm --filter @megacampus/course-gen-platform build

    - name: Build web
      run: pnpm --filter @megacampus/web build
      env:
        NEXT_PUBLIC_SUPABASE_URL: https://placeholder.supabase.co
        NEXT_PUBLIC_SUPABASE_ANON_KEY: placeholder-anon-key
        SUPABASE_SERVICE_ROLE_KEY: placeholder-service-key
        SUPABASE_JWT_SECRET: placeholder-jwt-secret
```

**Placeholder env**: Next.js требует переменные окружения во время build. Используем заглушки (реальные секреты подставляются в Docker runtime).

### Stage 4: CI Gate

**Цель**: Убедиться, что **критичные проверки прошли** (type-check, build). Если нет — останавливаем pipeline.

```yaml
ci-success:
  name: CI Success
  runs-on: ubuntu-latest
  needs: [lint, type-check, security, build]
  if: always()

  steps:
    - name: Check CI status
      run: |
        if [ "${{ needs.type-check.result }}" != "success" ]; then
          echo "Type check failed!"
          exit 1
        fi
        if [ "${{ needs.build.result }}" != "success" ]; then
          echo "Build failed!"
          exit 1
        fi
        echo "All critical CI checks passed!"
```

**Логика**:
- Lint, security, tests могут упасть → pipeline продолжается
- Type-check, build упали → **pipeline останавливается**

### Stage 5: Docker Builds (Matrix)

**Цель**: Собрать **web и api** Docker images **параллельно** и отправить в GitHub Container Registry.

```yaml
build-docker:
  name: Build Docker - ${{ matrix.image }}
  runs-on: ubuntu-latest
  needs: [ci-success]
  if: (github.ref == 'refs/heads/master' || github.ref == 'refs/heads/develop') || inputs.force_deploy
  timeout-minutes: 20

  strategy:
    fail-fast: false
    matrix:
      include:
        - image: web
          dockerfile: ./packages/web/Dockerfile
          context: .
        - image: api
          dockerfile: ./packages/course-gen-platform/Dockerfile
          context: .

  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to GHCR
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ghcr.io/${{ github.repository }}/${{ matrix.image }}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: ${{ matrix.context }}
        file: ${{ matrix.dockerfile }}
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha,scope=${{ matrix.image }}
        cache-to: type=gha,mode=max,scope=${{ matrix.image }}
        build-args: |
          NODE_VERSION=20
          BUILD_DATE=${{ github.event.head_commit.timestamp }}
          VCS_REF=${{ github.sha }}
```

**Matrix Strategy**: GitHub Actions запускает **2 job'а параллельно** (web, api). Общее время ≈ **3-5 минут** (с кэшированием).

**GitHub Actions Cache**: `cache-from: type=gha` переиспользует слои из предыдущих билдов. **Speedup**: ~70% (3 минуты вместо 10).

**Tags**:
- `ghcr.io/maslennikov-ig/mc-2/web:master` (branch name)
- `ghcr.io/maslennikov-ig/mc-2/web:master-a1b2c3d` (branch + short SHA)
- `ghcr.io/maslennikov-ig/mc-2/web:latest` (если master)

### Stage 6: Deploy to Staging (Blue/Green)

**Цель**: Задеплоить на `ai.megacampus.ru` (Staging) с Blue/Green стратегией.

```yaml
deploy:
  name: Deploy to Production
  runs-on: ubuntu-latest
  needs: [build-docker]
  if: github.ref == 'refs/heads/master' || inputs.force_deploy
  timeout-minutes: 10
  environment:
    name: production
    url: https://ai.megacampus.ru

  steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Setup SSH
      run: |
        mkdir -p ~/.ssh
        echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/deploy_key
        chmod 600 ~/.ssh/deploy_key
        ssh-keyscan -H ${{ env.DEPLOY_HOST }} >> ~/.ssh/known_hosts

    - name: Copy deployment files
      run: |
        scp -i ~/.ssh/deploy_key \
          docker-compose.infra.yml \
          docker-compose.app.yml \
          docker-compose.production.yml \
          nginx-megacampus.conf \
          nginx.conf.template \
          ${{ env.DEPLOY_USER }}@${{ env.DEPLOY_HOST }}:${{ env.DEPLOY_PATH }}/

        scp -i ~/.ssh/deploy_key \
          scripts/deploy_blue_green.sh \
          scripts/rollback_blue_green.sh \
          ${{ env.DEPLOY_USER }}@${{ env.DEPLOY_HOST }}:${{ env.DEPLOY_PATH }}/scripts/

    - name: Create .env.production
      run: |
        ssh -i ~/.ssh/deploy_key \
          ${{ env.DEPLOY_USER }}@${{ env.DEPLOY_HOST }} \
          "cat > ${{ env.DEPLOY_PATH }}/.env.production << 'ENVEOF'
        NODE_ENV=production
        SUPABASE_URL=${{ secrets.SUPABASE_URL }}
        SUPABASE_ANON_KEY=${{ secrets.SUPABASE_ANON_KEY }}
        REDIS_URL=redis://redis:6379
        # ... (остальные переменные)
        ENVEOF
        chmod 600 ${{ env.DEPLOY_PATH }}/.env.production"

    - name: Deploy
      run: |
        ssh -i ~/.ssh/deploy_key \
          ${{ env.DEPLOY_USER }}@${{ env.DEPLOY_HOST }} \
          "cd ${{ env.DEPLOY_PATH }} && GITHUB_TOKEN='${{ secrets.GITHUB_TOKEN }}' GITHUB_ACTOR='${{ github.actor }}' bash scripts/deploy_blue_green.sh production latest"

    - name: Verify deployment
      run: |
        echo "Waiting for services..."
        sleep 30

        # Check via HTTPS
        if curl -f -s https://ai.megacampus.ru/api/health > /dev/null; then
          echo "Web service healthy"
        else
          echo "Web health check failed!"
          exit 1
        fi

        # Get active color to determine API port
        ACTIVE_COLOR=$(ssh -i ~/.ssh/deploy_key \
          ${{ env.DEPLOY_USER }}@${{ env.DEPLOY_HOST }} \
          "cat ${{ env.DEPLOY_PATH }}/active_color")

        if [ "$ACTIVE_COLOR" = "blue" ]; then
          API_PORT=4001
        else
          API_PORT=4002
        fi

        if ssh -i ~/.ssh/deploy_key \
          ${{ env.DEPLOY_USER }}@${{ env.DEPLOY_HOST }} \
          "curl -f -s http://localhost:$API_PORT/health" > /dev/null; then
          echo "API service healthy"
        else
          echo "API health check failed!"
          exit 1
        fi

    - name: Cleanup SSH
      if: always()
      run: rm -f ~/.ssh/deploy_key
```

**Процесс:**
1. Копируем docker-compose файлы, nginx конфигурацию, скрипты деплоя на сервер
2. Создаём `.env.production` с секретами (хранятся в GitHub Secrets)
3. Запускаем `deploy_blue_green.sh production latest`
4. Ждём 30 секунд
5. Проверяем здоровье через HTTPS и localhost

**SSH Key**: Хранится в GitHub Secrets (`DEPLOY_SSH_KEY`), доступен только в production environment.

### Stage 7b: Deploy to Dev (Simple)

**Цель**: Задеплоить на `dev.ai.megacampus.ru` с простой стратегией (no Blue/Green).

```yaml
deploy-dev:
  name: Deploy to Dev
  runs-on: ubuntu-latest
  needs: [build-docker]
  if: github.ref == 'refs/heads/develop' && github.event_name == 'push'
  timeout-minutes: 20
  environment:
    name: development
    url: https://dev.ai.megacampus.ru

  steps:
    # ... (аналогично deploy, но проще)
    - name: Deploy
      run: |
        ssh -i ~/.ssh/deploy_key \
          ${{ env.DEPLOY_USER }}@${{ env.DEPLOY_HOST }} \
          "cd ${{ env.DEPLOY_PATH }} && GITHUB_TOKEN='${{ secrets.GITHUB_TOKEN }}' GITHUB_ACTOR='${{ github.actor }}' bash scripts/deploy_dev.sh"
```

**deploy_dev.sh** (упрощённо):
```bash
docker compose -f docker-compose.dev.yml pull
docker compose -f docker-compose.dev.yml up -d --remove-orphans
```

**Downtime**: ~10-20 секунд (пока контейнеры перезапускаются). Это нормально для dev окружения.

### Stage 7: Rollback (автоматический)

**Цель**: Откатиться, если деплой упал.

```yaml
rollback:
  name: Rollback
  runs-on: ubuntu-latest
  needs: [deploy]
  if: failure()
  timeout-minutes: 10

  steps:
    - uses: actions/checkout@v4

    - name: Setup SSH
      run: |
        mkdir -p ~/.ssh
        echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/deploy_key
        chmod 600 ~/.ssh/deploy_key
        ssh-keyscan -H ${{ env.DEPLOY_HOST }} >> ~/.ssh/known_hosts

    - name: Execute rollback
      run: |
        ssh -i ~/.ssh/deploy_key \
          ${{ env.DEPLOY_USER }}@${{ env.DEPLOY_HOST }} \
          "cd ${{ env.DEPLOY_PATH }} && bash scripts/rollback_blue_green.sh"

    - name: Cleanup SSH
      if: always()
      run: rm -f ~/.ssh/deploy_key
```

**Trigger**: `if: failure()` означает, что job запускается **только если deploy упал**.

**Процесс**:
1. Подключаемся по SSH
2. Запускаем `rollback_blue_green.sh`
3. Скрипт переключает трафик на предыдущую версию

**Timing**: ~30-60 секунд от обнаружения проблемы до отката.

### Stage 8: Notify (Telegram)

**Цель**: Отправить уведомление в Telegram о результате деплоя.

```yaml
notify:
  name: Notify
  runs-on: ubuntu-latest
  needs: [deploy, deploy-dev]
  if: always() && (github.ref == 'refs/heads/master' || github.ref == 'refs/heads/develop')

  steps:
    - name: Send Telegram notification
      env:
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        DEPLOY_PROD_RESULT: ${{ needs.deploy.result }}
        DEPLOY_DEV_RESULT: ${{ needs.deploy-dev.result }}
        COMMIT_SHA: ${{ github.sha }}
        ACTOR: ${{ github.actor }}
        BRANCH: ${{ github.ref_name }}
        RUN_URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
      run: |
        # Determine which deploy ran and its result
        if [ "$BRANCH" == "master" ]; then
          DEPLOY_RESULT="$DEPLOY_PROD_RESULT"
          ENV_NAME="Staging"
          ENV_URL="https://ai.megacampus.ru"
        else
          DEPLOY_RESULT="$DEPLOY_DEV_RESULT"
          ENV_NAME="Dev"
          ENV_URL="https://dev.ai.megacampus.ru"
        fi

        if [ "$DEPLOY_RESULT" == "success" ]; then
          MESSAGE="🚀 *MegaCampus $ENV_NAME*%0A%0A✅ SUCCESS%0A%0A📦 Commit: \`${COMMIT_SHA:0:7}\`%0A🌿 Branch: $BRANCH%0A👤 Author: $ACTOR%0A🔗 [View]($RUN_URL)%0A%0A🌐 $ENV_URL"
        else
          MESSAGE="🚀 *MegaCampus $ENV_NAME*%0A%0A❌ FAILED%0A%0A📦 Commit: \`${COMMIT_SHA:0:7}\`%0A🌿 Branch: $BRANCH%0A👤 Author: $ACTOR%0A🔗 [Logs]($RUN_URL)"
        fi

        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
          -d "chat_id=${TELEGRAM_CHAT_ID}" \
          -d "parse_mode=Markdown" \
          -d "disable_web_page_preview=true" \
          -d "text=${MESSAGE}"
```

**Пример уведомления**:
```
🚀 MegaCampus Staging

✅ SUCCESS

📦 Commit: a1b2c3d
🌿 Branch: master
👤 Author: maslennikovig
🔗 View

🌐 https://ai.megacampus.ru
```

---

## Docker Compose: Разделение ответственности

### Почему три файла?

**Проблема**: Если всё в одном docker-compose.yml, то при деплое **всё перезапускается** (включая Redis, Workers). Это приводит к:
- Потере данных в Redis (очереди, сессии)
- Остановке фоновых worker'ов (генерация курсов прерывается)
- Downtime для всех компонентов

**Решение**: Разделить на **Shared Infrastructure** (всегда работает) и **Application** (переключается через Blue/Green).

### docker-compose.infra.yml (Shared)

**Цель**: Компоненты, которые **никогда не останавливаются**.

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: megacampus-redis
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  docling-mcp:
    image: ghcr.io/maslennikov-ig/docling-mcp:latest
    container_name: megacampus-docling-mcp
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  worker:
    image: ghcr.io/maslennikov-ig/mc-2/api:latest
    container_name: megacampus-worker
    restart: unless-stopped
    command: node dist/workers/stages-worker.js
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    env_file: .env.production
    depends_on:
      - redis

  worker-stage7:
    image: ghcr.io/maslennikov-ig/mc-2/api:latest
    container_name: megacampus-worker-stage7
    restart: unless-stopped
    command: node dist/workers/stage7-worker.js
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    env_file: .env.production
    depends_on:
      - redis

volumes:
  redis-data:
```

**Запуск**:
```bash
docker compose -f docker-compose.infra.yml up -d
```

**Обновление**: Только при изменении инфраструктуры (добавление нового сервиса, изменение версии Redis).

### docker-compose.app.yml (Blue/Green)

**Цель**: Компоненты, которые **переключаются через Blue/Green**.

```yaml
services:
  web:
    image: ghcr.io/maslennikov-ig/mc-2/web:${TAG:-latest}
    container_name: ${COMPOSE_PROJECT_NAME}-web
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    ports:
      - "${WEB_PORT}:3000"
    env_file: .env.${COLOR}
    environment:
      - NODE_ENV=production
      - PORT=3000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    image: ghcr.io/maslennikov-ig/mc-2/api:${TAG:-latest}
    container_name: ${COMPOSE_PROJECT_NAME}-api
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
    ports:
      - "${API_PORT}:4000"
    env_file: .env.${COLOR}
    environment:
      - NODE_ENV=production
      - PORT=4000
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4000/health"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Переменные**:
- `TAG`: Docker image tag (latest, develop, master-a1b2c3d)
- `COLOR`: blue | green
- `WEB_PORT`: 3001 (blue) | 3002 (green)
- `API_PORT`: 4001 (blue) | 4002 (green)
- `COMPOSE_PROJECT_NAME`: megacampus-blue | megacampus-green

**Запуск (Blue)**:
```bash
docker compose -f docker-compose.app.yml --env-file .env.blue up -d
```

**Запуск (Green)**:
```bash
docker compose -f docker-compose.app.yml --env-file .env.green up -d
```

### docker-compose.dev.yml (Dev Environment)

**Цель**: Полностью изолированное окружение для разработки.

```yaml
services:
  web-dev:
    image: ghcr.io/maslennikov-ig/mc-2/web:develop
    container_name: megacampus-web-dev
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    ports:
      - "3010:3000"
    env_file: .env.dev
    environment:
      - NODE_ENV=production
      - PORT=3000
      - BULLMQ_QUEUE_NAME=course-generation-dev

  api-dev:
    image: ghcr.io/maslennikov-ig/mc-2/api:develop
    container_name: megacampus-api-dev
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    ports:
      - "4010:4000"
    env_file: .env.dev
    environment:
      - NODE_ENV=production
      - PORT=4000
      - BULLMQ_QUEUE_NAME=course-generation-dev
    volumes:
      - ./uploads-dev:/app/uploads

  worker-dev:
    image: ghcr.io/maslennikov-ig/mc-2/api:develop
    container_name: megacampus-worker-dev
    restart: unless-stopped
    command: node dist/workers/stages-worker.js
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    env_file: .env.dev
    environment:
      - BULLMQ_QUEUE_NAME=course-generation-dev
    depends_on:
      - megacampus-redis

  worker-stage7-dev:
    image: ghcr.io/maslennikov-ig/mc-2/api:develop
    container_name: megacampus-worker-stage7-dev
    restart: unless-stopped
    command: node dist/workers/stage7-worker.js
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    env_file: .env.dev
    environment:
      - BULLMQ_QUEUE_NAME=course-generation-dev
    depends_on:
      - megacampus-redis
```

**Отличия от Staging**:
- Другие порты (3010, 4010)
- Меньше ресурсов (1 CPU, 1GB)
- Другая очередь (`course-generation-dev`)
- Другая папка uploads (`./uploads-dev`)
- Использует образы с тегом `develop`

---

## Nginx: Template-Based Configuration

### Зачем template?

**Проблема**: Blue/Green переключает порты (3001 ↔ 3002, 4001 ↔ 4002). Nginx должен **динамически переключаться**.

**Решение**: Template файл с placeholder'ами, который заполняется через `sed` при деплое.

### nginx.conf.template

```nginx
upstream web_backend {
    server localhost:{{WEB_PORT}} max_fails=3 fail_timeout=30s;
}

upstream api_backend {
    server localhost:{{API_PORT}} max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name ai.megacampus.ru;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ai.megacampus.ru;

    # SSL Configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/ai.megacampus.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ai.megacampus.ru/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logging
    access_log /var/log/nginx/megacampus-access.log;
    error_log /var/log/nginx/megacampus-error.log;

    # Client settings
    client_max_body_size 100M;
    client_body_buffer_size 512k;
    large_client_header_buffers 4 512k;

    # Gzip
    gzip on;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Web (Next.js)
    location / {
        proxy_pass http://web_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # No caching for HTML to prevent stale deployments
        add_header Cache-Control "no-cache, no-store, must-revalidate" always;
        add_header Pragma "no-cache" always;
        add_header Expires "0" always;
    }

    # API (Express + tRPC)
    location /api {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Long timeouts for LLM operations
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        proxy_connect_timeout 60s;

        # Buffer settings for large responses
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
}
```

### Применение template при деплое

```bash
sed -e "s/{{WEB_PORT}}/3002/g" \
    -e "s/{{API_PORT}}/4002/g" \
    /opt/megacampus/nginx.conf.template | sudo tee /etc/nginx/sites-enabled/megacampus > /dev/null

sudo nginx -t  # Test config
sudo nginx -s reload  # Apply (no downtime)
```

**Результат**: Nginx переключается на новые порты **мгновенно** (reload ≈ 100ms).

### Особенности конфигурации

**No-cache для HTML**:
```nginx
add_header Cache-Control "no-cache, no-store, must-revalidate" always;
```
**Почему**: Если браузер закэширует HTML, пользователь может увидеть **старую версию** после деплоя. Мы принудительно отключаем кэширование для основных страниц.

**Long timeouts для API**:
```nginx
proxy_read_timeout 300s;
proxy_send_timeout 300s;
```
**Почему**: Генерация курсов через LLM может занимать **2-5 минут**. Стандартный timeout nginx (60s) оборвёт соединение.

**Large buffers**:
```nginx
proxy_buffer_size 128k;
proxy_buffers 4 256k;
```
**Почему**: tRPC может возвращать большие JSON response'ы (список курсов с метаданными). Стандартные буферы (4k) недостаточны.

---

## Реальные числа и опыт

### Timing

**CI/CD Pipeline** (от push до production):
- Stage 1 (Setup): ~1-2 минуты
- Stage 2 (Parallel Checks): ~8-10 минут (параллельно)
- Stage 3 (Build): ~2-3 минуты
- Stage 4 (CI Gate): ~10 секунд
- Stage 5 (Docker Builds): ~3-5 минут (с кэшем, параллельно)
- Stage 6 (Deploy): ~2-3 минуты
- **Total**: **~10-15 минут** от `git push` до production

**Деплой на сервере** (внутри deploy_blue_green.sh):
- Pull images: ~1-2 минуты (зависит от интернета)
- Start containers: ~20-30 секунд
- Health checks: ~30-60 секунд
- Nginx switch: ~100ms
- Stop old containers: ~10 секунд
- **Total**: **~2-3 минуты**

**Откат** (rollback_blue_green.sh):
- Если контейнеры ещё запущены: **~10 секунд**
- Если нужно поднять: **~30 секунд**

### Resource Usage

**Сервер**: 8 CPU, 11GB RAM

**Shared Infrastructure** (всегда работает):
- Redis: 1 CPU, 1GB RAM
- Docling MCP: 2 CPU, 4GB RAM
- Workers: 3 CPU, 3GB RAM
- **Total**: 6 CPU, 8GB RAM

**Application** (Blue/Green):
- Во время деплоя: 4 CPU, 4GB RAM (оба слота работают)
- После деплоя: 4 CPU, 4GB RAM (один слот работает, другой остановлен)
- **Peak**: ~10GB RAM (во время деплоя)
- **Normal**: ~8GB RAM (после деплоя)

**Dev** (отдельно):
- web-dev, api-dev, workers: 4 CPU, 4GB RAM
- **Total**: 4 CPU, 4GB RAM

**Итого**: Сервер работает на ~80% CPU, ~90% RAM в пике деплоя. Комфортно.

### Downtime

**Dev**:
- Простой деплой (restart): **~10-20 секунд**
- Приемлемо для dev окружения

**Staging (Blue/Green)**:
- Downtime: **0 секунд**
- Пользователи не замечают

**Откат**:
- С работающими контейнерами: **~10 секунд**
- С запуском контейнеров: **~30 секунд**

### Что я узнал

**1. Blue/Green на одном сервере — реально**

Не нужен Kubernetes. Не нужны облачные платформы. Достаточно:
- Docker Compose
- Nginx с template конфигурацией
- Bash скрипты для управления
- GitHub Actions для автоматизации

**2. Разделение docker-compose — критично**

Первая версия: всё в одном docker-compose.yml. Каждый деплой перезапускал Redis и Worker'ов. Потеря очередей, прерывание задач.

Решение: разделить на `.infra.yml` (shared) и `.app.yml` (Blue/Green). Инфраструктура работает 24/7, приложение переключается.

**3. Health checks — не формальность**

Были случаи, когда контейнер стартовал, но API не отвечал (проблемы с базой, миграциями). Health check ловил это и откатывался автоматически.

**Важно**: Проверять **реальную готовность**, не только `docker ps`.

**4. Параллельные проверки — ускорение на 70%**

До параллелизма: lint → type-check → security → tests → build ≈ **30 минут**.

После: lint, type-check, security, tests **параллельно** → build ≈ **10 минут**.

GitHub Actions matrix для Docker builds: **web + api параллельно** вместо последовательно. Ещё **-5 минут**.

**5. Кэширование Docker layers — must have**

Без кэша: Docker build ≈ **10 минут** (каждый раз с нуля).

С GitHub Actions cache (`type=gha`): **3-5 минут** (переиспользование слоёв).

**Speedup**: ~70%.

**6. Template nginx — проще чем кажется**

Первая мысль: "Нужен какой-то сложный конфиг-менеджер (Ansible, Terraform)".

Реальность: `sed` справляется за 1 строку. Проще, понятнее, надёжнее.

---

## Как внедрить у себя

### Минимальная версия (без CI/CD)

**Что нужно:**
1. Один сервер с Docker
2. Два docker-compose файла (infra + app)
3. Два скрипта (deploy_blue_green.sh + rollback_blue_green.sh)
4. Nginx с template конфигурацией

**Шаги:**

**1. Разделите docker-compose:**
```bash
# docker-compose.infra.yml
services:
  redis:
    image: redis:7-alpine
    # ... (shared services)

# docker-compose.app.yml
services:
  web:
    image: your-image:${TAG}
    container_name: ${COMPOSE_PROJECT_NAME}-web
    ports:
      - "${WEB_PORT}:3000"
    # ...
```

**2. Создайте env файлы:**
```bash
# .env.blue
COLOR=blue
WEB_PORT=3001
COMPOSE_PROJECT_NAME=app-blue

# .env.green
COLOR=green
WEB_PORT=3002
COMPOSE_PROJECT_NAME=app-green
```

**3. Скопируйте deploy_blue_green.sh:**
```bash
curl -O https://raw.githubusercontent.com/maslennikov-ig/mc-2/master/scripts/deploy_blue_green.sh
chmod +x deploy_blue_green.sh
```

**4. Настройте nginx template:**
```nginx
upstream web_backend {
    server localhost:{{WEB_PORT}};
}

server {
    listen 80;
    location / {
        proxy_pass http://web_backend;
    }
}
```

**5. Первый деплой:**
```bash
./deploy_blue_green.sh production latest
```

**6. Откат (если нужно):**
```bash
./rollback_blue_green.sh
```

**Время на настройку**: 1-2 часа.

### Полная версия (с CI/CD)

**Что нужно:**
1. Всё из минимальной версии
2. GitHub Actions
3. GitHub Container Registry
4. SSH доступ к серверу

**Шаги:**

**1. Создайте GitHub Secrets:**
- `DEPLOY_SSH_KEY` - приватный SSH ключ
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, etc. - секреты приложения
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` - для уведомлений

**2. Скопируйте CI/CD workflow:**
```bash
mkdir -p .github/workflows
curl -o .github/workflows/ci-cd.yml \
  https://raw.githubusercontent.com/maslennikov-ig/mc-2/master/.github/workflows/ci-cd.yml
```

**3. Адаптируйте под свой проект:**
- Замените `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`
- Замените `ghcr.io/${{ github.repository }}/web` на ваш registry
- Адаптируйте build команды (`pnpm build` → `npm run build`)

**4. Push в master:**
```bash
git add .github/workflows/ci-cd.yml
git commit -m "Add CI/CD with Blue/Green"
git push origin master
```

**5. Проверьте Actions:**
```
https://github.com/your-repo/actions
```

**Время на настройку**: 2-4 часа (включая отладку).

---

## Checklist для настройки

**Подготовка сервера:**
- [ ] Docker установлен
- [ ] Docker Compose установлен
- [ ] Nginx установлен
- [ ] SSL сертификат настроен (Let's Encrypt)
- [ ] SSH доступ настроен (ключи, без пароля)

**Конфигурация:**
- [ ] `docker-compose.infra.yml` создан (shared services)
- [ ] `docker-compose.app.yml` создан (Blue/Green app)
- [ ] `.env.production` создан (секреты)
- [ ] `.env.blue` создан (Blue config)
- [ ] `.env.green` создан (Green config)
- [ ] `nginx.conf.template` создан (template с placeholders)
- [ ] `scripts/deploy_blue_green.sh` создан
- [ ] `scripts/rollback_blue_green.sh` создан

**Тестирование:**
- [ ] Запустить infra: `docker compose -f docker-compose.infra.yml up -d`
- [ ] Первый деплой: `./deploy_blue_green.sh production latest`
- [ ] Проверить health: `curl http://localhost:3001/health`
- [ ] Проверить nginx: `curl https://your-domain.com`
- [ ] Второй деплой (переключение Blue → Green)
- [ ] Откат: `./rollback_blue_green.sh`

**CI/CD:**
- [ ] GitHub Secrets добавлены
- [ ] `.github/workflows/ci-cd.yml` создан
- [ ] Dockerfile оптимизирован (multi-stage build)
- [ ] Health endpoints реализованы (`/health`, `/api/health`)
- [ ] Push в master → проверить автоматический деплой

**Мониторинг:**
- [ ] Telegram уведомления настроены
- [ ] Логи nginx настроены (`/var/log/nginx/`)
- [ ] Docker logs доступны (`docker compose logs -f`)

---

## Ограничения и когда НЕ использовать

**Когда Blue/Green не подходит:**

**1. Stateful приложения с долгими соединениями**

Пример: WebSocket сервер с долгими соединениями (чат, игровой сервер).

Проблема: При переключении nginx активные WebSocket соединения **оборвутся**.

Решение: Нужен graceful shutdown (drain connections) или sticky sessions. Blue/Green в чистом виде не подходит.

**2. Shared state между версиями**

Пример: Приложение использует файловую систему для shared state (locks, temp files).

Проблема: Blue и Green видят **разные файлы** (разные volumes).

Решение: Вынести state в Redis/БД или использовать shared volume (но тогда нужны миграции).

**3. Database migrations breaking backward compatibility**

Пример: Новая версия меняет схему БД (удаляет поле, меняет тип).

Проблема: Старая версия (Blue) не совместима с новой схемой.

Решение: Миграции должны быть **backward compatible** или использовать expand-contract pattern.

**4. Очень ограниченные ресурсы**

Пример: Сервер с 2GB RAM, приложение использует 1.5GB.

Проблема: Во время деплоя **два слота** = 3GB RAM → сервер умрёт.

Решение: Blue/Green требует 2x ресурсов во время деплоя. Если нет запаса — используйте rolling deploy.

**Когда Blue/Green ИДЕАЛЕН:**

- ✅ Stateless приложения (web, api)
- ✅ Backward compatible migrations
- ✅ Есть запас ресурсов (2x RAM/CPU во время деплоя)
- ✅ Критично избежать downtime
- ✅ Важен быстрый откат

---

## Что дальше

**У меня в планах:**

**1. Production окружение**

Сейчас Staging использует Blue/Green. Когда появится Production, просто скопирую ту же стратегию.

**2. Канареечный деплой (Canary)**

Blue/Green переключает **100% трафика** сразу. Canary переключает **10% → 50% → 100%** постепенно.

Реализация: nginx upstream с `weight`:
```nginx
upstream web_backend {
    server localhost:3001 weight=9;  # Blue (90%)
    server localhost:3002 weight=1;  # Green (10%)
}
```

**3. Автоматические smoke tests после деплоя**

Сейчас проверяем `/health`. Хочу добавить реальные E2E тесты (создать курс, загрузить файл, проверить результат).

**4. Мониторинг метрик до/после деплоя**

Сравнивать latency, error rate, throughput до и после переключения. Автоматический откат если метрики деградировали.

---

## Заключение

**Что я сделал:**
- Настроил **Dev и Staging окружения** с полной изоляцией
- Добавил **Blue/Green деплой** для zero-downtime
- Автоматизировал через **CI/CD** (8 стадий, параллельные проверки)
- Деплою **в любое время дня**, без страха

**Результаты:**
- Деплой: **10-15 минут** от push до production
- Downtime: **0 секунд**
- Откат: **30 секунд**
- Спокойствие: **бесценно**

**Кому подходит:**
- У вас один сервер с Docker
- Вы используете docker-compose
- Вам нужен zero-downtime
- Вам важен быстрый откат

**Кому НЕ подходит:**
- Stateful приложения с долгими соединениями
- Очень ограниченные ресурсы (нет запаса для 2x во время деплоя)
- Breaking database migrations

**Репозиторий**: https://github.com/maslennikov-ig/mc-2
**Скрипты**: `scripts/deploy_blue_green.sh`, `scripts/rollback_blue_green.sh`
**CI/CD**: `.github/workflows/ci-cd.yml`

Если вы знаете как сделать лучше — напишите в комментариях. Я всегда открыт к улучшениям.

---

## Contact & Feedback

### 📱 Telegram

**Channel** (редкие, но интересные посты): https://t.me/maslennikovigor
Заходите, читайте мои мысли и статьи. Пишу редко, но метко.

**Direct Contact**: https://t.me/maslennikovig
Нужно поговорить? Пишите напрямую. Всегда рад общению.

### 💬 Feedback: I'm Wide Open

**Мне интересно услышать:**
- **Критику** — Что не так с этим подходом? Где слабые места?
- **Идеи** — Какие фичи добавить? Чего не хватает?
- **Предложения** — Как улучшить, оптимизировать, рефакторить?
- **Вопросы** — Что-то непонятно? Спрашивайте.

**Каналы для обратной связи:**
- **GitHub Issues**: https://github.com/maslennikov-ig/mc-2/issues (баги, фичи)
- **GitHub Discussions**: https://github.com/maslennikov-ig/mc-2/discussions (идеи, вопросы)
- **Telegram**: https://t.me/maslennikovig (личный диалог)

**Tone**: Максимально открыт к конструктивному диалогу. Без эго, просто хочу сделать лучше.
