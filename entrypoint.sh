#!/bin/sh
set -ex

echo "Waiting for Postgres..."

until /app/.venv/bin/python -c "
import socket
s = socket.socket()
s.settimeout(1)
s.connect(('db', 5432))
s.close()
"; do
  sleep 1
done

echo "Running migrations..."
/app/.venv/bin/python -m alembic upgrade head

echo "Starting FastAPI..."
exec /app/.venv/bin/uvicorn src.main:app --host 0.0.0.0 --port ${PORT}
