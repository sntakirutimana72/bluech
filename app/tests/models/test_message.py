import unittest
import pytest
import peewee as pee

from ..support.models import InstantUse
from ...models import Message

@pytest.mark.usefixtures('configure_db', 'message')
class MessageTestCases(unittest.TestCase):

    def test_valid_message(self):
        self.assertIsInstance(self.message, Message)

    def test_backrefs(self):
        self.assertTrue(self.user.messages.exists())
        self.assertFalse(self.user.receipts.exists())

        self.assertFalse(self.other_user.messages.exists())
        self.assertTrue(self.other_user.receipts.exists())

    def test_integrity_on_sender_or_recipient(self):
        with self.assertRaises(pee.IntegrityError):
            self.message.sender = None
            self.message.save()
        with self.assertRaises(pee.IntegrityError):
            self.message.recipient = None
            self.message.save()

    def test_has_replies(self):
        with InstantUse.message(sender=self.other_user, recipient=self.user, reply_to=self.message) as reply:
            self.assertTrue(self.message.replies.exists())
            self.assertIn(reply, list(self.message.replies))
