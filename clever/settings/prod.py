from .base import *
import os

SECRET_KEY = "$1zynwgl$r$61-gqv1)!j=&jy^&dt4fx&sn5++eo%82rktlton"
DEBUG = False
ALLOWED_HOSTS = ['nestingpolska.usermd.net', '127.0.0.1']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'p1472_nesting',
        'USER': 'p1472_nesting',
        'PASSWORD': 'Cleverspace2022',
        'HOST': 'pgsql52.mydevil.net',
        'PORT': '5432',
    }
}

