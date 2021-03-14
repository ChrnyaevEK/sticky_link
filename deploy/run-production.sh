uwsgi --ini /var/www/sticky_link/deploy/production.ini
/var/www/sticky_link/venv/bin/daphne -b 0.0.0.0 -p 9001 sticky_link.asgi:application