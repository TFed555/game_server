from gateway.transport.protocol import Protocol
from models.packet import Packet, PacketType
import asyncio

HOST = 'localhost'
PORT = 5050
FORMAT = 'utf-8'

reader=None
writer=None

async def recv():
    while True:
        protocol = Protocol()
        packet = await protocol.read_packet(reader)
        if not packet:
            break
        print(packet.payload.decode(FORMAT).rstrip())

async def send():
    while True:
        protocol = Protocol()
        msg = await asyncio.to_thread(input)
        packet = Packet(PacketType.PING, msg.encode(FORMAT))
        await protocol.write_packet(writer, packet)
        # msg = await asyncio.to_thread(input)
        # prefix = protocol(msg)
        # writer.write(prefix)
        # writer.write(msg.encode(FORMAT))
        # await writer.drain()

async def main():
    global reader, writer

    reader, writer = await asyncio.open_connection(HOST, PORT)
    
    recv_task = asyncio.create_task(recv())
    send_task = asyncio.create_task(send())

    await asyncio.gather(recv_task, send_task)

if __name__ == "__main__":
    asyncio.run(main())