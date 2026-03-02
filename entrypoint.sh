#!/bin/sh
set -e

cd /app

echo "Loading AWS Secrets..."
eval "$(python load_secrets_env.py)"
echo "Secrets exported."

echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 2
done

echo "PostgreSQL started"

echo "Making migrations..."
python manage.py makemigrations --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec "$@"