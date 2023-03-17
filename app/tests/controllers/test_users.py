import pytest
import os

import app.utils.layers as aul
from .conftest import ControllerTestCases
from ...models import ActivityLog

class TestChangeUsername(ControllerTestCases):
    @pytest.mark.asyncio
    async def test_bad_request(self):
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        resp = await self.client.edit_username(request={'body': {}})
        self.assertResponse(400, 'invalid_request', resp)

        await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_resource_not_changed(self):
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        resp = await self.client.edit_username(nickname=self.user.nickname)
        self.assertResponse(304, 'resource_not_changed', resp)

        await self.client.disconnect()

    @pytest.mark.asyncio
    async def test_success(self):
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        old_count = ActivityLog.select().count()
        resp = await self.client.edit_username()
        self.assertResponse(200, 'edit_username_success', resp)
        self.assert_equals(ActivityLog.select().count(), old_count + 1)
        self.assert_dict_has_key(resp, 'user')

        await self.client.disconnect()

class TestChangeAvatar(ControllerTestCases):
    @pytest.mark.asyncio
    async def test_successful_change(self, avatars_path, user_avatar, mocker):
        mocker.patch.object(aul, 'AVATARS_PATH', avatars_path)
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        old_count = ActivityLog.select().count()
        resp = await self.client.change_user_avatar(**user_avatar)
        self.assertResponse(200, 'change_avatar_success', resp)
        self.assert_equals(ActivityLog.select().count(), old_count + 1)
        self.assertIn(f'avatar_{self.user.id}.png', os.listdir(avatars_path))

        await self.client.disconnect()
