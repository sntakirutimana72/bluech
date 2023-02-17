import pytest
import asyncio

from ...settings import HOST_URL, HOST_PORT
from ...utils.middlewares import accept_conn

@pytest.fixture(scope='module')
def server(event_loop):
    s = event_loop.run_until_complete(asyncio.start_server(accept_conn, HOST_URL, HOST_PORT))
    return s

@pytest.fixture(scope='class')
async def ccli_con(request, cli_discon):
    def initiate(r_stream=None, w_stream=None):
        request.cls._reader = r_stream
        request.cls._writer = w_stream

    reader, writer = await asyncio.open_connection(host=HOST_URL, port=HOST_PORT)
    initiate(reader, writer)
    yield
    initiate()
    await cli_discon(writer)
    
@pytest.fixture
async def cli_con(cli_discon):
    pipe = await asyncio.open_connection(host=HOST_URL, port=HOST_PORT)
    yield pipe
    await cli_discon(pipe[1])
