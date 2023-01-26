import contextlib

from .declarations import Models
from ...models import User, Channel, Member, Message

def create_user(**options) -> User:
    user = User.create(**Models.user(**options))
    return user

def create_channel(**options) -> Channel:
    channel = Channel.create(**Models.channel(**options))
    return channel

def create_member(**options):
    return Member.create(**options)

def create_message(**options):
    return Message.create(**options)

@contextlib.contextmanager
def instant_member(**options):
    member = create_member(**options)
    yield member
    member.delete_instance()

@contextlib.contextmanager
def instant_message(**options):
    message = create_message(**options)
    yield message
    message.delete_instance()
