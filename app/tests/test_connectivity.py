import pytest
import asyncio

from .support.mocks.server import ConnectivityMockServer

@pytest.fixture(scope='module')
def server(event_loop):
    _server = ConnectivityMockServer()
    event_loop.run_until_complete(_server.initiate())
    return _server

@pytest.fixture
def fcli_con():
    def connect(host='localhost', port=8080):
        return asyncio.open_connection(host=host, port=port)
    return connect

@pytest.fixture
def fcli_discon():
    async def disconnect(pipe):
        pipe.close()
        await pipe.wait_closed()
    return disconnect


@pytest.mark.asyncio
async def test_client_connection(server, fcli_con, fcli_discon):
    assert server.con_counter == 0
    reader, writer = await fcli_con()
    tls = await reader.read()
    assert tls == b'helo'
    assert server.con_counter != 0
    await fcli_discon(writer)
