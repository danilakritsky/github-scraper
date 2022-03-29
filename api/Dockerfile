FROM python:3.10-alpine

RUN \
    apk update \
    && apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/
ENV APP_DIR=/home/api
WORKDIR $APP_DIR

COPY api $APP_DIR/api/
COPY manage.py requirements.txt $APP_DIR/
COPY ghubscraper $APP_DIR/ghubscraper

RUN \
    python -m pip install -r requirements.txt && \
    python manage.py makemigrations