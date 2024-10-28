.PHONY: all

SHELL=/bin/bash -e
STORAGES=docker-compose/storages.yaml

up_storages:
	docker-compose --env-file .env -f ${STORAGES} up -d

down:
	docker-compose --env-file .env-f ${STORAGES} down

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m="$(m)"

downgrade:
	alembic downgrade -1