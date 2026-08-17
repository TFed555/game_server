from .packethandler import PacketHandler
from datetime import datetime
import asyncio

class ConnectionHandler(PacketHandler):
    async def handle(self, msg, conn):
        conn.last_act = datetime.now()
        return