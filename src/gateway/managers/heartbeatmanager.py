from gateway.managers.connectionmanager import ConnectionManager
from proto.packet_pb2 import ServerMessage
import asyncio
from datetime import datetime
import logging

class HeartbeatManager:
    def __init__(self, connections: ConnectionManager):
        self._connections = connections
        self._interval = 15
        self._timeout = self._interval*2

    def ping_message(self):
        packet = ServerMessage()
        packet.ping.SetInParent()
        return packet

    async def run(self):
        while True:
            await asyncio.sleep(self._interval)
            now = datetime.now()
            for conn in self._connections.get_all():
                sub = (now - conn.last_act).total_seconds()
                if sub > self._timeout:
                    logging.info(f"[HEARTBEAT] Client {conn.id} is not answering, disconnecting")
                    await self._connections.force_disconnect(conn.id)
                elif sub > self._interval:
                    await self._connections.send(conn.id, self.ping_message())