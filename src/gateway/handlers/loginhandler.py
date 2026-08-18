from proto.auth_pb2 import LoginRequest
from proto.auth_pb2_grpc import AuthServiceStub
from .packethandler import PacketHandler
import grpc
from datetime import datetime
import logging

class LoginHandler(PacketHandler):
    async def handle(self, msg, conn): 
        channel = grpc.insecure_channel("localhost:50051")
        stub = AuthServiceStub(channel)
        if msg.login.login and msg.login.password:
            request = LoginRequest(login=msg.login.login, password=msg.login.password)
            response = stub.Login(request)
            print(response)
        else:
            logging.error("Not valid login request")
        return