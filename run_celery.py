from app import celery
from billiard import freeze_support
if __name__ == '__main__':
    freeze_support()
    argv = [
        'worker',
        '--loglevel=info',
        '--concurrency=1'
    ]
    celery.worker_main(argv)
