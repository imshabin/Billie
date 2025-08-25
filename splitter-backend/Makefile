# Top-level Makefile for splitter-backend
# Works in Git Bash (Windows), macOS, Linux

SHELL := /usr/bin/env bash

APP_PORT ?= 8080
DC ?= docker compose
ALEMBIC := alembic -c backend/alembic.ini
PYTHONPATH_ENV := PYTHONPATH=backend

.PHONY: help setup up down fmt lint type test rev migrate run precommit clean

help:
	@echo "Targets:"
	@echo "  setup      - install deps (runtime + dev) & install pre-commit"
	@echo "  up         - start Postgres & Redis (Docker)"
	@echo "  down       - stop and remove containers/volumes"
	@echo "  fmt        - auto-fix with ruff"
	@echo "  lint       - lint with ruff"
	@echo "  type       - mypy type-check"
	@echo "  test       - run pytest"
	@echo "  rev m='msg'- Alembic autogenerate revision"
	@echo "  migrate    - apply latest Alembic migrations"
	@echo "  run        - run FastAPI via uvicorn on port $(APP_PORT)"
	@echo "  precommit  - run pre-commit on all files"
	@echo "  clean      - remove caches"

setup:
	python -m pip install -e . && python -m pip install -e ".[dev]" && pre-commit install

up:
	$(DC) up -d

down:
	$(DC) down -v

fmt:
	ruff check . --fix

lint:
	ruff check .

type:
	$(PYTHONPATH_ENV) mypy backend/app

test:
	$(PYTHONPATH_ENV) pytest -q

rev:
	@if [ -z "$(m)" ]; then echo "Usage: make rev m='message'"; exit 1; fi
	$(ALEMBIC) revision --autogenerate -m "$(m)"

migrate:
	$(ALEMBIC) upgrade head

run:
	uvicorn app.main:app --reload --app-dir backend --port $(APP_PORT)

precommit:
	pre-commit run --all-files

clean:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} \; || true
	rm -rf .pytest_cache .mypy_cache
