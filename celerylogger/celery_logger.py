#!/usr/bin/env python

import argparse
import logging
import logging.config
import os
import signal
import sys
from functools import lru_cache

from celery import Celery

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "basic": {"format": "%(asctime)s - %(message)s"},
    },
    "handlers": {
        "stdout": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "basic",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "formatter": "basic",
            "filename": "/tmp/logger.txt",
        },
    },
    "loggers": {
        "celery_logger": {"handlers": ["stdout"], "propagate": False, "level": "INFO"},
    },
}


def setup_exit_signals():
    exit_gracefully = lambda *args: sys.exit(0)  # noqa E371
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)


@lru_cache(maxsize=None)
def get_logger(event_type):
    logger_name = f"celery_logger.{event_type}"
    return logging.getLogger(logger_name)


def celery_task_logger(app):
    state = app.events.State()

    def log_event(event):
        state.event(event)
        task = state.tasks.get(event["uuid"])

        msg_args = event
        msg_args.update({"name": task.name})
        msg = "{type} {name} {uuid} {hostname} {timestamp}".format(**msg_args)
        msg += f" * Raw event: {event}"
        logger = get_logger(event.get("type"))
        logger.info(msg)

    with app.connection() as connection:
        recv = app.events.Receiver(
            connection,
            handlers={
                "task-sent": log_event,
                "task-received": log_event,
                "task-started": log_event,
                "task-succeeded": log_event,
                "task-failed": log_event,
                "task-rejected": log_event,
                "task-revoked": log_event,
                "task-retried": log_event,
            },
        )
        recv.capture(limit=None, timeout=None, wakeup=True)


def setup_logging(log_file):
    base_logger = LOGGING_CONFIG["loggers"]["celery_logger"]
    file_handler = LOGGING_CONFIG["handlers"]["file"]

    if log_file:
        base_logger.update({"handlers": ["file"]})
        file_handler.update({"filename": log_file})

    logging.config.dictConfig(LOGGING_CONFIG)


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor and log Celery tasks")

    parser.add_argument(
        "--celery-broker",
        help="Celery broken URI. Defaults to environment var $CELERY_LOGGER_BROKER.",
        default=os.getenv("CELERY_LOGGER_BROKER"),
    )
    parser.add_argument(
        "--log-file",
        help=(
            "Path to log file. If not set logs will be sent to stdout. "
            "Defaults to environment var $CELERY_LOGGER_LOG_FILE."
        ),
        default=os.getenv("CELERY_LOGGER_LOG_FILE"),
    )
    return parser.parse_args()


def main():
    setup_exit_signals()

    args = parse_args()
    if not args.celery_broker:
        raise ValueError("Argument --celery-broker is required")

    setup_logging(args.log_file)

    app = Celery(broker=args.celery_broker)
    celery_task_logger(app)


if __name__ == "__main__":
    main()
