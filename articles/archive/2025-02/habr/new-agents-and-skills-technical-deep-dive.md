# Claude Code Orchestrator Kit: 44 новых агента и как я автоматизировал DevSecOps, систематическую отладку и развёртывание через GitOps

За последние два месяца я добавил в [Claude Code Orchestrator Kit](https://github.com/maslennikov-ig/claude-code-orchestrator-kit) 44 новых специализированных агента и около 30 скиллов. Это не просто "ещё агенты" — это готовые инженерные паттерны для реальных production-задач.

В этой статье я покажу технические детали трёх ключевых инноваций:
1. **deployment-engineer** — DevSecOps, GitOps, Blue-Green развёртывания
2. **systematic-debugging skill** — методология отладки с Iron Law: "NO FIXES WITHOUT ROOT CAUSE"
3. **Health workflows** — автоматическое обнаружение и исправление багов, уязвимостей, мёртвого кода

Будет код, архитектурные решения, граблимые моменты.

<cut />

## Оглавление

1. [Контекст: что такое orchestrator kit](#context)
2. [deployment-engineer: DevSecOps как агент](#devops)
3. [systematic-debugging: Iron Law отладки](#debugging)
4. [Health workflows: Return Control pattern](#health)
5. [Полный список новых агентов](#agents-list)
6. [Disclaimer: ожидаемый pushback](#disclaimer)
7. [Как попробовать](#try)
8. [Контакты и обратная связь](#contacts)

---

<a name="context"></a>
## 1. Контекст: что такое orchestrator kit

**Claude Code Orchestrator Kit** — это open-source система (MIT license), которая превращает Claude Code из мощного ассистента в профессиональную платформу оркестрации с 33+ специализированными агентами.

**Репозиторий**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit
**NPM**: `npm install -g claude-code-orchestrator-kit`

### Ключевая идея

**Проблема стандартного Claude Code**:
- Быстро сжигает контекстное окно
- Нет систематических воркфлоу
- Нет автоматических проверок качества
- Нет специализации под задачи

**Наше решение**:
- **Main Claude Code = orchestrator ONLY**
- Все сложные задачи → делегируем специализированным агентам
- Каждый агент = изолированный контекст
- Обязательная верификация после делегирования
- Автоматические quality gates (type-check, build, tests)

### Return Control Pattern

Это фундаментальный паттерн оркестрации, на котором построены все воркфлоу:

```
User Request
  ↓
Main Claude Code (Orchestrator)
  ├→ Собирает контекст (код, паттерны, коммиты)
  ├→ Создаёт plan file (.{workflow}-plan.json)
  ├→ Валидирует план
  ├→ Сигнализирует готовность, EXIT
  ↓
Main Session (User Context)
  ├→ Вызывает Sub-Agent через Task tool
  ↓
Sub-Agent (Isolated Context)
  ├→ Читает план
  ├→ Выполняет работу
  ├→ Валидирует (type-check, build, tests)
  ├→ Генерирует отчёт
  ├→ Возвращает контроль, EXIT
  ↓
Main Claude Code (Resumes)
  ├→ Читает отчёт
  ├→ Верифицирует результат (read files, run type-check)
  ├→ Accept ИЛИ Re-delegate с исправлениями
  ├→ Отмечает задачу completed
  ├→ Переходит к следующей
```

**Почему именно так?**
- **Изоляция контекста**: main session остаётся на ~10-15K токенов вместо ~50K
- **Специализация**: каждый агент — эксперт в домене (security, bugs, infrastructure)
- **Верификация**: обязательная проверка после каждого шага
- **Масштабируемость**: можно работать над проектом бесконечно долго

Теперь перейдём к конкретным реализациям.

---

<a name="devops"></a>
## 2. deployment-engineer: DevSecOps как агент

Это один из самых мощных новых агентов. Он реализует три ключевых практики современного DevOps:

1. **DevSecOps** — безопасность на каждом этапе CI/CD
2. **GitOps** — Git как единственный источник правды
3. **Blue-Green Deployment** — развёртывание без даунтайма

Агент находится в `.claude/agents/infrastructure/workers/deployment-engineer.md` (447 строк).

### 2.1. DevSecOps: Security Gates

Традиционный подход: "сначала сделали, потом проверили безопасность".
Наш подход: **безопасность на каждом этапе как блокирующее требование**.

#### Security Gate 1: Pre-Commit (Gitleaks)

**Задача**: Не допустить коммит секретов в репозиторий.

Конфиг `.gitleaks.toml`:
```toml
title = "Security Configuration"
[allowlist]
paths = ['''\.env\.example$''', '''README\.md$''']

[[rules]]
id = "generic-api-key"
regex = '''(?i)(api[_-]?key)['":\s]*=?\s*['"][a-zA-Z0-9]{20,}['"]'''

[[rules]]
id = "private-key"
regex = '''-----BEGIN (RSA |EC )?PRIVATE KEY-----'''
```

Pre-commit hook `.husky/pre-commit`:
```bash
#!/bin/sh
gitleaks protect --staged --verbose || exit 1
pnpm type-check || exit 1
pnpm lint || exit 1
```

**Результат**: Попытка закоммитить API ключ → **блокируется на локальной машине**.

#### Security Gate 2: SAST (Semgrep)

**Задача**: Статический анализ кода на паттерны уязвимостей.

Конфиг `.semgrep.yml`:
```yaml
rules:
  - id: hardcoded-secrets
    pattern: const $VAR = "$SECRET"
    severity: ERROR
    languages: [typescript, javascript]

  - id: sql-injection
    pattern: db.query("... " + $VAR + " ...")
    severity: ERROR
    languages: [typescript, javascript]
```

В CI/CD:
```yaml
sast-scan:
  needs: secret-scan
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: returntocorp/semgrep-action@v1
      with: { config: .semgrep.yml }
```

**Результат**: SQL injection паттерн в PR → **build fails**.

#### Security Gate 3: Container Security (Trivy + OPA)

**Задача**: Проверить Dockerfile на best practices и просканировать образ.

Policy as Code (`.conftest/policy/dockerfile.rego`):
```rego
package main

deny[msg] {
  input[i].Cmd == "from"
  contains(input[i].Value[_], "latest")
  msg = "Don't use latest tag"
}

deny[msg] {
  not user_defined
  msg = "Must specify USER directive"
}
user_defined { input[_].Cmd == "user" }

deny[msg] {
  not healthcheck_defined
  msg = "Must include HEALTHCHECK"
}
healthcheck_defined { input[_].Cmd == "healthcheck" }
```

В CI/CD:
```yaml
filesystem-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/trivy-action@master
      with:
        scan-type: fs
        severity: 'CRITICAL,HIGH'
```

**Результат**: `FROM node:latest` в Dockerfile → **policy violation**.

### 2.2. GitOps: Declarative Infrastructure

**Идея GitOps**:
- Git = single source of truth
- Сервер **сам** тянет изменения из Git (pull-based)
- Не push в production, а production читает Git
- Автоматическое обнаружение drift (ручные изменения на сервере)

#### Структура проекта

```
infrastructure/
├── base/                    # Общие конфиги
│   ├── docker-compose.base.yml
│   └── Dockerfile
├── environments/            # Оверлеи под окружения
│   ├── development/
│   ├── staging/
│   └── production/
└── scripts/
    ├── deploy.sh           # GitOps deployment
    └── detect-drift.sh     # Drift detection
```

#### GitOps Deploy Script

`scripts/deploy.sh` (упрощённая версия):
```bash
#!/bin/bash
set -euo pipefail

ENVIRONMENT="${1:-staging}"
DEPLOY_ROOT="/opt/megacampus"
STATE_FILE="${DEPLOY_ROOT}/.gitops-state.json"

# Тянем из Git (single source of truth)
pull_from_git() {
    cd "${DEPLOY_ROOT}"
    PREV=$(git rev-parse HEAD)
    git fetch origin && git reset --hard origin/main
    CURR=$(git rev-parse HEAD)
    [ "$PREV" != "$CURR" ] && return 0 || return 1
}

# Записываем состояние деплоя
record_state() {
    cat > "${STATE_FILE}" <<EOF
{"commit": "$(git rev-parse HEAD)", "env": "${ENVIRONMENT}", "time": "$(date -u +%FT%TZ)"}
EOF
}

# Детектим drift (ручные изменения на сервере)
detect_drift() {
    cd "${DEPLOY_ROOT}"
    git diff --quiet || {
        echo "⚠️  DRIFT DETECTED! Manual changes on server."
        return 1
    }
}

# Синхронизируем с production
sync_to_production() {
    local compose="infrastructure/environments/${ENVIRONMENT}/docker-compose.yml"
    docker compose -f "$compose" config -q || exit 1
    docker compose -f "$compose" up -d --remove-orphans
    record_state
}

# Main flow
pull_from_git && sync_to_production
detect_drift
```

#### Как это работает

**Обычный deploy** (push-based):
```bash
# Локально
git push origin main

# Потом вручную на сервере
ssh production "cd /app && git pull && docker compose up -d"
```

**GitOps deploy** (pull-based):
```bash
# Локально
git push origin main

# На сервере — автоматический cron job каждые 5 минут
*/5 * * * * /opt/megacampus/scripts/deploy.sh production
```

**Преимущества**:
- Сервер не имеет SSH доступа к Git (pull-only)
- Все деплои зафиксированы в Git истории
- Drift detection показывает ручные изменения
- Rollback = просто откат коммита в Git

### 2.3. Blue-Green Deployment: Zero-Downtime

**Идея**:
- Два идентичных production окружения: **blue** и **green**
- Только одно обслуживает трафик
- Новая версия → деплоим в неактивное окружение
- Smoke tests → переключаем трафик
- Rollback = просто переключаем обратно

#### Docker Compose для Blue-Green

`docker-compose.blue-green.yml`:
```yaml
version: '3.9'
services:
  traefik:
    image: traefik:v2.10
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports: ["80:80", "443:443", "8080:8080"]
    volumes: ["/var/run/docker.sock:/var/run/docker.sock:ro"]

  app-blue:
    image: ghcr.io/megacampus/mc2:${BLUE_VERSION:-latest}
    environment:
      - NODE_ENV=production
      - DEPLOYMENT_SLOT=blue
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app-blue.rule=Host(`example.com`)"
      - "traefik.http.routers.app-blue.entrypoints=websecure"
      - "traefik.http.services.app-blue.loadbalancer.healthcheck.path=/health"
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
      interval: 10s
      retries: 3

  app-green:
    image: ghcr.io/megacampus/mc2:${GREEN_VERSION:-latest}
    environment:
      - NODE_ENV=production
      - DEPLOYMENT_SLOT=green
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app-green.rule=Host(`green.internal`)"
      - "traefik.http.services.app-green.loadbalancer.healthcheck.path=/health"

  db:
    image: postgres:16-alpine
    volumes: [postgres-data:/var/lib/postgresql/data]
    healthcheck: { test: ["CMD", "pg_isready"], interval: 10s }

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes: [redis-data:/data]

volumes:
  postgres-data:
  redis-data:
```

#### Blue-Green Deploy Script

`scripts/blue-green-deploy.sh`:
```bash
#!/bin/bash
set -euo pipefail

NEW_VERSION="${1:-latest}"
STATE_FILE=".deployment-state.json"
COMPOSE="docker-compose.blue-green.yml"

get_active() { jq -r '.activeSlot // "blue"' "$STATE_FILE" 2>/dev/null || echo "blue"; }
get_inactive() { [ "$(get_active)" = "blue" ] && echo "green" || echo "blue"; }

# Деплоим в неактивный слот
deploy_inactive() {
    local slot=$(get_inactive)
    export ${slot^^}_VERSION="$NEW_VERSION"

    echo "→ Deploying $NEW_VERSION to $slot slot..."
    docker pull "ghcr.io/megacampus/mc2:$NEW_VERSION"
    docker compose -f "$COMPOSE" up -d "app-$slot"

    # Ждём healthy status
    for i in {1..30}; do
        STATUS=$(docker inspect --format='{{.State.Health.Status}}' "megacampus-app-$slot" 2>/dev/null || echo "starting")
        [ "$STATUS" = "healthy" ] && { echo "✓ $slot is healthy"; return 0; }
        echo "  Waiting for $slot to be healthy... ($i/30)"
        sleep 2
    done

    echo "✗ $slot failed to become healthy"
    return 1
}

# Smoke tests
smoke_test() {
    local slot=$(get_inactive)
    echo "→ Running smoke tests on $slot..."

    curl -sf "http://localhost:3000/health" | jq -e '.status == "ok"' > /dev/null || {
        echo "✗ Health check failed"
        return 1
    }

    echo "✓ Smoke tests passed"
}

# Переключаем трафик (меняем Traefik labels)
switch_traffic() {
    local new_active=$(get_inactive)
    echo "→ Switching traffic to $new_active..."

    # Обновляем Traefik конфигурацию
    docker compose -f "$COMPOSE" up -d traefik

    # Записываем новое состояние
    echo "{\"activeSlot\": \"$new_active\", \"version\": \"$NEW_VERSION\", \"time\": \"$(date -u +%FT%TZ)\"}" > "$STATE_FILE"

    echo "✓ Traffic switched to $new_active (version $NEW_VERSION)"
}

# Rollback
rollback() {
    local prev=$([ "$(get_active)" = "blue" ] && echo "green" || echo "blue")
    echo "→ Rolling back to $prev..."
    switch_traffic
}

# Main deployment flow
echo "=== Blue-Green Deployment ==="
echo "Active slot: $(get_active)"
echo "Deploying to: $(get_inactive)"

deploy_inactive || { echo "✗ Deployment failed"; exit 1; }
smoke_test || {
    echo "✗ Smoke tests failed, stopping inactive slot"
    docker compose -f "$COMPOSE" stop "app-$(get_inactive)"
    exit 1
}
switch_traffic

echo "=== Deployment successful ==="
echo "Active slot: $(get_active)"
echo "Version: $NEW_VERSION"
```

#### Использование

```bash
# Деплой новой версии
./scripts/blue-green-deploy.sh v1.2.3

# Вывод:
# === Blue-Green Deployment ===
# Active slot: blue
# Deploying to: green
# → Deploying v1.2.3 to green slot...
# ✓ green is healthy
# → Running smoke tests on green...
# ✓ Smoke tests passed
# → Switching traffic to green...
# ✓ Traffic switched to green (version v1.2.3)
# === Deployment successful ===

# Rollback (если что-то пошло не так)
./scripts/blue-green-deploy.sh rollback
```

#### Database Migration Strategy (Expand-Contract)

**Проблема**: Blue-Green требует, чтобы два слота работали одновременно. Но база данных одна.

**Решение**: Backwards-compatible миграции (Expand-Contract pattern).

**Пример**: Переименовываем колонку `name` → `full_name`.

**Неправильно** (ломает blue slot):
```sql
ALTER TABLE users RENAME COLUMN name TO full_name;
```

**Правильно** (Expand-Contract):

**Шаг 1: Expand** (добавляем новую колонку, старый код игнорирует):
```sql
ALTER TABLE users ADD COLUMN full_name TEXT;
UPDATE users SET full_name = name WHERE full_name IS NULL;
```

**Шаг 2: Deploy green** (код пишет в обе колонки):
```typescript
// Green slot code
await db.query(
  'UPDATE users SET name = $1, full_name = $1 WHERE id = $2',
  [fullName, userId]
);
```

**Шаг 3: Switch traffic** (green активен, blue ещё работает):
```bash
./scripts/blue-green-deploy.sh v1.2.3
```

**Шаг 4: Contract** (удаляем старую колонку ТОЛЬКО после полного переключения):
```sql
-- Через несколько часов, когда убедились что всё работает
ALTER TABLE users DROP COLUMN name;
```

**Результат**: Zero-downtime миграция.

### 2.4. CI/CD Pipeline (Полный пример)

`.github/workflows/ci-cd.yml`:
```yaml
name: CI/CD Pipeline with DevSecOps Gates
on:
  push: { branches: [main, develop] }
  pull_request: { branches: [main, develop] }

env:
  NODE_VERSION: '20.x'
  REGISTRY: ghcr.io

jobs:
  # Gate 1: Secret Scanning
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # Gate 2: SAST
  sast-scan:
    needs: secret-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with: { config: .semgrep.yml }

  # Build & Test
  build-test:
    needs: [secret-scan, sast-scan]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm type-check
      - run: pnpm lint
      - run: pnpm build
      - run: pnpm test:ci
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  # Gate 3: Dependency Audit
  dependency-audit:
    needs: build-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm audit --audit-level=high
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

  # Gate 4: Filesystem Scan
  filesystem-scan:
    needs: build-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          severity: 'CRITICAL,HIGH'

  # Build Docker Image
  build-docker:
    needs: [build-test, dependency-audit, filesystem-scan]
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      # Gate 5: Dockerfile Linting
      - uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ github.repository }}:${{ github.sha }}
            ${{ env.REGISTRY }}/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      # Gate 6: Container Image Scan
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ github.repository }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

  # Deploy to Staging
  deploy-staging:
    needs: build-docker
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.megacampus.ai
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy via GitOps
        run: |
          echo "Triggering GitOps pull on staging server..."
          # В реальности: webhook trigger или ArgoCD sync

  # Deploy to Production (Blue-Green)
  deploy-production:
    needs: build-docker
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://megacampus.ai
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy via Blue-Green
        run: |
          echo "Deploying ${{ github.sha }} to production via blue-green..."
          # В реальности: SSH в production + ./scripts/blue-green-deploy.sh
```

### 2.5. Dockerfile (Security Best Practices)

Multi-stage build с security best practices:

```dockerfile
# syntax=docker/dockerfile:1.4
ARG NODE_VERSION=20

# Stage 1: Base (общие зависимости)
FROM node:${NODE_VERSION}-alpine AS base
RUN npm install -g pnpm@9 && \
    apk add --no-cache dumb-init
WORKDIR /app

# Stage 2: Dependencies (кэширование)
FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Stage 3: Builder (сборка)
FROM deps AS builder
COPY . .
RUN pnpm build && \
    pnpm prune --prod

# Stage 4: Runner (production)
FROM node:${NODE_VERSION}-alpine AS runner

# Security: dumb-init для корректной обработки сигналов
RUN apk add --no-cache dumb-init

# Security: non-root user
RUN adduser -S -u 1001 nodejs

WORKDIR /app

# Копируем ТОЛЬКО production файлы
COPY --from=builder --chown=nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs /app/package.json ./

# Security: запуск от non-root
USER nodejs

EXPOSE 3000

ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q --spider http://localhost:3000/health || exit 1

# dumb-init для корректной обработки SIGTERM
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

**Почему multi-stage?**
- Финальный образ: ~50MB (vs ~500MB с dev dependencies)
- Кэширование слоёв: изменение кода → только пересборка builder stage
- Security: только production код в финальном образе

**Security детали**:
- ✅ Non-root user (nodejs, uid 1001)
- ✅ dumb-init (корректная обработка сигналов)
- ✅ Health check (для orchestrators)
- ✅ Specific Node version (не `latest`)
- ✅ Alpine Linux (минимальная attack surface)

### 2.6. Что deployment-engineer делает автоматически

Когда я запускаю агента:
```bash
# В Claude Code
Invoke deployment-engineer agent with task: "Setup CI/CD for our Next.js app with DevSecOps gates"
```

Агент:
1. Анализирует архитектуру проекта (monorepo/microservices, Next.js/Node)
2. Генерирует `.gitleaks.toml`, `.semgrep.yml`, `.conftest/policy/`
3. Создаёт `.github/workflows/ci-cd.yml` с security gates
4. Настраивает `docker-compose.blue-green.yml` с Traefik
5. Пишет `scripts/deploy.sh` (GitOps), `scripts/blue-green-deploy.sh`
6. Создаёт multi-stage `Dockerfile` с security best practices
7. Добавляет `.dockerignore`, `.husky/pre-commit`
8. Валидирует всё через `hadolint`, `yamllint`, `docker compose config`
9. Генерирует отчёт с инструкциями по настройке secrets

**Время**: 3-5 минут.
**Результат**: Production-ready CI/CD pipeline с DevSecOps gates.

---

<a name="debugging"></a>
## 3. systematic-debugging: Iron Law отладки

Это один из самых важных скиллов. Он решает проблему, с которой я сталкивался постоянно: **random fixes тратят время и создают новые баги**.

Скилл находится в `.claude/skills/systematic-debugging/SKILL.md` (297 строк).

### 3.1. The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

**Если вы не завершили Phase 1, вы не можете предлагать фиксы.**

Это не рекомендация. Это **требование**.

### 3.2. The Four Phases

#### Phase 1: Root Cause Investigation

**ПЕРЕД любым фиксом**:

1. **Внимательно читайте ошибки**
   - Не пропускайте ошибки и warnings
   - Они часто содержат точное решение
   - Читайте stack traces полностью
   - Отмечайте номера строк, пути файлов, error codes

2. **Воспроизводите консистентно**
   - Можете вызвать это надёжно?
   - Каковы точные шаги?
   - Это происходит каждый раз?
   - Если не воспроизводимо → собирайте больше данных, не гадайте

3. **Проверяйте недавние изменения**
   - Что изменилось, что могло это вызвать?
   - Git diff, recent commits
   - Новые dependencies, config changes
   - Различия в окружении

4. **Собирайте evidence в multi-component системах**

**КОГДА система имеет несколько компонентов** (CI → build → signing, API → service → database):

**ПЕРЕД предложением фиксов, добавьте диагностическую инструментацию**:
```
Для КАЖДОЙ границы компонента:
  - Логируйте какие данные входят в компонент
  - Логируйте какие данные выходят из компонента
  - Проверяйте распространение environment/config
  - Проверяйте состояние на каждом слое

Запустите один раз, чтобы собрать evidence, показывающую ГДЕ ломается
ПОТОМ анализируйте evidence, чтобы идентифицировать failing component
ПОТОМ исследуйте этот конкретный компонент
```

**Пример** (multi-layer система):
```bash
# Layer 1: Workflow
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"

# Layer 3: Signing script
echo "=== Keychain state: ==="
security list-keychains
security find-identity -v

# Layer 4: Actual signing
codesign --sign "$IDENTITY" --verbose=4 "$APP"
```

**Это показывает**: Какой layer fails (secrets → workflow ✓, workflow → build ✗)

5. **Трассируйте data flow**

**КОГДА ошибка глубоко в call stack**:

См. `root-cause-tracing.md` в директории скилла для полной техники backward tracing.

**Краткая версия**:
- Откуда берётся плохое значение?
- Что вызвало это с плохим значением?
- Продолжайте трассировку вверх, пока не найдёте источник
- Фиксите в источнике, не в симптоме

#### Phase 2: Pattern Analysis

**Найдите паттерн перед фиксом**:

1. **Найдите работающие примеры**
   - Найдите похожий рабочий код в том же codebase
   - Что работает, что похоже на сломанное?

2. **Сравните с референсами**
   - Если реализуете паттерн, прочитайте референс ПОЛНОСТЬЮ
   - Не бегло просматривайте — читайте каждую строку
   - Понимайте паттерн полностью перед применением

3. **Идентифицируйте различия**
   - Что отличается между рабочим и сломанным?
   - Перечислите каждое различие, как бы мало оно ни было
   - Не предполагайте "это не может иметь значения"

4. **Понимайте зависимости**
   - Какие другие компоненты это требует?
   - Какие настройки, конфиг, environment?
   - Какие предположения это делает?

#### Phase 3: Hypothesis and Testing

**Научный метод**:

1. **Сформируйте одну гипотезу**
   - Сформулируйте чётко: "Я думаю X — root cause, потому что Y"
   - Запишите это
   - Будьте конкретны, не расплывчаты

2. **Тестируйте минимально**
   - Сделайте МИНИМАЛЬНОЕ возможное изменение для проверки гипотезы
   - Одна переменная за раз
   - Не фиксите несколько вещей сразу

3. **Верифицируйте перед продолжением**
   - Сработало? Да → Phase 4
   - Не сработало? Сформируйте НОВУЮ гипотезу
   - НЕ добавляйте больше фиксов поверх

4. **Когда вы не знаете**
   - Скажите "Я не понимаю X"
   - Не притворяйтесь, что знаете
   - Попросите помощи
   - Изучите больше

#### Phase 4: Implementation

**Фиксите root cause, не симптом**:

1. **Создайте failing test case**
   - Простейшее возможное воспроизведение
   - Автоматизированный тест, если возможно
   - Одноразовый test script, если нет фреймворка
   - ДОЛЖЕН быть перед фиксом

2. **Реализуйте один фикс**
   - Адресуйте идентифицированный root cause
   - ОДНО изменение за раз
   - Никаких "пока я здесь" улучшений
   - Никакого bundled рефакторинга

3. **Верифицируйте фикс**
   - Тест проходит теперь?
   - Другие тесты не сломаны?
   - Проблема действительно решена?

4. **Если фикс не работает**
   - STOP
   - Посчитайте: Сколько фиксов вы попробовали?
   - Если < 3: Вернитесь к Phase 1, проанализируйте заново с новой информацией
   - **Если ≥ 3: STOP и поставьте под вопрос архитектуру (шаг 5 ниже)**
   - НЕ пытайтесь Fix #4 без архитектурного обсуждения

5. **Если 3+ фикса провалились: Поставьте под вопрос архитектуру**

**Паттерн, указывающий на архитектурную проблему**:
- Каждый фикс открывает новый shared state/coupling/проблему в другом месте
- Фиксы требуют "massive refactoring" для реализации
- Каждый фикс создаёт новые симптомы в другом месте

**STOP и поставьте под вопрос фундаменталы**:
- Этот паттерн фундаментально корректен?
- Мы "придерживаемся его через чистую инерцию"?
- Должны ли мы рефакторить архитектуру vs. продолжать фиксить симптомы?

**Обсудите с human partner перед попытками больше фиксов**

Это НЕ провалившаяся гипотеза — это **неправильная архитектура**.

### 3.3. Red Flags — STOP and Follow Process

Если вы поймали себя на мысли:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (когда уже попробовали 2+)**
- **Каждый фикс открывает новую проблему в другом месте**

**ВСЕ это означает: STOP. Вернитесь к Phase 1.**

**Если 3+ фикса провалились**: Поставьте под вопрос архитектуру (см. Phase 4.5)

### 3.4. Real-World Impact

Из наших debugging сессий:
- Systematic approach: **15-30 минут** до фикса
- Random fixes approach: **2-3 часа** thrashing
- First-time fix rate: **95% vs 40%**
- New bugs introduced: **Near zero vs common**

### 3.5. Пример использования скилла

**Проблема**: Tests failing с ошибкой `Cannot read property 'id' of undefined`.

**Неправильный подход** (random fixes):
```typescript
// Fix #1: Попробуем добавить optional chaining
const userId = user?.id;  // Не помогло

// Fix #2: Попробуем default value
const userId = user?.id || 'default';  // Тоже не помогло

// Fix #3: Попробуем проверку
if (user && user.id) { ... }  // Всё ещё ломается
```

**Правильный подход** (systematic-debugging):

**Phase 1: Root Cause Investigation**
```typescript
// Добавляем диагностику
console.log('User object:', user);
console.log('User type:', typeof user);
console.log('User is null?', user === null);
console.log('User is undefined?', user === undefined);

// Запускаем
// Output: User object: null
// Output: User type: object
// Output: User is null? true

// Root cause: user = null, not undefined
```

**Phase 2: Pattern Analysis**
```typescript
// Ищем откуда user берётся
const user = await getUserById(userId);
// ↑ Если пользователь не найден, возвращает null

// Проверяем референсную реализацию
// В документации: "Returns null if user not found"
```

**Phase 3: Hypothesis**
```
Гипотеза: getUserById возвращает null для несуществующего userId,
но код не проверяет null перед доступом к .id
```

**Phase 4: Implementation**
```typescript
// 1. Создаём failing test
test('handles non-existent user', async () => {
  const result = await processUser('non-existent-id');
  expect(result).toBeNull();
});

// 2. Фиксим root cause
const user = await getUserById(userId);
if (user === null) {
  return null;  // Handle gracefully
}
const processedId = user.id;

// 3. Верифицируем
// ✓ Test passes
// ✓ No other tests broken
```

**Результат**: Один фикс, 15 минут, проблема решена.

---

<a name="health"></a>
## 4. Health workflows: Return Control pattern в действии

Health workflows — это автоматические воркфлоу для обслуживания кодовой базы:
- `/health-bugs` — Bug detection and fixing
- `/health-security` — Security vulnerability scanning and remediation
- `/health-deps` — Dependency audit and safe updates
- `/health-cleanup` — Dead code detection and removal

Все используют **Return Control pattern** для изоляции контекста.

### 4.1. Архитектура Health Workflow

Каждый health workflow состоит из:
- **Orchestrator** (координирует фазы)
- **Hunter/Scanner/Auditor worker** (обнаруживает проблемы)
- **Fixer/Updater/Remover worker** (исправляет проблемы)

**Паттерн взаимодействия**:
```
Orchestrator → create plan → exit
Main session → invoke worker → worker completes → exit
Orchestrator → resume → validate → next phase
```

### 4.2. Example: /health-bugs workflow

**Phase 1: Bug Detection**

Orchestrator создаёт `.tmp/current/bug-hunting-plan.json`:
```json
{
  "phase": "detection",
  "config": {
    "scope": "full",
    "categories": ["syntax", "logic", "type", "runtime"],
    "excludePatterns": ["node_modules/", "dist/", ".next/"]
  },
  "validation": {
    "required": true,
    "minReportSections": 5
  }
}
```

Orchestrator сигнализирует готовность и **exits**.

Main session вызывает `bug-hunter` worker:
```
Task tool: invoke bug-hunter
```

**bug-hunter worker** (`.claude/agents/health/workers/bug-hunter.md`):

**Phase 1**: Read plan file
```typescript
const plan = JSON.parse(await readFile('.tmp/current/bug-hunting-plan.json'));
```

**Phase 2**: Execute work
```bash
# Grep для паттернов
grep -r "console\.log" src/  # Debug statements left behind
grep -r "TODO\|FIXME" src/  # Incomplete implementations

# Type-check для type errors
pnpm type-check 2>&1 | tee type-errors.txt

# Lint для code smells
pnpm lint 2>&1 | tee lint-errors.txt
```

**Phase 3**: Categorize bugs
```typescript
const bugs = [
  {
    severity: 'critical',
    category: 'type',
    file: 'src/api/users.ts:45',
    description: 'Property "id" does not exist on type "Partial<User>"',
    impact: 'Runtime error when accessing user.id'
  },
  {
    severity: 'high',
    category: 'logic',
    file: 'src/utils/validation.ts:12',
    description: 'Validation bypassed for empty strings',
    impact: 'Security: empty emails accepted'
  },
  // ... more bugs
];
```

**Phase 4**: Generate report (`.tmp/current/bug-hunting-report.md`)
```markdown
# Bug Detection Report

## Summary
- **Total bugs found**: 23
- **Critical**: 3
- **High**: 7
- **Medium**: 10
- **Low**: 3

## Critical Bugs

### 1. Type Error in src/api/users.ts:45
**Category**: Type Safety
**Severity**: Critical
**Description**: Property "id" does not exist on type "Partial<User>"

**Code**:
```typescript
const userId = user.id;  // ❌ user might be Partial<User>
```

**Impact**: Runtime error when accessing undefined property

**Root Cause**: getUserById returns Partial<User> for incomplete data, but code assumes full User

**Suggested Fix**:
```typescript
if (!user.id) {
  throw new Error('User ID is required');
}
const userId = user.id;  // ✓ Now safe
```

## High Priority Bugs

### 2. Logic Error in src/utils/validation.ts:12
...

## Quality Gates

- ✓ Type-check executed
- ✓ Lint executed
- ✓ Pattern search completed
- ✓ All bugs categorized

## Next Steps

Prioritize fixes by severity:
1. Critical bugs (3 issues) → Fix immediately
2. High bugs (7 issues) → Fix in current sprint
3. Medium/Low → Backlog
```

**Phase 5**: Return control (worker exits)

---

**Phase 2: Bug Fixing**

Orchestrator resumes, validates report, creates `.tmp/current/bug-fixing-plan.json`:
```json
{
  "phase": "fixing",
  "config": {
    "priority": "critical",
    "maxBugsPerIteration": 5,
    "requireTests": true
  },
  "bugs": [
    {
      "id": "bug-001",
      "file": "src/api/users.ts:45",
      "description": "Type error: Property 'id' does not exist",
      "suggestedFix": "Add type guard before accessing .id"
    }
  ],
  "validation": {
    "typeCheck": true,
    "build": true,
    "tests": false
  }
}
```

Orchestrator exits.

Main session вызывает `bug-fixer` worker.

**bug-fixer worker**:

**Phase 1**: Read plan

**Phase 2**: Fix bugs one by one
```typescript
// For each bug:
// 1. Read file
const content = await readFile('src/api/users.ts');

// 2. Apply fix
const fixed = content.replace(
  'const userId = user.id;',
  `if (!user.id) throw new Error('User ID required');\nconst userId = user.id;`
);

// 3. Write file
await writeFile('src/api/users.ts', fixed);
```

**Phase 3**: Validate (using `run-quality-gate` Skill)
```typescript
// Skill: run-quality-gate
const result = await runQualityGate({
  command: 'pnpm type-check',
  blocking: true
});

if (result.status === 'FAILED') {
  // Rollback changes
  await rollbackChanges();
  throw new Error('Type-check failed after fix');
}
```

**Phase 4**: Generate report

**Phase 5**: Return control

---

**Phase 3: Verification**

Orchestrator resumes, re-runs bug-hunter для проверки remaining issues.

**If issues remain AND iterations < max**:
- Repeat Phase 2 with next priority (high → medium → low)

**If clean OR max iterations**:
- Generate final summary
- Exit workflow

### 4.3. Iterative Refinement

**Почему итеративно?**

Сложные кодовые базы имеют сотни проблем. Фиксить все сразу → context overflow.

**Наше решение**:
1. Fix critical bugs → validate → verify → commit
2. Fix high bugs → validate → verify → commit
3. Fix medium bugs → validate → verify → commit

**Каждая итерация**:
- Изолированный контекст (worker exits после фикса)
- Validation gates (type-check, build, tests)
- Verification (re-run scanner)
- Commit (rollback point)

**Максимум итераций**: 5 (safety limit)

**Partial success handling**: Если 3 критических бага исправлены, но 2 остались → это **прогресс**, не провал.

### 4.4. Quality Gates в действии

Каждый worker использует `run-quality-gate` Skill для валидации.

**Skill invocation**:
```typescript
const gateResult = await Skill.invoke('run-quality-gate', {
  command: 'pnpm type-check && pnpm build',
  blocking: true,
  rollbackOnFailure: true
});

if (gateResult.status === 'FAILED') {
  // Worker НЕ продолжает, возвращает отчёт с ошибкой
  return {
    status: 'validation_failed',
    errors: gateResult.errors
  };
}
```

**Blocking logic**:
- `blocking: true` → worker exits, orchestrator rollbacks
- `blocking: false` → warning logged, продолжаем

**Rollback**:
```bash
# run-quality-gate Skill автоматически
git diff > .tmp/changes-to-rollback.patch
git restore src/api/users.ts
```

---

<a name="agents-list"></a>
## 5. Полный список новых агентов

За последние два месяца добавлено **44 новых агента** и **~30 скиллов**.

### 5.1. Health/Quality (10 агентов)

| Агент | Тип | Задача |
|-------|-----|--------|
| **bug-hunter** | Worker | Обнаружение багов (type errors, logic bugs, code smells) |
| **bug-fixer** | Worker | Исправление багов по priority |
| **security-scanner** | Worker | Сканирование уязвимостей (SAST, dependency audit) |
| **vulnerability-fixer** | Worker | Исправление уязвимостей |
| **dead-code-hunter** | Worker | Обнаружение мёртвого кода (Knip) |
| **dead-code-remover** | Worker | Удаление мёртвого кода |
| **reuse-hunter** | Worker | Обнаружение дублирования |
| **reuse-fixer** | Worker | Устранение дублирования |
| **dependency-auditor** | Worker | Аудит зависимостей |
| **dependency-updater** | Worker | Безопасное обновление зависимостей |

### 5.2. Infrastructure (5 агентов)

| Агент | Тип | Задача |
|-------|-----|--------|
| **deployment-engineer** | Worker | DevSecOps, GitOps, Blue-Green deployments |
| **infrastructure-specialist** | Worker | Инфраструктура (Docker, K8s, Terraform) |
| **qdrant-specialist** | Worker | Векторные базы данных (Qdrant) |
| **orchestration-logic-specialist** | Worker | Orchestration patterns |
| **quality-validator-specialist** | Worker | Quality gates, validation |

### 5.3. Development (5 агентов)

| Агент | Тип | Задача |
|-------|-----|--------|
| **problem-investigator** | Worker | Глубокое расследование проблем (multi-component systems) |
| **research-specialist** | Worker | Технические исследования |
| **code-reviewer** | Worker | Код-ревью с checklist |
| **typescript-types-specialist** | Worker | TypeScript типы и type safety |
| **skill-builder-v2** | Worker | Создание новых скиллов |

### 5.4. Testing (6 агентов)

| Агент | Тип | Задача |
|-------|-----|--------|
| **test-writer** | Worker | Написание тестов (unit, integration) |
| **integration-tester** | Worker | Интеграционные тесты |
| **performance-optimizer** | Worker | Оптимизация производительности |
| **accessibility-tester** | Worker | Тесты доступности (a11y) |
| **mobile-responsiveness-tester** | Worker | Мобильная адаптивность |
| **mobile-fixes-implementer** | Worker | Исправление мобильных проблем |

### 5.5. Frontend (3 агента)

| Агент | Тип | Задача |
|-------|-----|--------|
| **nextjs-ui-designer** | Worker | UI дизайн для Next.js |
| **visual-effects-creator** | Worker | Визуальные эффекты |
| **fullstack-nextjs-specialist** | Worker | Fullstack разработка (Next.js + API) |

### 5.6. Content (1 агент)

| Агент | Тип | Задача |
|-------|-----|--------|
| **article-writer-multi-platform** | Worker | Написание статей для VC.ru, Habr, Telegram, Medium, LinkedIn, YouTube |

### 5.7. Database (3 агента)

| Агент | Тип | Задача |
|-------|-----|--------|
| **database-architect** | Worker | Проектирование баз данных |
| **supabase-auditor** | Worker | Аудит Supabase проектов |
| **api-builder** | Worker | REST/GraphQL API |

### 5.8. Orchestrators (5 агентов)

| Агент | Тип | Задача |
|-------|-----|--------|
| **bug-orchestrator** | Orchestrator | Координация /health-bugs workflow |
| **security-orchestrator** | Orchestrator | Координация /health-security workflow |
| **dependency-orchestrator** | Orchestrator | Координация /health-deps workflow |
| **dead-code-orchestrator** | Orchestrator | Координация /health-cleanup workflow |
| **reuse-orchestrator** | Orchestrator | Координация reuse detection/fixing |

### 5.9. Ключевые скиллы (~30 total)

**Debugging & Quality**:
- `systematic-debugging` — Iron Law: "NO FIXES WITHOUT ROOT CAUSE"
- `bug-health-inline` — Inline orchestration для bug detection
- `run-quality-gate` — Quality gates с blocking logic

**Content & Research**:
- `content-research-writer` — Исследование с цитатами для статей
- `lead-research-assistant` — Поиск лидов для продаж

**DevOps**:
- `senior-devops` — CI/CD, Infrastructure as Code, deployment strategies

**Design**:
- `canvas-design` — Визуальный дизайн, постеры
- `algorithmic-art` — Генеративное искусство с p5.js
- `theme-factory` — 10 готовых тем для дизайна
- `artifacts-builder` — Артефакты для claude.ai (React/Tailwind)

**Engineering**:
- `senior-prompt-engineer` — Промпт-инжиниринг, LLM оптимизация
- `ux-researcher-designer` — UX исследования
- `ui-design-system` — Дизайн-системы
- `code-reviewer` — Чек-листы код-ревью

**Utilities**:
- `parse-error-logs`, `parse-git-status`, `parse-package-json` — Парсеры
- `format-commit-message`, `format-markdown-table`, `format-todo-list` — Форматтеры
- `generate-changelog`, `generate-report-header` — Генераторы
- `validate-plan-file`, `validate-report-file` — Валидаторы
- `rollback-changes` — Откат изменений

---

<a name="disclaimer"></a>
## Disclaimer: Expected Pushback

Я понимаю, что эта статья, вероятно, получит значительный pushback от разработчиков. Истории про "vibe coding", опасения про AI, заменяющий программистов, обвинения в упрощении.

**Моё мнение**: Я думаю, эта реакция больше про **страх, смешанный с высокомерием**, чем про настоящую техническую критику.

**Страх**: "Если AI может делать мою работу, что случится со мной?"
**Высокомерие**: "Только люди могут писать *настоящий* код, AI — это просто игрушка."

**Реальность**: AI не заменяет хороших разработчиков. Он их усиливает. Orchestrator kit — не про замену программистов, а про удаление повторяющихся задач, автоматизацию проверок качества и сохранение контекста, чтобы разработчики могли фокусироваться на архитектуре и сложных проблемах.

Если не согласны — отлично. Клонируйте репозиторий, попробуйте, потом скажите мне, где я не прав. Я предпочитаю технические аргументы эмоциональным реакциям.

**Конкретные технические возражения приветствуются**:
- "GitOps не подходит для X случая, потому что..."
- "Blue-Green deployment требует Y, чего нет в примере..."
- "Systematic debugging fails когда..."

Эти обсуждения полезны. Emotional reactions — нет.

---

<a name="try"></a>
## 6. Как попробовать

### 6.1. Установка

**NPM**:
```bash
npm install -g claude-code-orchestrator-kit
# или
npx claude-code-orchestrator-kit
```

**Manual**:
```bash
git clone https://github.com/maslennikov-ig/claude-code-orchestrator-kit.git
cd claude-code-orchestrator-kit
cp .env.example .env.local  # Configure credentials
./switch-mcp.sh  # Select MCP configuration
# Restart Claude Code
```

### 6.2. First Steps

1. Скопируйте `.claude/` в ваш проект
2. Скопируйте `mcp/` configurations
3. Скопируйте `CLAUDE.md` (behavioral OS)
4. Настройте `.env.local`
5. Запустите `./switch-mcp.sh` → выберите BASE
6. Рестартуйте Claude Code
7. Попробуйте `/health-bugs` для проверки setup

### 6.3. Примеры команд

```bash
# Health workflows
/health-bugs          # Обнаружение и исправление багов
/health-security      # Сканирование уязвимостей
/health-deps          # Аудит зависимостей
/health-cleanup       # Удаление мёртвого кода

# Deployment
# В Claude Code:
Invoke deployment-engineer agent with task: "Setup CI/CD with DevSecOps gates"

# Debugging
# Автоматически используется когда встречается баг
# Или вручную: "Use systematic-debugging skill to investigate this error"

# Worktrees (параллельная разработка)
/worktree-create feature/new-auth
# VS Code → switch to .worktrees/feature-new-auth/
# Separate Claude Code session → isolated context
```

---

<a name="contacts"></a>
## 7. Контакты и обратная связь

### 📱 Telegram

**Канал** (редкие, но интересные посты): https://t.me/maslennikovigor
Заходите, читайте мои мысли и статьи. Я не публикую часто, но когда публикую — это стоит того.

**Прямой контакт**: https://t.me/maslennikovig
Нужно поговорить? Пишите мне напрямую. Всегда рад связаться.

### 💬 Feedback: Я широко открыт

**Мне интересно услышать**:
- **Критику** — Что не так с этим подходом? Где слабые места?
- **Идеи** — Какие функции должны быть добавлены? Чего не хватает?
- **Предложения** — Как улучшить, оптимизировать или рефакторить систему?
- **Вопросы** — Что-то непонятно? Спрашивайте.

**Каналы для обратной связи**:
- **GitHub Issues**: https://github.com/maslennikov-ig/claude-code-orchestrator-kit/issues (для багов, фич)
- **Telegram**: https://t.me/maslennikovig (для идей, вопросов, прямого разговора)

**Тон**: Супер открыт к конструктивному диалогу. Без эго, просто хочу сделать это лучше.

---

## Источники

- [Google DeepMind's CodeMender](https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/)
- [OpenAI's Aardvark](https://openai.com/index/introducing-aardvark/)
- [CrowdStrike Multi-Agent Security System](https://www.crowdstrike.com/en-us/blog/secure-ai-generated-code-with-multiple-self-learning-ai-agents/)
- [GitOps Principles](https://www.gitops.tech/)
- [Blue-Green Deployment Pattern](https://martinfowler.com/bliki/BlueGreenDeployment.html)

---

## Image Prompts for Cover

### Prompt 1 (★★★★★)
Technical DevSecOps pipeline visualization: multi-stage security gates flowing through a futuristic blue-green deployment system. Dark background with glowing cyan and emerald gradient accents. Isometric 3D style showing CI/CD pipeline stages (secret scan, SAST, container security) as connected glowing nodes. Docker containers in dual blue/green environments with automated traffic routing. Code snippets and terminal windows floating in holographic displays. Style: technical infographic meets cyberpunk aesthetic, sharp geometric shapes, high contrast, professional but visually striking.

### Prompt 2 (★★★★☆)
Abstract representation of AI agent orchestration: central orchestrator node (golden glow) connected to specialized worker agents (various colors: security-red, infrastructure-blue, testing-green, debugging-purple) arranged in a neural network pattern. Return Control pattern visualized as bidirectional flow arrows with data passing through plan files (JSON visualized as structured nodes). Dark navy background, circuit board texture, clean modern design. Style: software architecture diagram meets abstract digital art, minimalist but informative.

### Prompt 3 (★★★☆☆)
Split-screen comparison: left side showing chaotic random debugging (tangled red lines, error symbols, frustrated developer silhouette), right side showing systematic debugging flow (clean white directional arrows, organized phases, Iron Law text "NO FIXES WITHOUT ROOT CAUSE" in bold typography). Middle divider with "vs" symbol. Color scheme: left (red/orange chaos), right (blue/green order). Style: editorial illustration, bold contrast, clear visual metaphor, professional technical magazine aesthetic.
