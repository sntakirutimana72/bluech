import unittest as unit
import peewee as pee

from ..models import *

class UserTestCases(unit.TestCase):

    def test_valid_user(self, create_singleuse_user):
        user = create_singleUse_user()
        self.assertIsInstance(user, User)

    def test_email_uniqueness(self, create_singleuse_user):
        create_singleuse_user()
        with self.assertRaises(pee.IntegrityError):
            create_singleuse_user()

    def test_email_cannot_be_null(self, create_singleuse_user):
        with self.assertRaises(pee.IntegrityError):
            create_singleuse_user(email=None)
            
    def test_email_cannot_be_more_than_100(self, create_singleuse_user):
        with self.assertRaises(pee.DataError):
            create_singleuse_user(email=('johnde@'*15))
            
    def test_nickname_cannot_be_null(self, create_singleuse_user):
        with self.assertRaises(pee.IntegrityError):
            create_singleuse_user(email="noway@", nickname=None)
    
    def test_nickname_cannot_be_more_than_12(self, create_singleuse_user):
        with self.assertRaises(pee.DataError):
            create_singleuse_user(email="noway1@", nickname='cdsakhoer903228jgwe098')
            
    def test_password_cannot_be_null(self, create_singleuse_user):
        with self.assertRaises(pee.IntegrityError):
            create_singleuse_user(email="noway3@", password=None)
