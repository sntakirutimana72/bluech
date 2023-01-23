import pytest

from ...models import User

@pytest.fixture(scope='class', autouse=True)
def configure_db(configure_db):
    yield configure_db
    
@pytest.fixture
def create_user():
    def _insert_row(**options):
        return User.create({
            'email': 'admin@email.com',
            'password': '1234',
            'nickname': 'josh567',
            **options
        })
    return _insert_row

@pytest.fixture
def create_singleuse_user(create_user):
    def _create_new(**options):
        user = create_user(**options)
        yield user
        user.delete_instance()
    return _create_new
