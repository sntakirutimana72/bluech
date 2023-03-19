import pytest

from .conftest import ControllerTestCases
from ..support.models import create_user
from ..support.mocks.clients import AppClientSpec

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
    def credentials(self, user=None):
        if user is None:
            user = self.user
        return {'email': user.email, 'password': 'test@123'}

    @pytest.mark.asyncio
    async def test_signin_success(self):
        await self.assertSigninSuccess(**self.credentials())
        await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_signout_success(self):
        await self.assertSigninSuccess(**self.credentials())
        # signing out
        resp = await self.client.logout()
        self.assertResponse(200, 'signout_success', resp)
        await self.client.disconnect()

    async def assertInMass(self, client: AppClientSpec, *args):
        for code, proto in args:
            res = await client.receive()
            self.assertResponse(code, proto, res)

    @pytest.mark.asyncio
    async def test_emissions_chronology(self):
        client_2 = AppClientSpec()
        client_3 = AppClientSpec()
        user_2 = create_user(email='user2@email.edu')
        user_3 = create_user(email='user3@email.edu')

        await self.assertSigninSuccess(**self.credentials())
        await self.assertSignin(client_2, self.credentials(user_2))
        await self.assertSignin(client_3, self.credentials(user_3))

        await self.assertInMass(self.client, *((200, 'connected'),)*2)
        await self.assertInMass(client_2, (200, 'all_users'), (200, 'connected'))
        await self.assertInMass(client_3, (200, 'all_users'))

        await client_2.disconnect()
        await self.assertInMass(self.client, (200, 'disconnected'))
        await self.assertInMass(client_3, (200, 'disconnected'))

        await client_3.disconnect()
        await self.client.disconnect()
