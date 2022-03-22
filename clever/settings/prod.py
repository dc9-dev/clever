from .base import *
import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = ['system.nesting.pl']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'p1472_nesting',
        'USER': 'p1472_nesting',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': 'pgsql52.mydevil.net',
        'PORT': '5432',
    },
}


STATIC_ROOT = '/home/Nestingpolska/domains/nesting.pl/public_python/public/static/'
MEDIA_ROOT = '/home/Nestingpolska/domains/nesting.pl/public_python/public/media/'