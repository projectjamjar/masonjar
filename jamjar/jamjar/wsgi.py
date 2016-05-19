"""
WSGI config for jamjar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

jamjar_env = os.environ.get('JAMJAR_ENV', None)

if jamjar_env in ['prod', 'dev']:
  settings_module = "jamjar.settings.{}".format(jamjar_env)
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
else:
    raise RuntimeError("No acceptable JAMJAR_ENV specified! Given: {}".format(jamjar_env))


application = get_wsgi_application()
