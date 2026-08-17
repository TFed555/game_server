import pytest
import asyncio
from models.packet_pb2 import ClientMessage
from models.connection import Connection
from gateway.routing.router import Router
from unittest.mock import Mock, AsyncMock
from datetime import datetime


@pytest.mark.asyncio
async def test_router_routes_echo():
    handler =  AsyncMock()
    router = Router()
    router.handlers["echo"]=handler

    message = ClientMessage()
    message.echo.message = "hello"
    mockWriter = Mock()
    mockReader = Mock()

    conn = Connection('1',mockWriter,mockReader,datetime.now(),datetime.now(),asyncio.current_task())

    await router.route(message,conn)

    handler.handle.assert_awaited_once()

@pytest.mark.asyncio
async def test_router_routes_pong():
    handler = AsyncMock()
    router = Router()
    router.handlers["pong"]=handler

    message = ClientMessage()
    message.pong.SetInParent()
    mockWriter = Mock()
    mockReader = Mock()

    conn = Connection('1',mockWriter,mockReader,datetime.now(),datetime.now(),asyncio.current_task())

    await router.route(message,conn)

    handler.handle.assert_awaited_once()

@pytest.mark.asyncio
async def test_router_rejects_empty_message():
    router = Router()

    message = ClientMessage()
    mockWriter = Mock()
    mockReader = Mock()
    conn = Connection('1',mockWriter,mockReader,datetime.now(),datetime.now(),asyncio.current_task())

    res = await router.route(message, conn)

    assert res is None

