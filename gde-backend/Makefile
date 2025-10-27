# Makefile para GDE Backend

.PHONY: help build dev prod up down logs shell test clean

# Variables
DOCKER_COMPOSE_DEV = docker-compose -f docker-compose.yml
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose.prod.yml
CONTAINER_NAME = gde-backend

help: ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir imagen de desarrollo
	docker build -f Dockerfile.dev -t gde-backend:dev .

build-prod: ## Construir imagen de producción
	docker build -f Dockerfile -t gde-backend:prod .

dev: ## Ejecutar en modo desarrollo
	$(DOCKER_COMPOSE_DEV) up --build

dev-detached: ## Ejecutar en modo desarrollo (detached)
	$(DOCKER_COMPOSE_DEV) up --build -d

prod: ## Ejecutar en modo producción
	$(DOCKER_COMPOSE_PROD) up --build

prod-detached: ## Ejecutar en modo producción (detached)
	$(DOCKER_COMPOSE_PROD) up --build -d

up: ## Levantar servicios
	$(DOCKER_COMPOSE_DEV) up -d

down: ## Detener servicios
	$(DOCKER_COMPOSE_DEV) down

down-prod: ## Detener servicios de producción
	$(DOCKER_COMPOSE_PROD) down

logs: ## Ver logs del backend
	$(DOCKER_COMPOSE_DEV) logs -f backend

logs-prod: ## Ver logs del backend (producción)
	$(DOCKER_COMPOSE_PROD) logs -f backend

shell: ## Acceder al shell del contenedor
	$(DOCKER_COMPOSE_DEV) exec backend /bin/bash

shell-prod: ## Acceder al shell del contenedor (producción)
	$(DOCKER_COMPOSE_PROD) exec backend /bin/bash

init-db: ## Inicializar base de datos
	$(DOCKER_COMPOSE_DEV) exec backend python scripts/init_db.py

test: ## Ejecutar tests
	$(DOCKER_COMPOSE_DEV) exec backend pytest

test-cov: ## Ejecutar tests con coverage
	$(DOCKER_COMPOSE_DEV) exec backend pytest --cov=app

lint: ## Ejecutar linting
	$(DOCKER_COMPOSE_DEV) exec backend flake8 app/
	$(DOCKER_COMPOSE_DEV) exec backend black --check app/
	$(DOCKER_COMPOSE_DEV) exec backend mypy app/

format: ## Formatear código
	$(DOCKER_COMPOSE_DEV) exec backend black app/
	$(DOCKER_COMPOSE_DEV) exec backend isort app/

clean: ## Limpiar contenedores e imágenes
	$(DOCKER_COMPOSE_DEV) down -v --rmi all
	docker system prune -f

clean-prod: ## Limpiar contenedores e imágenes de producción
	$(DOCKER_COMPOSE_PROD) down -v --rmi all
	docker system prune -f

restart: ## Reiniciar servicios
	$(DOCKER_COMPOSE_DEV) restart backend

restart-prod: ## Reiniciar servicios (producción)
	$(DOCKER_COMPOSE_PROD) restart backend

status: ## Ver estado de los servicios
	$(DOCKER_COMPOSE_DEV) ps

status-prod: ## Ver estado de los servicios (producción)
	$(DOCKER_COMPOSE_PROD) ps

health: ## Verificar salud de los servicios
	@echo "Backend Health:"
	@curl -f http://localhost:8000/health || echo "Backend no disponible"
	@echo "\nPostgreSQL Health:"
	@$(DOCKER_COMPOSE_DEV) exec postgres pg_isready -U gde_user -d gde_db || echo "PostgreSQL no disponible"
	@echo "\nRedis Health:"
	@$(DOCKER_COMPOSE_DEV) exec redis redis-cli ping || echo "Redis no disponible"

backup-db: ## Hacer backup de la base de datos
	$(DOCKER_COMPOSE_DEV) exec postgres pg_dump -U gde_user gde_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db: ## Restaurar base de datos desde backup (usar: make restore-db FILE=backup.sql)
	$(DOCKER_COMPOSE_DEV) exec -T postgres psql -U gde_user gde_db < $(FILE)

# Comandos de desarrollo rápido
quick-start: build dev ## Construir y ejecutar en modo desarrollo

quick-stop: down clean ## Detener y limpiar todo

# Comandos de producción
deploy: build-prod prod-detached ## Desplegar en producción

undeploy: down-prod clean-prod ## Desplegar en producción
