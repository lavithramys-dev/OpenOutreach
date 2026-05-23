#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --no-input
python manage.py setup_crm

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput || echo "Superuser already exists."
fi

# We check an environment variable to decide whether to run the web server or the daemon
if [ "$RUN_DAEMON" = "true" ]; then
    echo "Starting automation daemon..."
    # Make sure xvfb and vnc are running if needed by the entrypoint
    exec ./compose/linkedin/start
else
    echo "Starting web server..."
    exec python manage.py runserver 0.0.0.0:$PORT
fi
