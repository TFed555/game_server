import asyncio
import logging
import json
from datetime import datetime
from protocol import protocol
from client import Client
from client import Mode

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
    
    MAX_MESSAGE_SIZE = 1 * 1024 * 1024 
    
    async def get_enabled_connections(self, client_id: int) -> list:
        return [
            cid for cid in self.clients.keys()
            if cid != client_id
        ]
    
    async def read_message(self, reader):
        prefix = int.from_bytes(await reader.readexactly(4), 'big')
        if prefix > self.MAX_MESSAGE_SIZE:
            raise ValueError(f"Message too big: {prefix} bytes")
        return await reader.readexactly(prefix)

    async def handle_client(self, reader, writer):
        client_addr = writer.get_extra_info('peername')
        client_id = f"{client_addr[0]}:{client_addr[1]}"
        logging.info(f"[NEW CONNECTION] {client_addr} connected.")
        connected = True
        self.clients[client_id] = Client(
                                    writer=writer,  
                                    reader=reader,
                                    pending_request=None,
                                    chatter_id=None,
                                    connected_at=datetime.now(),
                                    mode=None,
                                    msgs_count=0
                                )
        client = self.clients[client_id]
        await self.broadcast_connections()
        try:
            welcome_msg = {
                'type': 'welcome',
                'msg': f'Welcome! You are connected as {client_id}',
                'timestamp': datetime.now().isoformat()
            }
            await self.send_message(writer, welcome_msg)
            logging.info(f"Send msg to {client_id}")
            await self.choose_option_menu(writer=writer, reader=reader, client_id=client_id)
            while connected:
                enabled_users = await self.get_enabled_connections(client_id=client_id)
                data = await self.read_message(reader)
                if not data:
                    break
                msg = data.decode(self.__format)
                match client.mode:
                    case Mode.Chat:
                        if client.pending_request is not None and msg == "yes":
                            await self.create_chat_connection(client_id=client_id)
                            logging.info("First case")
                        elif client.chatter_id is not None:
                            receiver_id = self.clients[client_id].chatter_id
                            await self.send_message(self.clients[receiver_id].writer, msg)
                            logging.info("Second case")
                        else:
                           if msg.isdigit():
                               try:
                                    enabled_users = await self.get_enabled_connections(client_id=client_id)
                                    chatter_id = enabled_users[int(msg)-1]
                                    self.clients[chatter_id].pending_request=client_id
                                    await self.send_message(self.clients[chatter_id].writer, f"User {client_id} want to start chat with you! Enter 'yes' to begin chatting")
                               except IndexError:
                                    logging.error(f"Wrong idx")
                           logging.info("Third case")
                    case Mode.Echo:
                        await self.process_message(writer, client_id, msg)
                    case _:
                        logging.error("Unknown mode")
        except Exception as e:
            logging.error(f"Error occured with a client {client_id}: {e}")

        async with self.__lock:
            await self.disconnect_client(client_id)

    async def echo(self, client_id):
        self.clients[client_id].mode = Mode.Echo
        await self.send_message(self.clients[client_id].writer, "Choosed mode Echo")
    
    async def chat(self, client_id):
        self.clients[client_id].mode = Mode.Chat
        writer = self.clients[client_id].writer
        await self.send_message(writer, "Chose mode Chat")
        enabled_users = await self.get_enabled_connections(client_id=client_id)
        await self.send_message(writer, f"Choose possible users to chat: {enabled_users}")
        
    async def create_chat_connection(self, client_id):
        sender_id = self.clients[client_id].pending_request
        self.clients[client_id].chatter_id=sender_id
        self.clients[sender_id].chatter_id=client_id
        self.clients[client_id].pending_request=None
        await self.send_message(self.clients[client_id].writer, "Chat started!")
        await self.send_message(self.clients[sender_id].writer, "Chat started!")

    async def process_message(self, writer, client_id, msg):
        self.clients[client_id].msgs_count +=1
        logging.info(f"Message from {client_id}")
        response = {
            'type': 'echo',
            'message': f"Received '{msg}'",
            'timestamp': datetime.now().isoformat()
        }
        await self.send_message(writer, response)
    
    async def choose_option_menu(self, writer, reader, client_id):
        options = {'Chat': self.chat, 
                   'Echo': self.echo, 
                   'Exit': self.disconnect_client}
        message = f'Choose one of server options: {list(options.keys())}'
        await self.send_message(writer, message)
        choosing=True
        while choosing:
            try:
                data = await self.read_message(reader)
                command = data.decode(self.__format)
                if not data: 
                    break
                if command in options:
                    async with self.__lock:
                        await options[command](client_id)
                        choosing = False 
            except Exception as e:
                logging.error(f"Error with choosing option with client {client_id}: {e}")
                return
    
    async def broadcast_connections(self):
        for cid, info in self.clients.items():
            enabled_users = await self.get_enabled_connections(client_id=cid)
            try:
                await self.send_message(info.writer, f"New user added! Now list of users is {enabled_users}")
                logging.info(f"Send msg to {cid}")
            except Exception as e:
                logging.error(f"Error occured with {cid}")
    

    async def broadcast_message(self, msg):
        for i in self.clients.values():
            await self.send_message(i.writer, msg)

    async def send_message(self, writer, msg):
        try:
            if isinstance(msg, dict):
                msg = json.dumps(msg)
            prefix = protocol(msg)
            writer.write(prefix)
            writer.write(msg.encode(self.__format))
            await writer.drain()
        except Exception as e:
            logging.error(f"Error with sending a message: {e}")

    async def disconnect_client(self, client_id:int):
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
            self.handle_client,
            self.__host,
            self.__port
        )
        logging.info(f"[LISTENING] Server is listening on {self.__host}")

        async with server:
            await server.serve_forever()

