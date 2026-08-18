from gateway.transport.tcp_server import TCP_Server
import asyncio

def main():
    gatewayServer = TCP_Server()
    try:
        asyncio.run(gatewayServer.start())
    except KeyboardInterrupt:
        print('\n Server is stopping...')

if __name__ == "__main__":
    main()