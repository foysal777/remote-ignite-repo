#!/bin/sh

echo "⏳ Waiting for PostgreSQL..."

while ! nc -z postgres 5432; do
  sleep 2
done

echo "✅ PostgreSQL started"

echo "🚀 Running migrations..."
python manage.py migrate --noinput

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔥 Starting Gunicorn..."

exec "$@"