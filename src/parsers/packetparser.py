from abc import ABC, abstractmethod

class PacketParser(ABC):
    FORMAT = 'utf-8'
    @abstractmethod
    def encode(self, raw_bytes):
        pass
    def decode(self, raw_bytes):
        pass