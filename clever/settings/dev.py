from .base import *

SECRET_KEY = '$1zynwgl$r$61-gqv1)!j=&jy^&dt4fx&sn5++eo%82rktlton'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


DATABASES ={
'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': BASE_DIR / 'sqlite3.db',                      # Or path to database file if using sqlite3.
        
}
}