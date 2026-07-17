from .packethandler import PacketHandler
from gateway.contexts.clientcontext import ClientContext

FORMAT = 'utf-8'
class EchoHandler(PacketHandler):
    async def handle(self, message, ctx: ClientContext) -> str:
        return f"Received {message} from client {ctx.client_id}".encode(FORMAT)