from .base import *

SECRET_KEY = '5atsi=ps6i$&!ym5&$z!nx8yx7s_ei!kjmsl41e+pnbsd3@mg+'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'nestingpolska.usermd.net']


DATABASES ={

'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': BASE_DIR / 'sqlite3.db',                      # Or path to database file if using sqlite3.
        }
}


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

