from base import *

# We want debugging on here
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wlh!-90ty3!dk5i1vi_gbsi7((jg+@j%k=&cel2$jrod&6^n(y'

# Paths
VIDEOS_PATH = '/opt/code/masonjar/videos'

# URLS
API_BASE_URL = 'http://api.localhost.dev:5001'
SITE_BASE_URL = 'http://dashboard.localhost.dev:5000/#'

# Host origins allowed to access the API
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
CORS_ORIGIN_WHITELIST = (
        'dashboard.localhost.dev:5000',
        'dashboard.localhost.dev',
        '52.2.193.201:5000'
)

ALLOWED_HOSTS = [
    '.localhost.dev',
    'localhost'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jamjar',
        'USER': 'jamjar',
        'PASSWORD': 'VolkolosIsMyBoi!!',
        'HOST': 'jamjar.cxdklgrw0tga.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}
