#!/bin/bash

python3 app/manage.py collectstatic --no-input
python3 app/manage.py migrate --no-input
gunicorn lazyguys.wsgi --bind 0.0.0.0:${PORT} --preload --max-requests 1200 --chdir ./app -w 2

exec "$@"
