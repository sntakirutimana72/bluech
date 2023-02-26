import pytest

from .conftest import ControllerTestCases

@pytest.mark.usefixtures('user')
class TestEditNickname(ControllerTestCases):
    @pytest.mark.asyncio
    async def test_failure(self):
        # signing in
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        # Edit user nickname
        resp = await self.client.edit_username(request={'body': {}})
        self.assertResponse(400, 'invalid_request', resp)
        await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_success(self):
        # signing in
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        # Edit user nickname
        resp = await self.client.edit_username()
        self.assertResponse(200, 'edit_username_success', resp)
        self.assert_dict_has_key(resp, 'user')
        await self.client.disconnect()
