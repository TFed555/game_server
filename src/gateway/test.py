from gateway.transport.protocol import Protocol
from proto.packet_pb2 import ClientMessage, ServerMessage
import asyncio

HOST = 'localhost'
PORT = 5050
FORMAT = 'utf-8'

reader=None
writer=None

async def recv(protocol):
    while True:
        packet = await protocol.read_packet(reader)
        print(packet)
        if not packet:
            break
        if packet.HasField("ping"):
            response = ClientMessage()
            response.pong.SetInParent()
            await protocol.write_packet(writer, response)
            continue
        # print(packet.echo.message.rstrip()) 

async def send(protocol):
    while True:
        msg = await asyncio.to_thread(input)
        packet = ClientMessage()
        if msg == 'login':
            packet.login.message = msg
        else:
            packet.echo.message = msg
        await protocol.write_packet(writer, packet)

async def main():
    global reader, writer

    reader, writer = await asyncio.open_connection(HOST, PORT)
    protocol = Protocol(incoming_msg=ServerMessage, outgoing_msg=ClientMessage)
    recv_task = asyncio.create_task(recv(protocol))
    send_task = asyncio.create_task(send(protocol))

    await asyncio.gather(recv_task, send_task)

if __name__ == "__main__":
    asyncio.run(main())