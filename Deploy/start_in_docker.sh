#!/usr/bin/env bash

set -e
set -u

export DJANGO_SETTINGS_MODULE=ITS_api.settings
export DJANGO_CONFIGURATION=Prod

cd /opt/app
python3 manage.py migrate --noinput        # Apply database migrations
python3 manage.py collectstatic --noinput  # Collect static files
python3 manage.py createdefaultuser   # Create default user admin
mkdir -p media/products && cp -rf fixtures/products media
python3 manage.py loaddata fixtures/category.json

supervisord -c /opt/app/Deploy/supervisor.conf