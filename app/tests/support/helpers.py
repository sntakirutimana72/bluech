import contextlib

from .declarations import Models
from ...models import User, Channel, Member

def create_user(**options) -> User:
    user = User.create(**Models.user(**options))
    return user

def create_channel(**options) -> Channel:
    channel =  Channel.create(**Models.channel(**options))
    return channel

def create_member(**options):
    return Member.create(**options)

@contextlib.contextmanager
def instant_member(**options):
    member = create_member(**options)
    yield member
    member.delete_instance()
