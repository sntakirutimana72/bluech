import unittest
import pytest
import peewee as pee

from ..support.models import create_activity
from ...models import Activity

@pytest.mark.usefixtures('configure_db', 'activity')
class ActivityTestCases(unittest.TestCase):

    def test_is_valid(self):
        self.assertTrue(Activity.select().exists())
        self.assertIsInstance(self.activity, Activity)

    def test_uniqueness(self):
        with self.assertRaises(pee.IntegrityError):
            create_activity()

    def test_length_restriction(self):
        with self.assertRaises(pee.DataError):
            self.activity.name = 'LOGOUT' * 5
            self.activity.save()
