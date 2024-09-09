#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

# DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

# wsgi server
# gunicorn obsfeare_server.wsgi:application --bind 0.0.0.0:8000

# asgi server
daphne -b 0.0.0.0 -p 8000 obsfeare_server.asgi:application
