#!/usr/bin/env bash

set -e
set -u

export DJANGO_SETTINGS_MODULE=ITS_api.settings
export DJANGO_CONFIGURATION=Prod

cd /opt/app
python3 manage.py migrate --noinput        # Apply database migrations
python3 manage.py collectstatic --noinput  # Collect static files
python3 manage.py createdefaultuser   # Create default user admin
python3 manage.py loaddata course.json lessons.json
#python3 manage.py runserver  127.0.0.1:8000


supervisord -c /opt/app/Deploy/supervisor.conf