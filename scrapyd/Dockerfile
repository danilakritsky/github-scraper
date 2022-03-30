FROM python:3.10-alpine

RUN \
    apk update \ 
    && apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/scrapyd/
ENV APP_DIR=/home/scrapyd/
WORKDIR $APP_DIR

COPY requirements.txt scrapyd.conf $APP_DIR/
RUN pip install -r requirements.txt


RUN mkdir logs
# ENTRYPOINT [ "sh" ]

