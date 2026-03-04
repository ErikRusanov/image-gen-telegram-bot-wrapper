FROM python:3.12-slim
WORKDIR /app
RUN pip install poetry && poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-interaction --no-root
COPY bot/ ./bot/
CMD ["python", "-m", "bot.main"]
