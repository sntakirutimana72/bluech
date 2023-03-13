import pytest

from .conftest import ControllerTestCases
from ..support.mocks.clients import AppClientSpec
from ...models import Message

@pytest.mark.usefixtures('user', 'other_user')
class TestMessagesController(ControllerTestCases):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.rec_client = AppClientSpec()

    @pytest.mark.asyncio
    async def test_successful_exchange(self):
        # signing sender
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        # signing recipient
        await self.assertSignin(self.rec_client, user={'email': self.other_user.email, 'password': 'test@123'})
        # send a message
        await self.client.new_message(recipient=self.other_user.id)
        # receive message
        resp = await self.rec_client.receive()
        # Then, assert
        self.assertResponse(200, 'new_message', resp)
        self.assert_dict_has_key(resp, 'message')
        self.assert_dict_has_key(resp['message'], 'sender')
        self.assert_dict_has_key(resp['message'], 'is_edited')
        self.assert_true(Message.select().exists())
