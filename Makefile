.PHONY: all

APP_UP=docker-compose.yaml
SHELL=/bin/bash -e
ENV = --env-file .env


app_up:
	docker-compose up -d --build

app_down:
	docker-compose down

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m="$(m)"

downgrade:
	alembic downgrade -1