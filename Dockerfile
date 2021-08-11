FROM python:3.7-slim-buster as build-env
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

# Installing `gosu` (https://github.com/tianon/gosu)
RUN set -eux; \
    apt-get update && \
    apt-get install -yq wget gpg && \
    wget https://github.com/tianon/gosu/releases/download/1.13/gosu-amd64 -O gosu && \
    wget https://github.com/tianon/gosu/releases/download/1.13/gosu-amd64.asc -O gosu.asc && \
    gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 && \
    gpg --batch --verify gosu.asc gosu && \
    chmod +x gosu

# Copying package files...
COPY ./requirements/ /usr/src/app/requirements/
COPY ./setup.py /usr/src/app/
COPY ./README.md /usr/src/app/
COPY celerylogger/ /usr/src/app/celerylogger/

# Installing python requirements
RUN pip install .

####################################

FROM gcr.io/distroless/python3

COPY --from=build-env /usr/src/app /usr/src/app
COPY --from=build-env /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
COPY --from=build-env /usr/src/app/gosu /usr/bin/

WORKDIR /usr/src/app

# App variables
ENV PYTHONPATH=/usr/local/lib/python3.7/site-packages
ENV CELERY_LOGGER_BROKER=""
ENV CELERY_LOGGER_LOG_FILE=""

# Running the logger with a non-root user
# Note we don't need to create a human-readable user name, simply using the uid works.
# References: https://github.com/GoogleContainerTools/distroless/issues/306
ENTRYPOINT ["gosu", "888:888", "python", "celerylogger/celery_logger.py"]