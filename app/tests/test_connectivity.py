import pytest

from .support.mocks.servers import ConnectivityMockServer
from .support.mocks.clients import ConnectivityClientSpec

@pytest.fixture(scope='module')
def server(event_loop):
    _server = ConnectivityMockServer()
    event_loop.run_until_complete(_server.initiate())
    return _server

@pytest.mark.asyncio
async def test_client_connection(server):
    assert server.con_counter == 0
    client = ConnectivityClientSpec()
    await client.connect()
    tls = await client.receive()
    assert tls == b'helo'
    assert server.con_counter != 0
    await client.disconnect()
