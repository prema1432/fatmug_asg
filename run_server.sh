#!/bin/bash

# Define environment file path
env_file=".env"

if [ ! -f "$env_file" ]; then
    echo "Creating $env_file"
    touch "$env_file"
    if [ "$ENVIRONMENT" = "local" ] || [ -z "$ENVIRONMENT" ]; then
      echo "# Environment" >> "$env_file"
      echo "ENVIRONMENT=local" >> "$env_file"
      echo "" >> "$env_file"
      echo "# Django settings" >> "$env_file"
      echo "DJANGO_SECRET_KEY=ArkKuN2zTeUV9xb_rZyWjrNwyrDatZzVzwT-n0WY6gSKPQLvLe5W3yD4LIxIrP8f0jM" >> "$env_file"
      echo "DEBUG=True" >> "$env_file"
      echo "" >> "$env_file"
      echo "# Database configuration" >> "$env_file"
      echo "POSTGRES_DB=fastmug_db" >> "$env_file"
      echo "POSTGRES_USER=user" >> "$env_file"
      echo "POSTGRES_PASSWORD=password" >> "$env_file"
      echo "DATABASE_HOST=pgdatabase" >> "$env_file"
      echo "DATABASE_PORT=5432" >> "$env_file"
      echo "" >> "$env_file"
      echo "# Redis configuration" >> "$env_file"
      echo "REDIS_URL=redis://redis:6379/0" >> "$env_file"
      echo "" >> "$env_file"

    elif [ "$ENVIRONMENT" = "production" ] || [ "$ENVIRONMENT" = "test" ]; then
      echo "# Environment" >> "$env_file"
      echo "ENVIRONMENT=test" >> "$env_file"
      echo "" >> "$env_file"
      echo "# Django settings" >> "$env_file"
      echo "DJANGO_SECRET_KEY=ArkKuN2zTeUV9xb_rZyWjrNwyrDatZzVzwT-n0WY6gSKPQLvLe5W3yD4LIxIrP8f0jM" >> "$env_file"
      echo "DEBUG=False" >> "$env_file"
      echo "" >> "$env_file"
      echo "# Database configuration" >> "$env_file"
      echo "POSTGRES_DB=" >> "$env_file"
      echo "POSTGRES_USER=" >> "$env_file"
      echo "POSTGRES_PASSWORD=" >> "$env_file"
      echo "DATABASE_HOST=" >> "$env_file"
      echo "DATABASE_PORT=" >> "$env_file"
      echo "" >> "$env_file"
      echo "# Redis configuration" >> "$env_file"
      echo "REDIS_URL=" >> "$env_file"
      echo "" >> "$env_file"
    fi
else
    echo "$env_file already exists."
fi


# Run Django commands
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
#python manage.py runserver
gunicorn fatmug_video_processing.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --workers 3
