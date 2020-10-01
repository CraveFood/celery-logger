# Celery Logger

celery-logger is a python library for logging [celery](https://docs.celeryproject.org/en/stable/) events such as tasks received, tasks failed/succeeded and tasks retried, along with task args.

## Features

- Simple and flexible task logs
- Multiple deployment options (docker, virtual machines)
- Integration possibilities: ELK stack and AWS cloudwatch for example

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

<!-- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install celery-logger.

```bash
pip install celerylogger
``` -->

## Usage

<!-- TODO -->

## Contributing

<!-- TODO -->

## License

<!-- TODO -->
