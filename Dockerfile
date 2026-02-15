FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-cache --no-install-project

COPY ./src ./src

FROM python:3.12-slim
WORKDIR /app

ENV PYTHONPATH=/app
ENV PORT=8000

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

COPY ./migration ./migration
COPY ./alembic.ini ./alembic.ini

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
