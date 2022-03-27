FROM alpine

# ===== INSTALL DEPENDENCIES =====
RUN \
    # update the list of packages to get curl
    apk update \
    # add poetry, scrapy dependencies
    && apk add --no-cache \
        curl \
        gcc \
        libc-dev \
        musl-dev \
        libffi-dev \
        zlib-dev \
        make \
        patch \
        readline-dev \
        openssl-dev \
        bzip2-dev \
        python3 \
        python3-dev \
        py3-pip \
        libxml2-dev \
        libxslt-dev \
        rust \
        cargo \
        g++ 


# ===== CREATE A NON-ROOT USER =====
# create directory for a new user
RUN mkdir -p /home/nonroot
# create the non-root user to run container processes
RUN addgroup -S nonroot && adduser -S -G nonroot nonroot
ENV HOME=/home/nonroot/

# ===== INSTALL AND CONFIGURE poetry FOR PACKAGE MANAGEMENT =====
# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# add poetry to path
ENV PATH "$HOME/.local/bin:$PATH"
# don't create virtualenvs
RUN poetry config virtualenvs.create false
# don't write .pyc to disk
ENV PYTHONDONTWRITEBYTECODE 1
# don't buffer stdout
ENV PYTHONUNBUFFERED 1

# ===== COPY THE APPLICATION FILES =====
ENV APP_DIR=/home/nonroot/ghubscraper/
RUN mkdir $APP_DIR
WORKDIR $APP_DIR
COPY pyproject.toml $APP_DIR
RUN poetry install
COPY ./scraper $APP_DIR/scraper
COPY scrapy.cfg $APP_DIR

# ===== ACCESS CONTAINER AS NON-ROOT ===
# make the nonroot user the owner of the app files
RUN chown -R nonroot:nonroot $APP_DIR
USER nonroot
ENTRYPOINT [ "sh" ]
