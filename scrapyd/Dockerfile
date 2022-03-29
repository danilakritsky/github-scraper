FROM python:3.10-alpine

RUN \
    apk update \ 
    && apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/scrapyd
ENV HOME=/home/scrapyd/
WORKDIR $HOME

COPY requirements.txt $HOME
RUN pip install -r requirements.txt
COPY scrapyd.conf $HOME