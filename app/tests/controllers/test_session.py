import pytest

from .conftest import ControllerTestCases
from ..support.models import InstantUse

class SessionTestCases(ControllerTestCases):
    async def assertSession(self, status: int, proto: str, **user):
        resp = await self.client.login(**user)
        self.assertResponse(status, proto, resp)

class TestSigninAndSignoutFailure(SessionTestCases):
    @pytest.mark.asyncio
    async def test_bad_request(self):
        await self.assertSession(400, 'invalid_request')
        await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_unauthorized(self):
        user = {'email': 'admin@test', 'password': 'test@123'}
        await self.assertSession(401, 'signin_failure', **user)
        await self.client.disconnect()

class TestSigninAndSignoutSuccess(SessionTestCases):
    @pytest.mark.asyncio
    async def test_signin_success(self):
        with InstantUse.admin_user() as admin:
            credentials = {'email': admin.email, 'password': 'test@123'}
            await self.assertSigninSuccess(**credentials)
            await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_signout_success(self):
        with InstantUse.admin_user() as admin:
            # signing in
            credentials = {'email': admin.email, 'password': 'test@123'}
            await self.assertSigninSuccess(**credentials)
            # signing out
            resp = await self.client.logout()
            self.assertResponse(200, 'signout_success', resp)
            await self.client.disconnect()
