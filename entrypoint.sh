#!/bin/bash

python3 manage.py collectstatic --no-input
python3 manage.py migrate --no-input

if [ -z ${DEBUG+x} ]; \
then gunicorn lazyguys.wsgi -b 0.0.0.0:${PORT} --preload --max-requests 1200; \
else python3 manage.py runserver 0.0.0.0:${PORT}; fi

exec "$@"
