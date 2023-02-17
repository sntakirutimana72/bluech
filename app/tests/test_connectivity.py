import pytest

from .support.mocks.server import ConnectivityMockServer

@pytest.fixture(scope='module')
def server(event_loop):
    _server = ConnectivityMockServer()
    event_loop.run_until_complete(_server.initiate())
    return _server

@pytest.mark.asyncio
async def test_client_connection(server, cli_con, cli_discon):
    assert server.con_counter == 0
    reader, writer = await cli_con()
    tls = await reader.read()
    assert tls == b'helo'
    assert server.con_counter != 0
    await cli_discon(writer)
