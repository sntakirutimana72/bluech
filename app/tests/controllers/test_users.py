import pytest
import os

import app.utils.layers as aul
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
    async def test_successful_change(self, avatars_path, user_avatar, mocker):
        mocker.patch.object(aul, 'AVATARS_PATH', avatars_path)
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        resp = await self.client.change_user_avatar(**user_avatar)
        self.assertResponse(200, 'change_avatar_success', resp)
        self.assertIn(f'avatar_{self.user.id}.png', os.listdir(avatars_path))
        await self.client.disconnect()
