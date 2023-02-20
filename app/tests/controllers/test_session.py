import pytest

from ..support.unittests import PyTestCase
from ..support.models import InstantUse
from ..support.mocks.clients import AppClientSpec
from ..support.declarations import RequestSpecs

@pytest.mark.usefixtures('server')
class SessionTestCases(PyTestCase):
    client: AppClientSpec

    async def assertResponse(self, status: int, proto: str, **user: dict[str, str]):
        resp = await self.signin(**user)
        self.assert_isinstanceof(resp, dict)
        self.assert_dict_has_key(resp, 'proto')
        self.assert_equals(resp['proto'], proto)
        self.assert_dict_has_key(resp, 'status')
        self.assert_equals(resp['status'], status)

    async def signin(self, **credentials: dict[str, str]):
        # connect to server
        self.client = await AppClientSpec().connect()
        # formatting data and packing it for a specific factory pattern recognizable by the server
        await self.client.send(RequestSpecs.signin(**credentials))
        # now, receive server response
        resp = await self.client.receive()
        return resp

class TestSigninFailure(SessionTestCases):
    @pytest.mark.asyncio
    async def test_bad_request(self):
        await self.assertResponse(400, 'signin_failure')
        await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_unauthorized(self):
        user = {'email': 'admin@test', 'password': 'test@123'}
        await self.assertResponse(401, 'signin_failure', **user)
        await self.client.disconnect()

class TestSigninSuccess(SessionTestCases):
    @pytest.mark.asyncio
    async def test_success(self):
        with InstantUse.admin_user() as admin:
            credentials = {'email': admin.email, 'password': 'test@123'}
            await self.assertResponse(200, 'signin_success', **credentials)
            await self.client.disconnect()
