import pytest

from ..support.helpers import create_user

@pytest.fixture(scope='class')
def user(request):
    _user = create_user()
    request.cls.user = _user
    yield _user
    _user.delete_instance()
