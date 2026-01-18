# Blue-Green Deployment + Dev/Staging Article Materials

## Article Context

**Platform:** Habr (primary), can adapt for Tenchat later
**Author:** Igor Maslennikov
**Previous Article:** "2 часа в день на баги → 15 минут" (promised Blue-Green in next article)
**Target Length:** 20,000-25,000 characters
**Language:** Russian

## Article Goals

1. Explain Blue-Green deployment strategy in practical terms
2. Show real production setup (not toy examples)
3. Demonstrate Dev/Staging environment isolation
4. Provide actionable knowledge for setting up similar infrastructure

## Key Technical Details

### Architecture Overview

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

### Environment Strategy

| Domain | Environment | Branch | Deploy Strategy | Description |
|--------|-------------|--------|-----------------|-------------|
| dev.ai.megacampus.ru | Dev | develop | Simple rolling | Fast iteration, no zero-downtime |
| ai.megacampus.ru | Staging | master | Blue/Green | Zero-downtime, instant rollback |
| TBD | Production | TBD | Blue/Green | Future expansion |

### Port Allocation

| Environment | Web Port | API Port |
|-------------|----------|----------|
| Blue (Staging) | 3001 | 4001 |
| Green (Staging) | 3002 | 4002 |
| Dev | 3010 | 4010 |

### Key Scripts

**deploy_blue_green.sh workflow:**
1. Determine active color (read `active_color` file)
2. Calculate new color (blue→green, green→blue)
3. Ensure infrastructure running (docker-compose.infra.yml)
4. Copy env file, add color-specific vars (ports, project name)
5. Pull new Docker images from GHCR
6. Start new color containers
7. Health checks (12 retries, 60s total timeout)
   - Check API: `curl localhost:$PORT/health`
   - Check Web: `curl localhost:$PORT`
8. If healthy → switch Nginx (sed template → reload)
9. Update `active_color` state file
10. Stop old color containers

**rollback_blue_green.sh workflow:**
1. Read current active color
2. Calculate target (previous) color
3. Ensure infrastructure running
4. Start target color (if not running)
5. Health checks (6 retries, 30s timeout)
6. Switch Nginx to target
7. Update state
8. Stop broken color

### CI/CD Pipeline (8 Stages)

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

### Docker Compose Split

**docker-compose.infra.yml** (shared, always running):
- Redis (1 CPU, 1GB RAM) - queue state, sessions
- Docling MCP (2 CPU, 4GB RAM) - document processing
- Workers (2 CPU, 2GB RAM) - stages 1-6
- Worker-stage7 (1 CPU, 1GB RAM) - enrichment

**docker-compose.app.yml** (Blue/Green switchable):
- web (2 CPU, 2GB RAM) - Next.js frontend
- api (2 CPU, 2GB RAM) - Express + tRPC backend
- Parameterized via env: WEB_PORT, API_PORT, COLOR, COMPOSE_PROJECT_NAME

**docker-compose.dev.yml** (separate dev environment):
- web-dev, api-dev (reduced resources: 1 CPU, 1GB)
- worker-dev, worker-stage7-dev (separate queues)
- BULLMQ_QUEUE_NAME=course-generation-dev (queue isolation)

### Nginx Configuration

**Key features:**
- SSL via Let's Encrypt
- Template-based port switching: `{{WEB_PORT}}`, `{{API_PORT}}`
- Long timeouts for API (300s for LLM operations)
- Buffer size adjustments (512k for large headers)
- Gzip compression
- Security headers (X-Frame-Options, X-XSS-Protection)
- No-cache for HTML (prevents stale deployments)

**Traffic switch:**
```bash
sed -e "s/{{WEB_PORT}}/$NEW_WEB_PORT/g" \
    -e "s/{{API_PORT}}/$NEW_API_PORT/g" \
    nginx.conf.template | sudo tee /etc/nginx/sites-enabled/megacampus
sudo nginx -t && sudo nginx -s reload
```

### Health Checks

| Check | Endpoint | Timeout | Retries |
|-------|----------|---------|---------|
| API | /health | 5s | 12 (deploy), 6 (rollback) |
| Web | / | 5s | 12 (deploy), 6 (rollback) |

### Key Benefits (for article)

**Zero Downtime:**
- Old version serves traffic while new version starts
- Traffic switch is instant (nginx reload)
- Users see no interruption

**Instant Rollback:**
- Previous version's containers may still be running
- If not, script starts them
- 30 seconds to full rollback

**Environment Isolation:**
- Dev uses separate queues (BULLMQ_QUEUE_NAME)
- Dev uses separate uploads directory
- Dev uses separate Docker project names
- Changes on dev don't affect staging

**Resource Efficiency:**
- Shared infrastructure (Redis, Docling, Workers)
- Only application containers are duplicated
- During deploy: temporary 2x app resources (~8GB → ~12GB)
- After deploy: back to normal (~8GB)

### Real Numbers (from production)

**Deploy timing:**
- CI pipeline: ~8-12 minutes
- Docker build: ~3-5 minutes (with cache)
- Health check: ~30-60 seconds
- Total: ~10-15 minutes from push to production

**Resource usage:**
- Server: 8 CPU, 11GB RAM total
- Blue/Green slots: 4 CPU, 4GB each (max)
- Shared infra: 6 CPU, 8GB
- Peak during deploy: ~10GB RAM

**Rollback timing:**
- Script execution: ~30-60 seconds
- If containers already running: ~10 seconds
- If containers need to start: ~30 seconds

### Automation via GitHub Actions

**Triggers:**
- Push to `master` → Production (Blue/Green)
- Push to `develop` → Dev (simple)
- PR → CI only (no deploy)
- Manual dispatch with options (skip_tests, force_deploy)

**Secrets (GitHub Environments):**
- DEPLOY_SSH_KEY
- SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY
- QDRANT_URL, QDRANT_API_KEY
- OPENROUTER_API_KEY
- TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

**Notifications:**
- Telegram message on deploy success/failure
- Contains: commit SHA, branch, author, link to logs

## Article Outline

### Title Options

1. "git push → production за 10 минут: настраиваем Blue-Green деплой с нуля"
2. "Zero-downtime деплой на одном сервере: практический гайд"
3. "Деплой без страха: как Blue-Green и изолированные окружения спасают продакшен"
4. "От git push до production: автоматизация деплоя с Blue-Green и CI/CD"

### Structure

1. **Intro (боль)**
   - Деплой в 3 часа ночи — классика
   - "Откатывайте!" через 5 минут после деплоя
   - Страх деплоить в рабочее время
   - Тестировали на dev, сломали на stage

2. **Решение: архитектура**
   - Multi-environment (Dev/Staging/Prod)
   - Blue-Green для zero-downtime
   - Shared infrastructure для экономии ресурсов

3. **Blue-Green: как это работает**
   - Два слота, nginx переключает трафик
   - Health checks перед switch
   - State file для отслеживания активного цвета
   - Детальный разбор скрипта

4. **Изоляция окружений**
   - Зачем отдельный dev
   - Queue isolation (разные BullMQ queues)
   - Отдельные данные (uploads-dev)

5. **CI/CD Pipeline**
   - 8 стадий, параллельные проверки
   - Docker build с кэшированием
   - Автоматический rollback при ошибке
   - Telegram уведомления

6. **Rollback: когда всё пошло не так**
   - 30 секунд до отката
   - Автоматический при failure в CI/CD
   - Ручной запуск если нужно

7. **Результаты**
   - Деплой в любое время дня
   - 10-15 минут от push до production
   - Спокойный сон

8. **Как внедрить у себя**
   - Минимальная версия (без CI/CD)
   - Полная версия (как у меня)
   - Checklist для настройки

9. **Ссылки**
   - GitHub репозиторий с примерами
   - ADR документы
   - Предыдущая статья про error fixing

## Code Examples for Article

### Deploy Script (simplified for article)
```bash
# 1. Determine colors
CURRENT=$(cat active_color)  # blue
NEW=$([ "$CURRENT" == "blue" ] && echo "green" || echo "blue")

# 2. Start new version
docker compose -f app.yml --env-file .env.$NEW up -d

# 3. Health check
for i in {1..12}; do
  curl -s localhost:$NEW_PORT/health && break
  sleep 5
done

# 4. Switch traffic
sed "s/{{PORT}}/$NEW_PORT/" nginx.template > /etc/nginx/sites-enabled/app
nginx -s reload

# 5. Update state & cleanup
echo $NEW > active_color
docker compose -f app.yml -p "app-$CURRENT" down
```

### Rollback (one-liner)
```bash
ssh server "cd /opt/app && bash scripts/rollback_blue_green.sh"
```

### Health Check in CI/CD
```yaml
- name: Verify deployment
  run: |
    sleep 30
    curl -f https://ai.megacampus.ru/api/health || exit 1
```

## Author Info

**Igor Maslennikov**
- AI Dev Team @ DNA IT
- Claude Code Orchestrator Kit maintainer
- 10+ years in IT, 2 years with AI agents

**Links:**
- GitHub: github.com/maslennikov-ig/claude-code-orchestrator-kit
- Telegram: @maslennikovigor (channel), @maslennikovig (personal)

## Previous Article Reference

В предыдущей статье "2 часа в день на баги → 15 минут" я обещал рассказать про:
- Blue-Green деплой
- Dev и Staging окружения
- CI/CD pipeline

Эта статья — выполнение обещания.
