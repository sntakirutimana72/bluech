import pytest

from .conftest import ControllerTestCases

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
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_signout_success(self):
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        # signing out
        resp = await self.client.logout()
        self.assertResponse(200, 'signout_success', resp)
        await self.client.disconnect()
