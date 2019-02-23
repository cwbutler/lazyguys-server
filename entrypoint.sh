#!/bin/bash

python3 manage.py collectstatic --no-input
python3 manage.py migrate --no-input
gunicorn lazyguys.wsgi -b 0.0.0.0:${PORT} --preload --max-requests 1200

exec "$@"
