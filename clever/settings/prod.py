from .base import *
import os

SECRET_KEY = "$1zynwgl$r$61-gqv1)!j=&jy^&dt4fx&sn5++eo%82rktlton"
DEBUG = True
ALLOWED_HOSTS = ['nestingpolska.usermd.net']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'p1472_nesting',
        'USER': 'p1472_nesting',
        'PASSWORD': 'Cleverspace2022',
        'HOST': 'pgsql52.mydevil.net',
        'PORT': '5432',
    },
}
