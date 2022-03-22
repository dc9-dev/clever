import os
import sys
from urllib.parse import unquote

from django.core.wsgi import get_wsgi_application

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = "clever.settings.prod" 
def application(environ, start_response):
    environ["PATH_INFO"] = unquote(environ["PATH_INFO"]).encode('iso-8859-1').decode('utf-8')
    _application = get_wsgi_application()
    return _application(environ, start_response)