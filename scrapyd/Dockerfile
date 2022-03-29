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
RUN touch docker_entrypoint.sh
RUN chmod +x docker_entrypoint.sh
RUN echo "scrapyd &" >> docker_entrypoint.sh
RUN echo "logparser -dir logs &" >> docker_entrypoint.sh
ENTRYPOINT [ "sh" ]

