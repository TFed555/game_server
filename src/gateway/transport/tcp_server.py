import asyncio
import logging
from datetime import datetime
from gateway.transport.protocol import Protocol
from gateway.routing.router import Router
from proto.packet_pb2 import ClientMessage, ServerMessage
from gateway.models.connection import Connection
from gateway.contexts.clientcontext import ClientContext
from gateway.managers.connectionmanager import ConnectionManager
from gateway.managers.heartbeatmanager import HeartbeatManager
import uuid

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TCP_Server:
    def __init__(self, host='localhost', port=5050):
        self.__host = host
        self.__port = port
        # self.__header = header
        # self.__format = 'utf-8'
        self.__lock = asyncio.Lock()
        self.protocol = Protocol(incoming_msg=ClientMessage, outgoing_msg=ServerMessage)
        self.router = Router()
        self.connections = ConnectionManager(self.protocol)
        self.heartbeat = HeartbeatManager(self.connections)
        self.heartbeat_task = asyncio.Task


    async def handle_connection(self, conn):
        while True:
            packet = await self.protocol.read_packet(conn.reader)
            if not packet:
                break
            logging.info("Msg received")
            if packet is not None:
                conn.last_act = datetime.now()
                response = await self.router.route(packet, conn)
                if response is not None:
                    await self.protocol.write_packet(conn.writer, response)

    async def open_connection(self, reader, writer):
        client_id = str(uuid.uuid4())
        conn = Connection(id=client_id, 
                          writer=writer, 
                          reader=reader,
                          connected_at=datetime.now(), 
                          last_act=datetime.now(),
                          task=asyncio.current_task())
        self.connections.add(client_id, conn)
        logging.info(f"[CONNECTION] Client {client_id[:5]} connected")
        # ctx = ClientContext(connection_id=client_id,
        #                     last_act=datetime.now())
        try:
            await self.handle_connection(conn)
        except Exception as e:
            logging.error(f"Error occurred with a client {client_id[:5]}: {e}")
        finally:
            await self.close_connection(client_id=client_id, writer=writer)

    async def close_connection(self, client_id, writer):
        self.connections.remove(client_id=client_id)
        writer.close()
        await writer.wait_closed()
        logging.info(f"[CLIENT]{client_id} was disconnected")

    async def start(self):
        server = await asyncio.start_server(
            self.open_connection,
            self.__host,
            self.__port
        )
        logging.info(f"[LISTENING] Server is listening on {self.__host}")
        try:
            self.heartbeat_task = asyncio.create_task(self.heartbeat.run())
        except Exception as e:
            logging.error(f"[HEARTBEAT] Task was dropped with exceptiob {e}")

        async with server:
            await server.serve_forever()