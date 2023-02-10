import pytest
import asyncio

from ...settings import HOST_URL, HOST_PORT
from ...utils.middlewares import accept_conn

@pytest.fixture(scope='module')
def server(event_loop):
    s = event_loop.run_until_complete(asyncio.start_server(accept_conn, HOST_URL, HOST_PORT))
    return s

@pytest.fixture(scope='class')
def connect_sclient():
    return asyncio.open_connection(host=HOST_URL, port=HOST_PORT)
