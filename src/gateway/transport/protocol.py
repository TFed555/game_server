from typing import TypeVar, Generic
import models.packet_pb2 as packet_pb2

T = TypeVar('T', packet_pb2.ClientMessage, packet_pb2.ServerMessage)
K = TypeVar('K', packet_pb2.ClientMessage, packet_pb2.ServerMessage)

class Protocol(Generic[T,K]):
    def __init__(self, incoming_msg: type[T], outgoing_msg: type[K]):
        self.incoming_msg = incoming_msg
        self.outgoing_msg = outgoing_msg
    HEADER_SIZE = 4
    MAX_PACKET_SIZE = 1 * 1024 * 1024

    async def read_packet(self, reader) -> T:
        prefix = int.from_bytes(await reader.readexactly(self.HEADER_SIZE), 'big')
        if prefix > self.MAX_PACKET_SIZE:
            raise ValueError(f"Message too big: {prefix} bytes")
        data = await reader.readexactly(prefix)
        msg = self.incoming_msg()
        msg.ParseFromString(data)
        return msg

    async def write_packet(self, writer, msg: K):
        data = msg.SerializeToString()
        length = len(data)
        prefix = length.to_bytes(self.HEADER_SIZE, 'big')
        writer.write(prefix)
        writer.write(data)
        await writer.drain()
