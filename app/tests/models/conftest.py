import pytest

from ..support.helpers import create_user, create_channel, create_member

@pytest.fixture(scope='class')
def user(request):
    _user = create_user()
    request.cls.user = _user
    yield _user
    _user.delete_instance()
    
@pytest.fixture(scope='class')
def channel(request, user):
    _channel = create_channel(created_by=user)
    request.cls.channel = _channel
    yield _channel
    _channel.delete_instance()
