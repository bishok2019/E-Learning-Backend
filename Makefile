DC := docker compose
# ── Help ──────────────────────────────────────────────────────────────────────

.PHONY: help
help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make app <app_name>                 Create a new FastAPI app"
	@echo "  make revision \"message\"              Generate Alembic migration"
	@echo "  make migrate                         Apply migrations"
	@echo "  make downgrade                       Rollback last migration"
	@echo "  make current                         Show current migration"
	@echo "  make history                         Show migration history"
	@echo ""
	@echo "Docker:"
	@echo "  make build                           Build Docker images"
	@echo "  make up                              Start all containers"
	@echo "  make down                            Stop all containers"
	@echo "  make restart                         Restart all containers"
	@echo "  make logs                            Follow all container logs"
	@echo ""
	@echo "Web Command:"
	@echo "make web-logs						  Follow web logs"
	@echo "make web-shell						  Enter web shell"
	@echo "make web-restart						  Restart Web Container"
	@echo ""
	@echo "DB Command:"
	@echo "make db-logs						   	  Follow db logs"
	@echo "make db-psql						      Enter psql shell"
	@echo "make db-shell						  Enter db shell"
	@echo ""
	@echo "Management Command:"
	@echo "  make permission                      Create permissions and category"
	@echo "  make flush                           Flush all data"
	@echo "  make superuser                       Create superuser"
	@echo ""

# ── apps ───────────────────────────────────────────────────────────────
.PHONY: app
app:
	@bash create_app.sh $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

# ── Alembic ───────────────────────────────────────────────────────────────────

.PHONY: revision upgrade downgrade current history
revision:
	@if [ -z "$(word 2,$(MAKECMDGOALS))" ]; then \
		echo 'Usage: make revision "your message"'; \
		exit 1; \
	fi
	$(DC) exec web alembic revision --autogenerate -m "$(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))"

upgrade:
	$(DC) exec web alembic upgrade head

downgrade:
	$(DC) exec web alembic downgrade -1

current:
	$(DC) exec web alembic current

history:
	$(DC) exec web alembic history
# ── Docker Container Command ────────────────────────────────────────────────────────────────────

.PHONY: ps logs build up down remove restart
ps:
	$(DC) ps

logs:
	$(DC) logs -f

build:
	$(DC) build

up:
	$(DC) up -d

down:
	$(DC) down

remove:
	$(DC) down -v

restart:
	$(DC) restart

# ----------------------------Web Command-------------------

.PHONY: web-shell web-logs web-restart
web-shell:
	$(DC) exec -it web bash

web-logs:
	$(DC) logs -f web

web-restart:
	$(DC) restart web


# ----------------------------DB Command-------------------
.PHONY: db-shell db-psql db-logs
db-shell:
	$(DC) exec -it db bash

db-psql:

	$(DC) exec -it db psql -U admin e_learning_db

db-logs:
	$(DC) logs -f db

# ----------------------------NginX Command-----------------
.PHONY: nginx-logs nginx-shell nginx-test nginx-reload

nginx-logs:
	$(DC) logs -f nginx

nginx-shell:
	$(DC) exec -it nginx sh

nginx-test:
	$(DC) exec nginx nginx -t

nginx-reload:
	$(DC) exec nginx nginx -s reload
# ───────────────── Management command-------------------------
.PHONY: permission flush seed_db
permission:
	$(DC) exec web python manage.py seed_permissions

flush:
	$(DC) exec web python manage.py flush_data
seed_db:
	$(DC) exec web python manage.py seed_db


.PHONY: superuser
superuser:
	$(DC) exec web python manage.py createsuperuser

# ── Positional Arguments ──────────────────────────────────────────────────────

%:
	@: