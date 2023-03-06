import pytest
import asyncio as io
import itertools

a = [1, 50]
b = [2, 2000]

for a, b in itertools.arr

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
        
@pytest.mark.usefixtures('user', 'user_avatar')
class TestChangeAvatar(ControllerTestCases):
    @pytest.mark.asyncio
    async def test_with_bad_request(self):
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        resp = await self.client.change_user_avatar(**self.avatar)
