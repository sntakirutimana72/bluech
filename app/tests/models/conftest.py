import pytest

from ..support.helpers import create_user, create_channel, create_message

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
    
@pytest.fixture(scope='class')
def other_user(request):
    _user = create_user(email='other_user@email')
    request.cls.other_user = _user
    yield _user
    _user.delete_instance()

@pytest.fixture(scope='class')
def message(request, other_user, user):
    _message = create_message(sender=user, recipient=other_user)
    request.cls.message = _message
    yield _message
    _message.delete_instance()
