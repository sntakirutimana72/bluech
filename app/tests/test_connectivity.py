import pytest
import asyncio

from .support.mocks.server import ConnectivityMockServer

@pytest.fixture(scope='module')
def server(event_loop):
    _server = ConnectivityMockServer()
    event_loop.run_until_complete(_server.initiate())
    return _server

@pytest.mark.asyncio
async def test_client_connection(server, disconnect_client, connect_client):
    assert server.con_counter == 0
    reader, writer = await connect_client()
    tls = await reader.read()
    assert tls == b'helo'
    assert server.con_counter != 0
    await disconnect_client(writer)
