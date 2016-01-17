from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jamjar',
        'USER': 'jamjar',
        'PASSWORD': 'jamjar',
        'HOST': 'localhost',
        'PORT': '',
    },
    'lilo': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dejavu',
        'USER': 'jamjar',
        'PASSWORD': 'jamjar',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


JAMJAR_ENV = 'prod' # TODO
