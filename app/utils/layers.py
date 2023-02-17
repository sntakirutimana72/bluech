from .serializers import PayloadJSONSerializer
from .repositories import RepositoriesHub
from .interfaces import AttributeDict
from ..models import *

class ChannelLayer:
    def __init__(self, writer, _id):
        self._id = _id
        self._writer = writer

    @property
    def uid(self):
        return self._id

    @property
    def is_writable(self):
        return self._writer is None

    @property
    def resource(self):
        if self.is_writable:
            return User.get_by_id(self._id)
        return Channel.get_by_id(self._id)

    async def write(self, payload: bytes):
        if not self.is_writable:
            raise
        self._writer.write(payload)
        await self._writer.drain()

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
        return PayloadJSONSerializer.compress({'protocol': proto, **kwargs})

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
        content_size = await reader.read(4)
        buffer_size = 1028
        content_size = int(content_size.decode())

        if content_size < buffer_size:
            buffer_size = content_size

        content = b''

        while content_size > 0:
            chunk = await reader.read(buffer_size)
            content += chunk
            content_size -= buffer_size

            if buffer_size > content_size > 0:
                buffer_size = content_size

        return PayloadJSONSerializer.decompress(content)

    @staticmethod
    async def pump(writer, raw_payload: dict):
        packed_payload = PayloadJSONSerializer.compress(raw_payload)
        writer.write(packed_payload)
        await writer.drain()
