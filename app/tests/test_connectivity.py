import pytest
import asyncio

from .support.mocks.server import ConnectivityMockServer

@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='module')
def server(event_loop):
    _server = ConnectivityMockServer()
    event_loop.run_until_complete(_server.initiate())
    return _server

@pytest.fixture
def client():
    def wrapper(host='localhost', port=8080):
        return asyncio.open_connection(host=host, port=port)
    return wrapper
