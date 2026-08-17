from models.connection import Connection
from models.packet_pb2 import ServerMessage

class ConnectionManager:
    def __init__(self, protocol):
        self._connections: dict[str, Connection] = {}
        self.protocol = protocol

    def add(self, client_id:str, conn:Connection):
        self._connections[client_id] = conn

    def remove(self, client_id:str):
        self._connections.pop(client_id, None)

    def get(self, client_id:str):
        return self._connections.get(client_id)

    def get_all(self):
        return self._connections.values()

    async def send(self, client_id:str, msg:ServerMessage):
        conn = self.get(client_id)
        if conn is None:
            return
        await self.protocol.write_packet(conn.writer, msg)

    async def broadcast(self, msg:ServerMessage):
        for conn in self._connections.values():
            await self.protocol.write_packet(conn.writer, msg)

    async def force_disconnect(self, client_id:str):
        conn = self.get(client_id)
        if conn is None:
            return
        conn.task.cancel()