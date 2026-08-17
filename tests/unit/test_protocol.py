import pytest
import asyncio

from models.packet_pb2 import ClientMessage, ServerMessage
from gateway.transport.protocol import Protocol

class MockWriter:
    def __init__(self):
        self.data = bytearray()

    def write(self, data):
        self.data.extend(data)

    async def drain(self):
        pass

class MockReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    async def readexactly(self, n):
        if self.pos + n > len(self.data):
            raise asyncio.IncompleteReadError(partial=self.data[self.pos:], expected=n)
        result = self.data[self.pos:self.pos+n]
        self.pos+=n
        return result

@pytest.mark.asyncio
async def test_write_valid_frame():
    protocol = Protocol(incoming_msg=ServerMessage, outgoing_msg=ClientMessage)
    writer = MockWriter()
    msg = ClientMessage()
    msg.echo.message = "hello"
    await protocol.write_packet(writer, msg)
    frame = bytes(writer.data)
    prefix = int.from_bytes(frame[:protocol.HEADER_SIZE], "big")
    data = frame[protocol.HEADER_SIZE:]
    assert prefix == len(data)
    decoded = ClientMessage()
    decoded.ParseFromString(data)
    assert decoded == msg

@pytest.mark.asyncio
async def test_read_valid_frame():
    protocol = Protocol(incoming_msg=ServerMessage, outgoing_msg=ClientMessage)
    msg = ServerMessage()
    msg.echo.message = "hello"
    data = msg.SerializeToString()
    prefix = len(data).to_bytes(protocol.HEADER_SIZE, "big")
    reader = MockReader(prefix+data)
    result = await protocol.read_packet(reader)
    assert result == msg

@pytest.mark.asyncio
async def test_read_incomplete_body():
    protocol = Protocol(incoming_msg=ServerMessage, outgoing_msg=ClientMessage)
    msg = ServerMessage()
    msg.echo.message = "hello"
    data = msg.SerializeToString()
    prefix = (10).to_bytes(protocol.HEADER_SIZE, "big")
    reader = MockReader(prefix+data)
    with pytest.raises(asyncio.IncompleteReadError):
        await protocol.read_packet(reader)

@pytest.mark.asyncio
async def test_read_incomplete_header():
    protocol = Protocol(incoming_msg=ServerMessage, outgoing_msg=ClientMessage)
    reader = MockReader(b"\x00\x00")
    with pytest.raises(asyncio.IncompleteReadError):
        await protocol.read_packet(reader)

@pytest.mark.asyncio
async def test_write_empty_msg():
    protocol = Protocol(incoming_msg=ServerMessage, outgoing_msg=ClientMessage)
    writer = MockWriter()
    msg=ClientMessage()
    await protocol.write_packet(writer, msg)
    frame = bytes(writer.data)
    prefix = int.from_bytes(frame[:protocol.HEADER_SIZE], "big")
    data = frame[protocol.HEADER_SIZE:]
    assert prefix == len(data)

@pytest.mark.asyncio
async def test_read_big_payload():
    protocol = Protocol(incoming_msg=ServerMessage, outgoing_msg=ClientMessage)
    msg = ServerMessage()
    msg.echo.message = bytes(1024*1024+1)
    data = msg.SerializeToString()
    prefix = len(data).to_bytes(protocol.HEADER_SIZE, "big")
    reader = MockReader(prefix+data)
    with pytest.raises(ValueError):
        await protocol.read_packet(reader)

@pytest.mark.asyncio
async def test_read_exact_payload():
    protocol = Protocol(incoming_msg=ServerMessage, outgoing_msg=ClientMessage)
    msg = ServerMessage()
    msg.echo.message = "a" * protocol.MAX_PACKET_SIZE

    data = msg.SerializeToString()

    assert len(data) > protocol.MAX_PACKET_SIZE