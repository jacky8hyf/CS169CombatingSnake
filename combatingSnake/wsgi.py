"""
WSGI config for combatingSnake project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

# import os
from dj_static import Cling
# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "combatingSnake.settings")

# application = Cling(get_wsgi_application())

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "combatingSnake.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from snake_websocket_server import SnakeWebSocketServer

_django_app = Cling(get_wsgi_application())
_websocket_app = SnakeWebSocketServer()

def application(environ, start_response):
    if environ.get('PATH_INFO').startswith(settings.WEBSOCKET_URL):
        return _websocket_app(environ, start_response)
    return _django_app(environ, start_response)