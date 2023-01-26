import contextlib

from .declarations import Models
from ...models import *

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


class InstantUse:
    
    @staticmethod
    @contextlib.contextmanager
    def member(**options):
        member = create_member(**options)
        yield member
        member.delete_instance()
        
    @staticmethod
    @contextlib.contextmanager
    def message(**options):
        message = create_message(**options)
        yield message
        message.delete_instance()
