from .packethandler import PacketHandler
from models.packet_pb2 import ServerMessage
from models.connection import Connection
from gateway.contexts.clientcontext import ClientContext

FORMAT = 'utf-8'
class EchoHandler(PacketHandler):
    async def handle(self, message, conn: Connection) -> ServerMessage:
        response = ServerMessage()
        response.echo.message = f"Received {message} from client {conn.id}"
        return response