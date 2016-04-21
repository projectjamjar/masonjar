from base import *
import os

SECRET_KEY = 's0rryH@xx0r$'

TMP_VIDEOS_PATH = os.path.expanduser('~/videos')
if not os.path.exists(TMP_VIDEOS_PATH):
    os.makedirs(TMP_VIDEOS_PATH)

# URLS
API_BASE_URL = 'http://api.localhost.dev:5001'
SITE_BASE_URL = 'http://dashboard.localhost.dev:5000/#'

S3_URL = 'https://s3.amazonaws.com/jamjar-videos/dev/{}/{}.{}'

# GMaps API Key
GMAPS_API_KEY = 'AIzaSyB3ay9JpvAc9SLQKkkuJpYKqCCAH0cVUk0'
GMAPS_CACHE_BUST = 5 # Update GMapLocations after 5 days of staleness

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jamjar',
        'USER': 'jamjar',
        'PASSWORD': 'jamjar',
        'HOST': 'localhost',
        'PORT': '',
        'AUTOCOMMIT': False
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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'jamjar': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
