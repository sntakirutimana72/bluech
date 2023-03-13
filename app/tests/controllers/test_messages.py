import pytest

from .conftest import ControllerTestCases
from ..support.mocks.clients import AppClientSpec
from ..support.models import create_user
from ...models import Message

class TestMessagesController(ControllerTestCases):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.user = create_user()
        cls.rec_user = create_user(email='rec@email.eu')
        cls.rec_client = AppClientSpec()

    @pytest.mark.asyncio
    async def test_new_message_success(self):
        # signing sender
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        # signing recipient
        await self.assertSignin(self.rec_client, user={'email': self.rec_user.email, 'password': 'test@123'})
        # send a message
        await self.client.new_message(recipient=self.rec_user.id)
        # receive message
        resp = await self.rec_client.receive()
        # Then, assert
        self.assertResponse(200, 'new_message', resp)
        self.assert_dict_has_key(resp, 'message')
        self.assert_dict_has_key(resp['message'], 'sender')
        self.assert_equals(resp['message']['sender']['email'], self.user.email)
        self.assert_dict_has_key(resp['message'], 'is_edited')
        self.assert_true(Message.select().exists())
        # disconnect clients' connections
        await self.client.disconnect()
        await self.rec_client.disconnect()
