"""
WSGI config for combatingSnake project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

"""
For Websockets, we start uWsgi. For more information visit:
http://django-websocket-redis.readthedocs.org/en/latest/running.html
To test, run with:
uwsgi --http 0.0.0.0:8080 --gevent 100 --http-websockets --module wsgi
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "combatingSnake.settings")
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer

_django_app = get_wsgi_application()
_websocket_app = uWSGIWebsocketServer()

def application(environ, start_response):
    if environ.get('PATH_INFO').startswith(settings.WEBSOCKET_URL):
        return _websocket_app(environ, start_response)
    return _django_app(environ, start_response)
