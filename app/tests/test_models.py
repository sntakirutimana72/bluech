import unittest as unit
import peewee as pee

from ..utils.db_connect import db_connector, drop_schema
from ..models import *
from ..settings import DB_CONFIGS

class UserTestCases(unit.TestCase):

    def setUp(self):
        self.con = db_connector('test')
        self.create_user()

    def create_user(self, **kwargs):
        options = {
            'email': 'email1@test.com',
            'password': '1234',
            'nickname': 'john567',
            **kwargs
        }
        self.user = User.create(**options)

    def test_valid_user(self):
        self.assertIsInstance(self.user, User)

    def test_email_uniqueness(self):
        with self.assertRaises(pee.IntegrityError):
            self.create_user()

    def test_email_cannot_be_null(self):
        with self.assertRaises(pee.IntegrityError):
            self.create_user(email=None)

    def tearDown(self):
        self.con.close()
        self.con = None

        options = DB_CONFIGS['test'].copy()
        schema = options.pop('schema')
        drop_schema(schema, **options)
