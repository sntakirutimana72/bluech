import unittest as unit
import peewee as pee
import pytest

from ..support.helpers import create_user
from ...models import User

@pytest.mark.usefixtures('configure_db', 'user')
class UserTestCases(unit.TestCase):

    def test_valid_user(self):
        self.assertIsInstance(self.user, User)

    def test_email_uniqueness(self):
        with self.assertRaises(pee.IntegrityError):
            create_user()

    def test_email_cannot_be_null(self):
        with self.assertRaises(pee.IntegrityError):
            create_user(email=None)

    def test_email_cannot_be_more_than_100(self):
        with self.assertRaises(pee.DataError):
            create_user(email=('johnde@'*15))

    def test_nickname_cannot_be_null(self):
        with self.assertRaises(pee.IntegrityError):
            create_user(email="noway@", nickname=None)

    def test_nickname_cannot_be_more_than_12(self):
        with self.assertRaises(pee.DataError):
            create_user(email="noway1@", nickname='cdsakhoer903228jgwe098')

    def test_password_cannot_be_null(self):
        with self.assertRaises(pee.IntegrityError):
            create_user(email="noway3@", password=None)
