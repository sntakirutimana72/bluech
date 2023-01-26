import unittest
import pytest
import peewee as pee

from ..support.helpers import create_resource
from ...models import Resource

@pytest.fixture(scope='class')
def resource(request):
    _resource = create_resource()
    request.cls.resource = _resource
    yield _resource
    _resource.delete_instance()

@pytest.mark.usefixtures('configure_db', 'channel', 'message', 'resource')
class ResourceTestCases(unittest.TestCase):
    
    def _assert_backrefs(self, state=False):
        self.assertIs(self.user.picture.exists(), state)
        self.assertIs(self.channel.attachments.exists(), state)
        self.assertIs(self.message.attachments.exists(), state)
        
    def _mass_alter(self, user=None, channel=None, message=None):
        self.resource.user = user
        self.resource.channel = channel
        self.resource.message = message
        self.resource.save()
    
    def test_is_valid(self):
        self.assertIsInstance(self.resource, Resource)
        
    def test_location_uniqueness(self):
        with self.assertRaises(pee.IntegrityError):
            create_resource()
            
    def test_backrefs(self):
        self._assert_backrefs()
        self._mass_alter(self.user, self.channel, self.message)
        self._assert_backrefs(True)
        self._mass_alter()
        self._assert_backrefs()
