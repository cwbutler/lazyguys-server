#!/bin/bash

python3 app/manage.py migrate --no-input

if [ "DJANGO_DEBUG" == "False" ]
then
  python3 app/manage.py collectstatic --no-input
  gunicorn lazyguys.wsgi --bind 0.0.0.0:${PORT} --preload --max-requests 1200 --chdir ./app -w 2
else
  python3 app/manage.py runserver 0.0.0.0:${PORT}
fi

exec "$@"
