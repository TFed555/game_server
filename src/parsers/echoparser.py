from .packetparser import PacketParser
from models.packet import PacketType
import logging

class EchoParser(PacketParser):
    def encode(self, message) -> PacketType | bytes:
        packet_type = PacketType.PONG
        return (packet_type, message)
    
    def decode(self, payload):
        return payload.decode(super().FORMAT)