import unittest as unit
import peewee as pee
import pytest

from ...models import *

def new_user(**options):
    user = User.create(**{
        'email': 'admin@email.com',
        'password': '1234',
        'nickname': 'josh567',
        **options
    })
    return user
    
@pytest.fixture(scope='class')
def user(request):
    request.cls.user = new_user()

@pytest.mark.usefixtures('configure_db', 'user')
class UserTestCases(unit.TestCase):

    def test_valid_user(self):
        self.assertIsInstance(self.user, User)

    # def test_email_uniqueness(self):
    #     with self.assertRaises(pee.IntegrityError):
    #         new_user()

    # def test_email_cannot_be_null(self):
    #     with self.assertRaises(pee.IntegrityError):
    #         new_user(email=None)
            
    # def test_email_cannot_be_more_than_100(self):
    #     with self.assertRaises(pee.DataError):
    #         new_user(email=('johnde@'*15))
            
    # def test_nickname_cannot_be_null(self):
    #     with self.assertRaises(pee.IntegrityError):
    #         new_user(email="noway@", nickname=None)
    
    # def test_nickname_cannot_be_more_than_12(self):
    #     with self.assertRaises(pee.DataError):
    #         new_user(email="noway1@", nickname='cdsakhoer903228jgwe098')
            
    # def test_password_cannot_be_null(self):
    #     with self.assertRaises(pee.IntegrityError):
    #         new_user(email="noway3@", password=None)
