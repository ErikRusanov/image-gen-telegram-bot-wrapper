run:
	poetry run python -m bot.main

build:
	docker build -t image-gen-bot .

format:
	poetry run ruff format .
	poetry run ruff check --fix .
