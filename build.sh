#!/usr/bin/env bash
# exit on error
set -o errexit

curl -sSL https://install.python-poetry.org | python3 -

poetry install

python3 manage.py collectstatic --no-input
python3 manage.py migrate

celery -A api worker -l info
celery -A api beat -l info