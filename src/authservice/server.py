from proto.auth_pb2_grpc import AuthServiceServicer, add_AuthServiceServicer_to_server
from proto.auth_pb2 import LoginResponse
import grpc
from domain.repositories.userrepository import AuthRepositoryProtocol
from domain.entities.userdomainmodel import UserDomainModel
import logging

class AuthServiceServer(AuthServiceServicer):
    def __init__(self, repo: AuthRepositoryProtocol):
        self.user_repository = repo

    async def Login(self, request, context):
        user = UserDomainModel(login=request.login, password_hash=request.password, is_active=True, id=None)
        user_id = self.user_repository.addUser(user)
        return LoginResponse(user_id = user_id)

    async def serve(self):
        server = grpc.aio.server()
        add_AuthServiceServicer_to_server(
            AuthServiceServer(self.repo),
            server
        )
        listen_addr = "localhost:50051"
        server.add_insecure_port(listen_addr)
        logging.info(f"Starting auth server on {listen_addr}")
        await server.start()
        await server.wait_for_termination()