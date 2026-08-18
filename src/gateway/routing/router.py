from gateway.handlers.echohandler import EchoHandler
from gateway.handlers.connectionhandler import ConnectionHandler
from gateway.handlers.loginhandler import LoginHandler
from proto.packet_pb2 import ClientMessage
from gateway.contexts.clientcontext import ClientContext
from gateway.models.connection import Connection

class Router:
    def __init__(self):
        self.handlers = {
            "echo": EchoHandler(),
            "pong": ConnectionHandler(),
            "login": LoginHandler()
        }
    async def route(self, msg: ClientMessage, conn: Connection):
        try:
            kind = msg.WhichOneof("payload")
            if kind is None:
                raise ValueError
            handler = self.handlers.get(kind)
            if handler is None:
                raise KeyError
            payload = getattr(msg, kind)
            result = await handler.handle(payload, conn)
            return result
        except (ValueError, KeyError):
            return None
