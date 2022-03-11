from .base import *
import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = ['nestingpolska.usermd.net']


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


