from gateway.handlers.echohandler import EchoHandler
from gateway.handlers.connectionhandler import ConnectionHandler
from models.packet_pb2 import ClientMessage
from gateway.contexts.clientcontext import ClientContext

class Router:
    def __init__(self):
        self.handlers = {
            "echo": EchoHandler(),
            "connection": ConnectionHandler()
        }
    async def route(self, msg: ClientMessage, ctx: ClientContext):
        try:
            kind = msg.WhichOneof("payload")
            if kind == "pong":
                handler = self.handlers.get("connection")
            else:
                handler = self.handlers.get(kind)
            if handler is None:
                return None
            payload = getattr(msg, kind)
            result = await handler.handle(payload, ctx)
            return result
        except KeyError:
            return None
