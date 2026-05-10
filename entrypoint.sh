#!/bin/sh
set -e

# Apply database migrations
echo "Apply database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collect static files..."
python manage.py collectstatic --noinput || true

echo "Starting server..."
# If GUNICORN is set, use gunicorn; otherwise use runserver (good for development)
if [ -n "$GUNICORN" ]; then
  exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
else
  exec python manage.py runserver 0.0.0.0:8000
fi
