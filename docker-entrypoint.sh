#!/bin/sh

echo "Esperando a que la base de datos esté disponible..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Base de datos disponible."

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn bjumper_test.wsgi:application --bind 0.0.0.0:8000