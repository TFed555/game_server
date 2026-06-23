import asyncio
import logging
import json
from datetime import datetime
from client import Client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Server:
    def __init__(self, host='localhost', port=5050):
        self.__host = host
        self.__port = port
        # self.__header = header
        self.__format = 'utf-8'
        self.__lock = asyncio.Lock()
        self.clients = {}

    async def handle_client(self, reader, writer):
        client_addr = writer.get_extra_info('peername')
        client_id = f"{client_addr[0]}:{client_addr[1]}"
        logging.info(f"[NEW CONNECTION] {client_addr} connected.")
        connected = True
        self.clients[client_id]= Client(
                                    writer=writer, 
                                    connected_at=datetime.now(),
                                    msgs_count=0
                                )
        try:
            welcome_msg = {
                'type': 'welcome',
                'msg': f'Welcome! You are connected as {client_id}',
                'timestamp': datetime.now().isoformat()
            }
            await self.send_message(writer, welcome_msg)
            while connected:
                data = await reader.read(1024)
                if not data:
                    break
        except Exception as e:
            logging.error(f"Error occured with a client {client_id}: {e}")

        async with self.__lock:
            await self.disconnect_client(client_id)

    async def send_message(self, writer, msg):
        try:
            if isinstance(msg, dict):
                msg = json.dumps(msg)
            writer.write(msg.encode(self.__format))
            await writer.drain()
        except Exception as e:
            logging.error(f"Error with sending a message: {e}")

    async def disconnect_client(self, client_id:int):
        if client_id in self.clients.keys():
            try:
                self.clients[client_id]['writer'].close()
                await self.clients[client_id]['writer'].wait_closed()
            except:
                pass
            del self.clients[client_id]
            logging.info(f"[CLIENT]{client_id} was disconnected")

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client,
            self.__host,
            self.__port
        )
        logging.info(f"[LISTENING] Server is listening on {self.__host}")

        async with server:
            await server.serve_forever()

