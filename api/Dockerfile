FROM python:3.10-alpine

RUN \
    apk update
    # && apk add --no-cache \
    #     gcc \
    #     musl-dev \
    #     libffi-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/api/
ENV HOME=/home/api/
WORKDIR $HOME

COPY requirements.txt $HOME
RUN pip install -r requirements.txt
COPY api ghubscraper manage.py $HOME

RUN \
    python manage.py makemigrations && \
    python manage.py migrate