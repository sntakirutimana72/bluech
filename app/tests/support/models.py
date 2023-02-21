import contextlib

from app.tests.support.declarations import Models
from app.models import *

def create_user(**options) -> User:
    return User.create(**Models.user(**options))

def create_channel(**options) -> Channel:
    return Channel.create(**Models.channel(**options))

def create_member(**options) -> Member:
    return Member.create(**options)

def create_message(**options) -> Message:
    return Message.create(**options)

def create_resource(**options) -> Resource:
    return Resource.create(**Models.resource(**options))

def create_activity(**options) -> Activity:
    return Activity.create(**Models.activity(**options))

def create_activity_log(**options) -> Activity:
    return ActivityLog.create(**Models.activity_log(**options))


class InstantUse:
    @staticmethod
    @contextlib.contextmanager
    def admin_user(**options):
        admin = create_user(**options)
        yield admin
        admin.delete_instance()

    @staticmethod
    @contextlib.contextmanager
    def member(**options):
        _member = create_member(**options)
        yield _member
        _member.delete_instance()

    @staticmethod
    @contextlib.contextmanager
    def message(**options):
        _message = create_message(**options)
        yield _message
        _message.delete_instance()
