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


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail52.mydevil.net'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'biuro@nestingpolska.usermd.net'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']