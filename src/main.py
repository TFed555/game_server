from gateway.transport.tcp_server import TCP_Server
import asyncio

def main():
    s = TCP_Server()
    try:
        asyncio.run(s.start())
    except KeyboardInterrupt:
        print('\n Server is stopping...')

if __name__ == "__main__":
    main()