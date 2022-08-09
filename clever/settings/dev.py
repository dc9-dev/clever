from .base import *

SECRET_KEY = '$env:SECRET_KEY'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'nestingpolska.usermd.net']


# DATABASES ={

# 'default': {
#         'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': BASE_DIR / 'sqlite3.db',                      # Or path to database file if using sqlite3.
#         }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'clever',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

