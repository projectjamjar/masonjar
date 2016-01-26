from celery import Celery
from django.conf import settings

import os

jamjar_env = os.environ.get('JAMJAR_ENV', None)

if jamjar_env is None:
  raise RuntimeError("No JAMJAR_ENV variable given!")
settings_module = "jamjar.settings.{}".format(jamjar_env)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery('tasks', backend=settings.REDIS_QUEUE, broker=settings.REDIS_QUEUE, include=['jamjar.tasks'])
