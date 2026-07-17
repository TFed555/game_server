import asyncio
import logging
from datetime import datetime
from gateway.transport.protocol import Protocol
from gateway.routing.router import Router
from models.client import Client
from gateway.contexts.clientcontext import ClientContext
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
        self.protocol = Protocol()
        self.router = Router()
        self.clients = {}

    async def open_connection(self, reader, writer):
        client_id = str(uuid.uuid4())
        self.clients[client_id] = Client(
                            id=client_id,
                            writer=writer,
                            pending_request=None,
                            chatter_id=None,
                            connected_at=datetime.now(),
                            msgs_count=0
                        )
        logging.info(f"[CONNECTION] Client {client_id[:5]} connected")
        try:
            while True:
                packet = await self.protocol.read_packet(reader)
                if not packet:
                    break
                logging.info("Msg received")
                if packet is not None:
                    ctx = ClientContext(client_id=client_id)
                    response = await self.router.route(packet, ctx)
                    if response is not None:
                        await self.protocol.write_packet(writer, response)
        except Exception as e:
            logging.error(f"Error occurred with a client {client_id}: {e}")
        finally:
            await self.close_connection(client_id=client_id)

    async def close_connection(self, client_id):
        if client_id in self.clients.keys():
            try:
                self.clients[client_id].writer.close()
                await self.clients[client_id].writer.wait_closed()
            except Exception as e:
                logging.error(f"[CLIENT]{client_id} error with disconnection: {e}")
            del self.clients[client_id]
            logging.info(f"[CLIENT]{client_id} was disconnected")

    async def start(self):
        server = await asyncio.start_server(
            self.open_connection,
            self.__host,
            self.__port
        )
        logging.info(f"[LISTENING] Server is listening on {self.__host}")

        async with server:
            await server.serve_forever()