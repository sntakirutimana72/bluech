import unittest
import pytest
import peewee as pee

from ..support.models import create_activity_log
from ...models import ActivityLog

@pytest.fixture(scope='class')
def log(request, activity, user):
    _log = create_activity_log(activity=activity, doer=user)
    request.cls.log = _log
    yield _log
    _log.delete_instance()

@pytest.mark.usefixtures('configure_db', 'log')
class ActivityLogTestCases(unittest.TestCase):

    def test_is_valid(self):
        self.assertTrue(ActivityLog.select().exists())
        self.assertIsInstance(self.log, ActivityLog)

    def test_summary_is_not_nullable(self):
        with self.assertRaises(pee.IntegrityError):
            self.log.summary = None
            self.log.save()

    def test_backrefs(self):
        self.assertTrue(self.user.activities.exists())
        self.assertTrue(self.activity.logs.exists())
