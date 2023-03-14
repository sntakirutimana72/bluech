import pytest

from .conftest import ControllerTestCases
from ..support.mocks.clients import AppClientSpec
from ..support.models import create_user, create_message
from ..support.responses import Skeletons
from ...models import Message

class TestMessagesController(ControllerTestCases):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.user = create_user()
        cls.rec_user = create_user(email='rec@email.eu')
        cls.rec_client = AppClientSpec()

    @classmethod
    def teardown_class(cls):
        super().teardown_class()
        delattr(cls, 'rec_client')
        delattr(cls, 'user')
        delattr(cls, 'rec_user')

    async def affirmSigns(self):
        if self.client.connected:
            return
        # signing primary user
        await self.assertSigninSuccess(email=self.user.email, password='test@123')
        # signing secondary user
        await self.assertSignin(self.rec_client, user={'email': self.rec_user.email, 'password': 'test@123'})

    def assertMessageResponse(self, proto: str, edited: bool, user, resp: dict):
        self.assert_true(Skeletons.new_message(resp))
        self.assertResponse(200, proto, resp)
        self.assert_equals(resp['message']['sender']['email'], user.email)
        self.assert_equals(resp['message']['is_edited'], edited)
        self.assert_true(Message.select().exists())

    @pytest.mark.asyncio
    async def test_new_message_success(self):
        await self.affirmSigns()
        # send a message
        await self.client.post_message('new_message', recipient=self.rec_user.id)
        # receive message
        resp = await self.rec_client.receive()
        # Then, assert
        self.assertMessageResponse('new_message', False, self.user, resp)

    @pytest.mark.asyncio
    async def test_edit_message_success(self):
        await self.affirmSigns()
        # create a demo message
        tmp_msg = create_message(recipient=self.user, sender=self.rec_user, description='Hola!')
        # send a message
        await self.rec_client.post_message('edit_message', params={'id': tmp_msg.id}, description='Salut!')
        # receive message
        resp = await self.client.receive()
        # Then, assert
        self.assertMessageResponse('edit_message', True, self.rec_user, resp)
