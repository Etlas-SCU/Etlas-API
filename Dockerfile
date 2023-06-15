# Base Image for Python 3.11 
FROM python:3.11-slim-buster as build-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Install system dependencies
RUN apt-get update && apt-get install -y \
  curl \
  python3-dev \
  libpq-dev \
  build-essential 

# Install poetry 
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Separate docker stage to avoid re-installing poetry & build essentials on every change
FROM build-base as final-stage

# set work directory
WORKDIR $PYSETUP_PATH

# install dependencies
COPY poetry.lock ./

COPY pyproject.toml ./

RUN poetry install --no-root --only main --sync

# copy project
WORKDIR /home/etlas

COPY ./ ./

# run entrypoint.sh
COPY entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

# run server
CMD uvicorn api.asgi:application --host 0.0.0.0 --port 8000 \
  --app-dir /home/etlas \
  --reload \
  --reload-dir /home/etlas

# expose port
EXPOSE 8000
