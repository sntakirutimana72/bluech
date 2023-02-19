import pytest

from ..support.unittests import PyTestCase
from ..support.mocks.clients import AppClientSpec
from ..support.declarations import RequestSpecs

@pytest.mark.usefixtures('server')
class TestSigninFailure(PyTestCase):
    async def assertResponse(self, status, **user):
        # connect to server
        client = AppClientSpec()
        await client.connect()
        # formatting data and packing it for a specific factory pattern recognizable by the server
        await client.send(RequestSpecs.signin(**user))
        # now, receive server response
        resp = await client.receive()

        self.assert_isinstanceof(resp, dict)
        self.assert_dict_has_key(resp, 'proto')
        self.assert_equals(resp['proto'], 'signin_failure')
        self.assert_dict_has_key(resp, 'status')
        self.assert_equals(resp['status'], status)

        await client.disconnect()

    @pytest.mark.asyncio
    async def test_bad_request(self):
        await self.assertResponse(400)

    @pytest.mark.asyncio
    async def test_unauthorized(self):
        user = {'email': 'admin@test', 'password': 'test@123'}
        await self.assertResponse(401, **user)
