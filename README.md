# test-celery-with-priority


## Setup

```sh
$ git clone https://github.com/sisobus/test-celery-with-priority
$ cd test-celery-with-priority
$ docker-compose up -d --build
```

## Test

```sh
$ (new terminal to check container logs) docker logs -f test-celery-with-priority
$ docker exec -it test-celery-with-priority python client.py
```

## Important

- Priority: A number between 0 and 255, where 255 is the highest priority.
- Supported by: RabbitMQ, **Redis (Priority reversed, 0 is highest)**
