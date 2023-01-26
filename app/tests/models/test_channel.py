import peewee as pee
import pytest
import unittest

from ..support.helpers import instant_member, create_channel
from ...models import Channel, Member

@pytest.fixture(scope='class')
def channel(request, user):
    _channel = create_channel(created_by=user)
    request.cls.channel = _channel
    yield _channel
    _channel.delete_instance()

@pytest.mark.usefixtures('configure_db', 'channel')
class ChannelTestCases(unittest.TestCase):

    @property
    def members(self):
        return self.channel.members

    @property
    def channels(self):
        return self.user.channels

    def test_valid_channel(self):
        self.assertIsInstance(self.channel, Channel)
        self.assertEqual(self.channel.created_by, self.user)

    def test_nickname_cannot_be_null(self):
        with self.assertRaises(pee.IntegrityError):
            self.user.nickname = None
            self.user.save()

    def test_nickname_cannot_be_more_than_12_chars(self):
        with self.assertRaises(pee.DataError):
            self.user.nickname = 'nickname' * 3
            self.user.save()

    def test_membership_backref(self):
        with instant_member(user=self.user, channel=self.channel, is_admin=True, is_creator=True):
            self.assertIn(self.user, list(self.members))
            self.assertIn(self.channel, list(self.channels))

    def test_add_and_remove_member(self):
        self.assertNotIn(self.user, list(self.members))
        self.members.add(self.user)
        self.assertIn(self.user, list(self.members))

        self.members.remove(self.user)
        self.assertNotIn(self.user, list(self.members))

    def test_add_and_remove_channel(self):
        self.assertNotIn(self.channel, list(self.channels))
        self.channels.add(self.channel)
        self.assertIn(self.channel, list(self.channels))

        self.channels.remove(self.channel)
        self.assertNotIn(self.channel, list(self.channels))

    def test_duplicate_membership(self):
        with instant_member(user=self.user, channel=self.channel):
            with self.assertRaises(pee.IntegrityError):
                Member.create(user=self.user, channel=self.channel)
