from dataclasses import dataclass
from enum import Enum

class PacketType(Enum):
    CONNECT = 0
    DISCONNECT = 1
    PING = 2
    PONG = 3
    LOGIN = 4
    AUTH = 5

@dataclass
class Packet:
    type: PacketType
    payload: bytes