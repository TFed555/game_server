from .packethandler import PacketHandler
from datetime import datetime

class ConnectionHandler(PacketHandler):
    async def handle(self, msg, conn):
        conn.last_act = datetime.now()
        return