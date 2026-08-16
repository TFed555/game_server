from .packetparser import PacketParser
import models.packet_pb2
import logging

class EchoParser(PacketParser):
    def encode(self, message) -> models.packet_pb2.PacketType | bytes:
        packet_type = models.packet_pb2.PacketType.PONG
        return (packet_type, message)
    
    def decode(self, payload):
        return payload.decode(super().FORMAT)