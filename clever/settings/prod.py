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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail52.mydevil.net'
EMAIL_PORT = 465
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'biuro@nestingpolska.usermd.net'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']