from gateway.handlers.echohandler import EchoHandler
from models.packet import Packet, PacketType
from gateway.contexts.clientcontext import ClientContext
from parsers.echoparser import EchoParser

class Router:
    def __init__(self):
        self.routes = {
            PacketType.PING: (EchoParser(), EchoHandler()),
        }
    async def route(self, packet: Packet, ctx: ClientContext) -> Packet | None:
        try:
            parser, handler = self.routes[packet.type]
            message = parser.decode(packet.payload)
            result = await handler.handle(message, ctx)
            if result is None:
                return None
            response_type, response = parser.encode(result)
            return Packet(response_type, response)
        except KeyError:
            return
