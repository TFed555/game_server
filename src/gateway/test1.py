import server
import asyncio

HOST = 'localhost'
PORT = 5050

reader=None
writer=None

async def recv():
    while True:
        data = await reader.readline()
        if not data:
            break
        print(data.decode().rstrip())

async def send():
    pass

async def main():
    global reader, writer

    reader, writer = await asyncio.open_connection(HOST, PORT)
    
    recv_task = asyncio.create_task(recv())
    send_task = asyncio.create_task(send())

    await asyncio.gather(recv_task, send_task)

if __name__ == "__main__":
    asyncio.run(main())