import pytest
import os

from .conftest import ControllerTestCases

@pytest.mark.usefixtures('user')
class TestChangeUsername(ControllerTestCases):
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

@pytest.mark.usefixtures('user')
class TestChangeAvatar(ControllerTestCases):
    @pytest.mark.asyncio
    async def test_with_bad_request(self, avatars_path, user_avatar):
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        resp = await self.client.change_user_avatar(**user_avatar)
        print(os.listdir(avatars_path))
        self.assertResponse(200, 'change_avatar_success', resp)
        await self.client.disconnect()
