from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jamjar',
        'USER': 'jamjar',
        'PASSWORD': 'jamjar',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CORS_ORIGIN_WHITELIST = (
        'dashboard.localhost.dev:5000',
        'dev.projectjamjar.com'
)

ALLOWED_HOSTS = [
    '.localhost.dev'
]
