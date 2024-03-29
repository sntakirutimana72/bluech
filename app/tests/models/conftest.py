import pytest

from ..support.models import create_message, create_activity, create_user

@pytest.fixture(scope='class')
def user(request):
    _user = create_user()
    request.cls.user = _user
    yield _user
    _user.delete_instance()

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

@pytest.fixture(scope='class')
def activity(request):
    _activity = create_activity()
    request.cls.activity = _activity
    yield _activity
    _activity.delete_instance()
