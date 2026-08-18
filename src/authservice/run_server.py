from authservice.server import AuthServiceServer
from domain.repositories import AuthRepositoryProtocol
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

def main():
    s = AuthServiceServer(AuthRepositoryProtocol())
    try:
        asyncio.run(s.serve())
    except KeyboardInterrupt:
        print('\n Server is stopping...')

if __name__ == "__main__":
    main()