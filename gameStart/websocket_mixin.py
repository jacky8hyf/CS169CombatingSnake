from djwebsockets.decorator import Namespace
from djwebsockets.mixins.wsgi import WSGIMixin


@Namespace("/ws")
class WebSocketMixin:
    rooms = {}

    @classmethod
    def on_connect(cls, socket, path):
        room = cls.get_room(path)
        room.append(socket)
        msg = "{} has joined room".format(str(socket.user))
        cls.publish(room, msg)

    @classmethod
    def on_message(cls, socket, message):
        room = cls.get_room(socket.path)
        msg = str(socket.user)+" : "+message
        cls.publish(room, msg)

    @classmethod
    def on_close(cls, socket):
        room = cls.get_room(socket.path)
        msg = "{} has left the room".format(str(socket.user))
        room.remove(socket)
        cls.publish(room, msg)

    @classmethod
    def get_room(cls, path):
        if path not in cls.rooms:
            cls.rooms[path] = []
        room = cls.rooms[path]
        return room

    @staticmethod
    def publish(room, message):
        for socket in room:
            socket.send(message)


@Namespace("/echo")
class EchoHandler:
    @classmethod
    def on_connect(cls, socket, path):
        print(socket.socket.__dict__)
        socket.send("Welcome")
    @classmethod
    def on_message(cls, socket, message):
        socket.send(message)
    @classmethod
    def on_close(cls, socket):
        socket.send("Bye")