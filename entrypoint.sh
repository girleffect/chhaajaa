#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput 
nginx -g 'daemon off;' &
gosu wagtail gunicorn chajaa.wsgi:application --config /etc/gunicorn/config.py --timeout 1800