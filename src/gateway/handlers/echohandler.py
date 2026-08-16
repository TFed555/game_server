from .packethandler import PacketHandler
from models.packet_pb2 import ServerMessage
from gateway.contexts.clientcontext import ClientContext

FORMAT = 'utf-8'
class EchoHandler(PacketHandler):
    async def handle(self, message, ctx: ClientContext) -> ServerMessage:
        response = ServerMessage()
        response.echo.message = f"Received {message} from client {ctx.client_id}"
        return response