import pytest
import asyncio

from ...settings import HOST_URL, HOST_PORT
from ...utils.middlewares import accept_conn

@pytest.fixture(scope='module')
def server(event_loop):
    s = event_loop.run_until_complete(asyncio.start_server(accept_conn, HOST_URL, HOST_PORT))
    return s

@pytest.fixture(scope='class')
async def clis_con(request):
    def _ready(r_stream=None, w_stream=None):
        request.cls._reader = r_stream
        request.cls._writer = w_stream

    reader, writer = await asyncio.open_connection(host=HOST_URL, port=HOST_PORT)
    _ready(reader, writer)
    yield
    _ready()
    writer.close()
    await writer.wait_closed()
