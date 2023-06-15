#!/bin/bash

. $VENV_PATH/bin/activate

poetry run python manage.py migrate

poetry run python manage.py collectstatic --noinput --clear

exec "$@"
