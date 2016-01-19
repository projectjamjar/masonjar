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

LILO_CONFIG = {
    'database': {
        'db': 'dejavu_test',
        'user': 'jamjar',
        'passwd': 'jamjar',
        'host': 'localhost'
    },
    'multiple_match': True
}

JAMJAR_ENV = 'test'
