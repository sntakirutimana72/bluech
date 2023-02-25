import pytest

from ..support.mocks.servers import AppServerSpec
from ..support.mocks.clients import AppClientSpec
from ..support.unittests import PyTestCase

@pytest.fixture(scope='class')
def server(event_loop):
    server = AppServerSpec()
    event_loop.run_until_complete(server.initiate())
    yield
    event_loop.run_until_complete(server.terminate())

@pytest.mark.usefixtures('server')
class ControllerTestCases(PyTestCase):
    client: AppClientSpec

    @classmethod
    def setup_class(cls):
        cls.client = AppClientSpec()

    async def assertSigninSuccess(self, **user):
        resp = await self.client.login(**user)
        self.assertResponse(200, 'signin_success', resp)
        self.assert_dict_has_key(resp, 'user')
        return resp

    def assertResponse(self, status: int, proto: str, resp):
        self.assert_isinstanceof(resp, dict)
        self.assert_dict_has_key(resp, 'proto')
        self.assert_equals(resp['proto'], proto)
        self.assert_dict_has_key(resp, 'status')
        self.assert_equals(resp['status'], status)
