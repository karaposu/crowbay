VENV := .venv/bin
M ?= update

run:
	cd src && ../$(VENV)/python -m uvicorn app:app --reload --port 8000

bot:
	cd src && ../$(VENV)/python -m bot.main

test:
	$(VENV)/pytest

migrate:
	$(VENV)/alembic upgrade head

makemigration:
	$(VENV)/alembic revision --autogenerate -m "$(M)"

seed:
	cd src && ../$(VENV)/python -m db.seed

lint:
	$(VENV)/ruff check src && $(VENV)/ruff format --check src

format:
	$(VENV)/ruff format src && $(VENV)/ruff check --fix src

.PHONY: run test migrate makemigration seed lint format
