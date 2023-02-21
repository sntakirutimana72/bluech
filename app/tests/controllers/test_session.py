import pytest

from ..support.unittests import PyTestCase
from ..support.models import InstantUse
from ..support.mocks.clients import AppClientSpec

@pytest.mark.usefixtures('server')
class SessionTestCases(PyTestCase):
    client: AppClientSpec

    @classmethod
    def setup_class(cls):
        cls.client = AppClientSpec()

    async def assertResponse(self, status: int, proto: str, **user: dict[str, str]):
        resp = await self.client.login(**user)
        self.assert_isinstanceof(resp, dict)
        self.assert_dict_has_key(resp, 'proto')
        self.assert_equals(resp['proto'], proto)
        self.assert_dict_has_key(resp, 'status')
        self.assert_equals(resp['status'], status)

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

class TestSigninAndSignoutSuccess(SessionTestCases):
    @pytest.mark.asyncio
    async def test_signin_success(self):
        with InstantUse.admin_user() as admin:
            credentials = {'email': admin.email, 'password': 'test@123'}
            await self.assertResponse(200, 'signin_success', **credentials)
            await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_signout_success(self):
        with InstantUse.admin_user() as admin:
            # signing in
            credentials = {'email': admin.email, 'password': 'test@123'}
            await self.assertResponse(200, 'signin_success', **credentials)
            # signing out
            resp = await self.client.logout()
            self.assert_isinstanceof(resp, dict)
            self.assert_dict_has_key(resp, 'proto')
            self.assert_equals(resp['proto'], 'signout_success')
            await self.client.disconnect()
