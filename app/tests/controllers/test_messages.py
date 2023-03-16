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
        cls.rec_user = create_user(email='rec@email.eu')
        cls.rec_client = AppClientSpec()

    @classmethod
    def teardown_class(cls):
        super().teardown_class()
        delattr(cls, 'rec_client')
        delattr(cls, 'rec_user')

    def tmp_message(self):
        return create_message(recipient=self.user, sender=self.rec_user, description='Hola!')

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

    def assertRemove(self, user_id, msg_id, resp):
        self.assert_true(Skeletons.remove_message(resp))
        self.assertResponse(200, 'remove_message', resp)
        self.assert_equals(resp['message_id'], msg_id)
        self.assert_equals(resp['benefactor']['id'], user_id)

    @pytest.mark.asyncio
    async def test_new_message_success(self):
        await self.affirmSigns()
        await self.client.post_message('new_message', recipient=self.rec_user.id)
        resp = await self.rec_client.receive()
        self.assertMessageResponse('new_message', False, self.user, resp)

    @pytest.mark.asyncio
    async def test_edit_message_success(self):
        await self.affirmSigns()
        msg = self.tmp_message()
        await self.rec_client.post_message('edit_message', params={'id': msg.id}, description='Salut!')
        resp = await self.client.receive()
        self.assertMessageResponse('edit_message', True, self.rec_user, resp)

    @pytest.mark.asyncio
    async def test_remove_message_success(self):
        await self.affirmSigns()
        msg_id = self.tmp_message().id
        await self.rec_client.post_message('remove_message', params={'id': msg_id})
        for client, user in ((self.rec_client, self.user), (self.client, self.rec_user)):
            resp = await client.receive()
            self.assertRemove(user.id, msg_id, resp)
        msg = Message.get_or_none(Message.id == msg_id)
        self.assert_is_none(msg)
