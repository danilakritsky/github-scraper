FROM python:3.10-alpine

RUN \
    apk update
    # && apk add --no-cache \
    #     gcc \
    #     musl-dev \
    #     libffi-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/
ENV HOME=/home/api
WORKDIR $HOME

COPY api $HOME/api/
COPY manage.py requirements.txt $HOME/
COPY ghubscraper $HOME/ghubscraper

RUN \
    python -m pip install -r requirements.txt && \
    python manage.py makemigrations