#!/usr/bin/env python

import argparse
import logging
import os
from functools import lru_cache

from celery import Celery


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


def configure_logging(log_file):
    logger = logging.getLogger("celery_logger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(message)s")

    if log_file:
        handler = logging.handlers.WatchedFileHandler(log_file)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    logger.addHandler(handler)


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
            "Path to log file. If not set logs will be sent to stdout."
            "Defaults to environment var $CELERY_LOGGER_LOG_FILE."
        ),
        default=os.getenv("CELERY_LOGGER_LOG_FILE"),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.celery_broker:
        raise ValueError("Argument --celery-broker is required")
    configure_logging(args.log_file)
    app = Celery(broker=args.celery_broker)
    celery_task_logger(app)


if __name__ == "__main__":
    main()
