FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY ./requirements/base.txt /code/
RUN pip install -r base.txt
COPY celerylogger/celery_logger.py /code/
CMD python celery_logger.py
