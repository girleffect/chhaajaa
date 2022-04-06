#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput 

if [ -n "$DOMAIN" ]; then
    sed -i "s/{{DOMAIN}}/${DOMAIN}/" /etc/nginx/conf.d/django.conf
else
    sed -i "s/{{DOMAIN}}/_/" /etc/nginx/conf.d/django.conf
fi

nginx -g 'daemon off;' &
gosu wagtail gunicorn chajaa.wsgi:application --config /etc/gunicorn/config.py --timeout 1800
