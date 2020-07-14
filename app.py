import os
import time
import random
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import abort
import redis
from celery import Celery
from celery.concurrency import asynpool
from celery.signals import worker_process_init, worker_process_shutdown
from pathlib import Path


def init():
    global app, celery, redis_conn

    app = Sanic(__name__)
    settings = {
        'REQUEST_TIMEOUT': 3600,
        **os.environ,
        'CELERY_TASK_SERIALIZER': 'pickle',
        'CELERY_ACCEPT_CONTENT': ['json', 'pickle'],
        'C_FORCE_ROOT': '1',
    }
    app.config.update(settings)
    celery = Celery('app', backend='redis://redis:6379',
                    broker='redis://redis:6379')
    celery.conf.update(app.config)
    asynpool.PROC_ALIVE_TIMEOUT = 2000
    redis_conn = redis.StrictRedis(
        host='redis',
        port=6379,
        db=1
    )


init()


@worker_process_init.connect()
def on_worker_init(**_):
    global redis_conn
    print('== model load ==')
    redis_conn.set('ModelLoaded', 'success')
    print('== model loaded ==')


@worker_process_shutdown.connect()
def on_worker_shutdown(**_):
    global redis_conn
    redis_conn.delete('ModelLoaded')


@celery.task(serializer='pickle')
def long_task_over_5seconds():
    time.sleep(5 + random.random() * 5)
    print('long done')
    return {}


@celery.task(serializer='pickle')
def short_task_under_2seconds():
    time.sleep(1 + random.random())
    print('short done')
    return {}


@app.get('/long')
async def long(request):
    long_task_over_5seconds.apply_async(priority=9)
    return json({'message': 'long_task_over_5seconds go'})


@app.get('/short')
async def short(request):
    short_task_under_2seconds.apply_async(priority=0)
    return json({'message': 'short_task_under_2seconds go'})


if __name__ == '__main__':
    app.go_fast(host='0.0.0.0',
                port=5000, debug=1, workers=4)
