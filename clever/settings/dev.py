from .base import *

SECRET_KEY = '$1zynwgl$r$61-gqv1)!j=&jy^&dt4fx&sn5++eo%82rktlton'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}