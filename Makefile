.PHONY: all

BACKEND_APP = docker_compose/app.yaml
SHELL=/bin/bash -e
STORAGES=docker_compose/storage.yaml
ENV = --env-file .env


backend_up:
	docker compose ${ENV} -f ${BACKEND_APP} up -d --build

backend_down:
	docker compose ${ENV} -f ${BACKEND_APP} down

up_storages:
	docker compose --env-file .env -f ${STORAGES} up -d

down:
	docker compose --env-file .env -f ${STORAGES} down

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m="$(m)"

downgrade:
	alembic downgrade -1