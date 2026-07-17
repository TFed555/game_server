from models.packet import Packet, PacketType

class Protocol:
    HEADER_SIZE = 4
    MAX_PACKET_SIZE = 1 * 1024 * 1024
    async def read_packet(self, reader) -> Packet:
        prefix = int.from_bytes(await reader.readexactly(self.HEADER_SIZE), 'big')
        if prefix > self.MAX_PACKET_SIZE:
            raise ValueError(f"Message too big: {prefix} bytes")
        data = await reader.readexactly(prefix)
        packet = Packet(PacketType(data[0]), data[1:])
        return packet

    async def write_packet(self, writer, packet):
        length = len(packet.payload) + 1
        prefix = length.to_bytes(self.HEADER_SIZE, 'big')
        data = packet.payload
        type_value = packet.type.value.to_bytes(1, 'big')
        data = prefix + type_value + data
        writer.write(data)
        await writer.drain()
