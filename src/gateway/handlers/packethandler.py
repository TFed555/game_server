from abc import ABC, abstractmethod

class PacketHandler(ABC):
    @abstractmethod
    async def handle(self, packet):
        pass