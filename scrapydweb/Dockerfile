FROM python:3.10-alpine

RUN \
    apk update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/scrapydweb/
ENV APP_DIR=/home/scrapydweb/
WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR
COPY scrapydweb_settings_v10.py $APP_DIR
RUN python -m pip install -r requirements.txt

