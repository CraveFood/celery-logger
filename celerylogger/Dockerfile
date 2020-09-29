FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY celerylogger/celery_logger.py /code/