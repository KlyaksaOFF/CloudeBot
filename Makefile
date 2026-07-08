lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

start:
	uv run start.py