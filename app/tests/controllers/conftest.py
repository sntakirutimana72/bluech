import pytest

from ..support.mocks.servers import AppServerSpec

@pytest.fixture(scope='class')
def server(event_loop):
    server = AppServerSpec()
    event_loop.run_until_complete(server.initiate())
    yield
    event_loop.run_until_complete(server.terminate())
