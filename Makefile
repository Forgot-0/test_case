.PHONY: all

BACKEND_APP = docker_compose/app.yaml
SHELL=/bin/bash -e
STORAGES=docker_compose/storage.yaml
ENV = --env-file .env


migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m="$(m)"

downgrade:
	alembic downgrade -1