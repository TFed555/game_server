from .packethandler import PacketHandler
import asyncio

class ConnectionHandler(PacketHandler):
    async def handle(self, packet, ctx):
        ctx.last_pong = asyncio.get_running_loop().time()
        return