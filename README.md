# Celery Logger

celery-logger is a python library for logging [celery](https://docs.celeryproject.org/en/stable/) events such as tasks received, tasks failed/succeeded and tasks retried, along with task args.

## Features

- Simple and flexible task logs
- Multiple deployment options (docker, virtual machines)
- Integration possibilities: ELK stack and AWS cloudwatch for example

## How does it work?

Celery-logger connects with your message broker (such as redis, rabbitMQ or SQS) and logs the tasks on a file or stdout.

This way you can easily have multiple celery workers and see your logs in a single place.

![Celery Logger Diagram](https://user-images.githubusercontent.com/9268203/128907058-e4306c14-6014-49c6-b265-2a794d2a3ce0.png)
## Sample project

We provided a sample project for playing around and seeing how it works. 

### Getting started:

```
# navigate to the sample-project folder
$ cd sample-project
# Build and start the containers:
$ docker-compose up
```

### Querying logs

Make sure you are in the sample-project folder 

#### Calling a few tasks 

```
$ docker-compose exec celeryd python call_tasks.py

Tasks have been called!
Run `docker-compose logs -f celery-logger` to see the logger in action.
```

#### Taking a look in all events


```
$ docker-compose logs celery-logger 
```

#### Searching for failed tasks:

```
$ docker-compose logs celery-logger | grep task-failed
```

#### Searching for a specific task:

```
$ docker-compose logs celery-logger | grep "app.add"
```

#### Searching for a specific task and args:

```
$ docker-compose logs celery-logger | grep "app.add" | grep "(6, 1)"
```

![image](https://user-images.githubusercontent.com/9268203/94805158-4de00d80-03c2-11eb-8a7d-cc37b05e84f3.png)

#### Searching for a task id

```
$   docker-compose logs celery-logger | grep 20925a8c-03f7-4bd7-b3dd-24e2bc9e26e2
```

![image](https://user-images.githubusercontent.com/9268203/94805193-5a646600-03c2-11eb-9f4e-0e96490a78f0.png)

## Installation

Use the package manager [pip](https://pypi.org/project/celery-logger/) to install celery-logger.

```bash
pip install celerylogger
```

## Usage

The executable will be available in the path as `celery-logger`:

```bash
# Display the help text
$ celery-logger -h
# Start logging from a redis broker
$ celery-logger --celery-broker redis://redis:6379/0
```


## Authors


-  **Sergio Oliveira** - *Initial work* - [Seocam](https://github.com/seocam)
-  **Thiago Ferreira** - *Improvements, documentation and current maintainer* - [thiagoferreiraw](https://github.com/thiagoferreiraw)
-  **André Girol** - *Packaging and distribution* - [Girol](https://github.com/girol)

