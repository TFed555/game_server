from protocol import protocol
import asyncio

HOST = 'localhost'
PORT = 5050
FORMAT = 'utf-8'

reader=None
writer=None

async def recv():
    while True:
        prefix = int.from_bytes(await reader.readexactly(4), "big")
        data = await reader.readexactly(prefix)
        if not data:
            break
        print(data.decode(FORMAT).rstrip())

async def send():
    while True:
        msg = await asyncio.to_thread(input)
        prefix = protocol(msg)
        writer.write(prefix)
        writer.write(msg.encode(FORMAT))
        await writer.drain()

async def main():
    global reader, writer

    reader, writer = await asyncio.open_connection(HOST, PORT)
    
    recv_task = asyncio.create_task(recv())
    send_task = asyncio.create_task(send())

    await asyncio.gather(recv_task, send_task)

if __name__ == "__main__":
    asyncio.run(main())