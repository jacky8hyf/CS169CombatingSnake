import re
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer, uWSGIWebsocket

class EchoWebSocket(uWSGIWebsocket):
    def receive(self, *args, **kwargs):
        msg = uWSGIWebsocket.receive(self, *args, **kwargs)
        uWSGIWebsocket.send(self,msg)
        return msg
class SnakeWebSocketServer(uWSGIWebsocketServer):

    routes = {
        '/ws/echo(/|)': EchoWebSocket
    }

    def upgrade_websocket(self, environ, start_response):
        uWSGIWebsocketServer.upgrade_websocket(self, environ, start_response)
        path = environ.get('REQUEST_URI')
        for pattern, func in self.routes.items():
            if re.match(pattern, path):
                return func()
        return uWSGIWebsocket()