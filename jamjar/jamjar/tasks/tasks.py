from celery import Celery
from django.conf import settings

#app = Celery('tasks', backend=settings.REDIS_QUEUE, broker=settings.REDIS_QUEUE)
app = Celery('tasks', backend='redis://localhost:6379/0', broker='redis://localhost:6379/0', include=['tasks'])
