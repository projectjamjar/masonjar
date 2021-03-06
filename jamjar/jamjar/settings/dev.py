from base import *

# We want debugging on here
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wlh!-90ty3!dk5i1vi_gbsi7((jg+@j%k=&cel2$jrod&6^n(y'

# Paths
TMP_VIDEOS_PATH = '/opt/code/masonjar/videos'

# URLS
API_BASE_URL = 'http://api.localhost.dev:5001'
SITE_BASE_URL = 'http://dashboard.localhost.dev:5000/#'

S3_URL = 'https://s3.amazonaws.com/jamjar-videos/dev/{}/{}.{}'

# GMaps API Key
GMAPS_API_KEY = 'AIzaSyB3ay9JpvAc9SLQKkkuJpYKqCCAH0cVUk0'
GMAPS_CACHE_BUST = 5 # Update GMapLocations after 5 days of staleness

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Host origins allowed to access the API
CORS_ORIGIN_WHITELIST = (
        'localhost',
        'localhost:5000',
        'dashboard.localhost.dev:5000',
        'dashboard.localhost.dev',
        '52.2.193.201:5000'
)

ALLOWED_HOSTS = [
    '.localhost.dev',
    'localhost'
]

# Add silk to the apps and stuff
INSTALLED_APPS += [
    'silk',
]

MIDDLEWARE_CLASSES = [
    'silk.middleware.SilkyMiddleware',
] + MIDDLEWARE_CLASSES

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
        'db': 'dejavu',
        'user': 'jamjar',
        'passwd': 'jamjar',
        'host': 'localhost'
    },
    'multiple_match': True
}
