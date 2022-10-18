#!/bin/bash
if [ -n "$RUN_COLLECTSTATIC" ]; then
    python manage.py collectstatic --noinput
fi
if [ -n "$RUN_MIGRATIONS" ]; then
    python manage.py makemigrations && python manage.py migrate --noinput
fi

if grep "{{DOMAIN}}" /etc/nginx/conf.d/django.conf; then
    if [ -n "$DOMAIN" ]; then
        sed -i "s/{{DOMAIN}}/${DOMAIN}/" /etc/nginx/conf.d/django.conf

        target="https://${DOMAIN}\$request_uri"
        tee -a /etc/nginx/conf.d/django.conf <<EOF
server {
    listen 8000 default_server;
    server_name _;
    return 301 "${target}";
}
EOF
    else
        sed -i "s/{{DOMAIN}}/_/" /etc/nginx/conf.d/django.conf
    fi
fi

nginx -g 'daemon off;' &
gosu wagtail gunicorn chajaa.wsgi:application --config /etc/gunicorn/config.py --timeout 1800
