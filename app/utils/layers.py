from .serializers import compress, decompress
from .repositories import RepositoriesHub
from .interfaces import AttributeDict
from ..models import *

class ChannelLayer:

    def __init__(self, writer, channel_id):
        self.channel_id = channel_id
        self.writer = writer

    @property
    def is_group(self):
        return self.writer is None

    @property
    def model(self):
        if self.writer:
            return User.get_by_id(self.channel_id)
        return Channel.get_by_id(self.channel_id)

class TasksLayer:

    @staticmethod
    def _new(proto, _id, **options):
        new_task = AttributeDict({**options, 'proto': proto, 'id': _id})
        return new_task

    @classmethod
    async def build(cls, proto, resource_id, **options):
        await RepositoriesHub.tasks_repository.push(cls._new(proto, resource_id, **options))

class Response:

    @staticmethod
    def _make(proto: str, **kwargs) -> bytes:
        return compress({'protocol': proto, **kwargs})

    # noinspection PyProtectedMember
    @classmethod
    def _as_resource(cls, proto: str, resource: _Model):
        return cls._make(proto, **{resource.name: resource.as_json()})

    @classmethod
    def as_exc(cls, message):
        return cls._make('exception', message=message)

    @classmethod
    def as_signin_success(cls, user):
        return cls._as_resource('signin_success', user)

    @classmethod
    def as_signin_failure(cls, message: str):
        return cls._make('signin_failure', message=message)

    @classmethod
    def as_signout_success(cls):
        return cls._make('signout_success')

    @classmethod
    def as_signout_failure(cls, message=''):
        return cls._make('signout_failure', message=message)

    @classmethod
    def as_message(cls, message):
        return cls._as_resource('message', message)

    @classmethod
    def as_message_edited(cls, message):
        return cls._as_resource('message_edited', message)

    @classmethod
    def as_my_nickname_changed(cls, user):
        return cls._as_resource('my_nickname_changed', user)

    @classmethod
    def as_nickname_changed(cls, resource):
        return cls._as_resource('nickname_changed', resource)

class PipeLayer:

    @staticmethod
    async def fetch(reader):
        data = await reader.read()
        return decompress(data)

    @staticmethod
    async def pump(writer, data):
        writer.write(compress(data))
        await writer.drain()
