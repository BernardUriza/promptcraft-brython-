.PHONY: help dev-all dev-backend dev-frontend build test lint migrate seed clean

# Colors for terminal output
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "$(GREEN)PromptCraft - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================
# DEVELOPMENT
# ============================================

dev-all: ## Start ALL services for development (main command)
	@echo "$(GREEN)Starting PromptCraft development environment...$(NC)"
	@echo "$(YELLOW)Services: PostgreSQL, Redis, FastAPI, Celery, Nginx$(NC)"
	@echo ""
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

dev-detached: ## Start all services in background
	@echo "$(GREEN)Starting PromptCraft in background...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
	@echo "$(GREEN)Services started! Access at http://localhost:8080$(NC)"

dev-backend: ## Start only backend services (db, redis, api)
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build db redis backend

dev-db: ## Start only database services
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build db redis

stop: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose down
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

# ============================================
# LOGS
# ============================================

logs: ## Show all logs
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-db: ## Show database logs
	docker-compose logs -f db

logs-celery: ## Show celery logs
	docker-compose logs -f celery celery-beat

# ============================================
# BUILD
# ============================================

build: ## Build all containers
	docker-compose build

build-no-cache: ## Build all containers without cache
	docker-compose build --no-cache

build-prod: ## Build for production
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# ============================================
# DATABASE
# ============================================

migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

migrate-create: ## Create new migration (usage: make migrate-create MSG="description")
	docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

migrate-rollback: ## Rollback last migration
	docker-compose exec backend alembic downgrade -1

migrate-history: ## Show migration history
	docker-compose exec backend alembic history

seed: ## Seed database with sample data
	docker-compose exec backend python -m scripts.seed_data

db-shell: ## Open PostgreSQL shell
	docker-compose exec db psql -U promptcraft -d promptcraft

db-reset: ## Reset database (WARNING: destroys all data)
	@echo "$(RED)WARNING: This will destroy all data!$(NC)"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	docker-compose down -v
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d db
	@sleep 5
	docker-compose exec backend alembic upgrade head
	docker-compose exec backend python -m scripts.seed_data

# ============================================
# TESTING
# ============================================

test: ## Run all tests
	docker-compose exec backend pytest -v

test-cov: ## Run tests with coverage report
	docker-compose exec backend pytest --cov=app --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	docker-compose exec backend pytest-watch

# ============================================
# LINTING & FORMATTING
# ============================================

lint: ## Run linters
	docker-compose exec backend ruff check app/

lint-fix: ## Fix linting issues
	docker-compose exec backend ruff check app/ --fix

format: ## Format code
	docker-compose exec backend ruff format app/

type-check: ## Run type checking with mypy
	docker-compose exec backend mypy app/

# ============================================
# SHELL ACCESS
# ============================================

shell-backend: ## Open bash shell in backend container
	docker-compose exec backend bash

shell-db: ## Open psql shell
	docker-compose exec db psql -U promptcraft -d promptcraft

shell-redis: ## Open Redis CLI
	docker-compose exec redis redis-cli

shell-python: ## Open Python shell with app context
	docker-compose exec backend python -c "from app.main import app; import code; code.interact(local=locals())"

# ============================================
# REDIS COMMANDS
# ============================================

redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

redis-flush: ## Flush Redis cache (WARNING)
	docker-compose exec redis redis-cli FLUSHALL

redis-monitor: ## Monitor Redis commands
	docker-compose exec redis redis-cli MONITOR

# ============================================
# CLEANUP
# ============================================

clean: ## Stop and remove all containers
	docker-compose down

clean-all: ## Remove containers, volumes, and images
	docker-compose down -v --rmi local
	docker system prune -f

clean-volumes: ## Remove only volumes (destroys data)
	docker-compose down -v

# ============================================
# PRODUCTION
# ============================================

prod-up: ## Start production environment
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down: ## Stop production environment
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

prod-logs: ## Show production logs
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# ============================================
# INITIAL SETUP
# ============================================

init: ## Initial project setup (run once)
	@echo "$(GREEN)Setting up PromptCraft...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(YELLOW)Created .env file. Please edit with your settings.$(NC)"; \
	fi
	@echo "Building containers..."
	docker-compose build
	@echo "Starting database..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d db redis
	@sleep 5
	@echo "Running migrations..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm backend alembic upgrade head
	@echo "Seeding database..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml run --rm backend python -m scripts.seed_data
	docker-compose down
	@echo ""
	@echo "$(GREEN)Setup complete!$(NC)"
	@echo "Run '$(YELLOW)make dev-all$(NC)' to start the development server"
	@echo "Access the app at $(GREEN)http://localhost:8080$(NC)"

# ============================================
# STATUS & INFO
# ============================================

status: ## Show status of all containers
	docker-compose ps

info: ## Show project info
	@echo "$(GREEN)PromptCraft - Interactive Prompt Engineering Course$(NC)"
	@echo ""
	@echo "URLs:"
	@echo "  Frontend:  http://localhost:8080"
	@echo "  API:       http://localhost:8000"
	@echo "  API Docs:  http://localhost:8000/docs"
	@echo ""
	@echo "Services:"
	@docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
