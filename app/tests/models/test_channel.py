import pytest
import unittest

from ...models import User, Channel

def new_channel(**options):
    channel = Channel(**{
        'nickname': 'channel_874', **options
    })
    return channel

@pytest.fixture(scope='class')
def user(request):
    user = User.create(email='c_user@email.it', password='1234', nickname='c_user')
    request.cls.user = user
    return user

@pytest.fixture(scope='class')
def channel(request, user):
    request.cls.channel = new_channel(created_by=user)

@pytest.mark.usefixtures('configure_db', 'user', 'channel')
class ChannelTestCases(unittest.TestCase):

    def test_valid_channel(self):
        self.assertIsInstance(self.channel, Channel)
        self.assertEqual(self.channel.created_by, self.user)
