import server
import asyncio

def main():
    s = server.Server()
    try:
        asyncio.run(s.start())
    except KeyboardInterrupt:
        print('\n Server is stopping...')

if __name__ == "__main__":
    main()