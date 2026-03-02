#!/bin/sh
set -e

cd /app

echo "Loading AWS Secrets..."
python load_secrets_env.py > /app/.env.runtime

set -a
. /app/.env.runtime
set +a

echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 2
done

echo "PostgreSQL started"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec "$@"


