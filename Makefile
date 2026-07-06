lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

bot-start:
	uv run start.py