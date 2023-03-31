import unittest
import pytest
import peewee as pee

from ..support.models import create_activity
from ...models import Activity

@pytest.mark.usefixtures('activity')
class ActivityTestCases(unittest.TestCase):
    def test_is_valid(self):
        self.assertTrue(Activity.select().exists())
        self.assertIsInstance(self.activity, Activity)

    def test_uniqueness(self):
        with self.assertRaises(pee.IntegrityError):
            create_activity()

    def test_datatype_integrity(self):
        with self.assertRaises(pee.DataError):
            self.activity.level = 'LOGOUT'
            self.activity.save()
