import random

from celery import Celery
from requests import get

app = Celery("app", broker="redis://redis:6379/0")


@app.task
def add(x, y):
    return x + y


@app.task
def call_external_api():
    """
    Send a get request to httpbin.org.

    The api call will fail randomly to ilustrate how the logs will be stored.
    """
    possible_status_codes = [200, 400, 500]
    request_status = random.choice(possible_status_codes)

    response = get(f"https://httpbin.org/status/{request_status}")

    # Raises an exception if the response code is not successfull
    response.raise_for_status()

    return "The status code was: " + str(response.status_code)
