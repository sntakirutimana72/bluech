import asyncio as io
import typing as yi

from .serializers import PayloadJSONSerializer
from .repositories import RepositoriesHub
from .interfaces import AttributeDict
from ..models import *

class ChannelLayer:
    def __init__(self, writer: io.StreamWriter, _id):
        self._id = _id
        self._writer = writer

    @property
    def uid(self) -> int | str:
        return self._id

    @property
    def is_writable(self):
        return self._writer is None

    @property
    def resource(self) -> User | Channel:
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
    def make(proto: str, status=200, **kwargs):
        return {'proto': proto, 'status': status, **kwargs}

    # noinspection PyProtectedMember
    @classmethod
    def _as_resource(cls, proto: str, resource: _Model):
        return cls.make(proto, **{resource.name: resource.as_json()})

    @classmethod
    def exception(cls, message='Internal Error', status=500):
        return cls.make('error', status=status, message=message)

    @classmethod
    def signin_success(cls, user):
        return cls._as_resource('signin_success', user)

    @classmethod
    def signin_failure(cls, message: str, status=401):
        return cls.make('signin_failure', status=status, message=message)

    @classmethod
    def as_signout_success(cls):
        return cls.make('signout_success')

    @classmethod
    def as_signout_failure(cls, message=''):
        return cls.make('signout_failure', message=message)

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
    async def fetch(reader: io.StreamReader):
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
    async def pump(writer: io.StreamWriter, raw_payload: dict[str, yi.Any]):
        packed_payload = PayloadJSONSerializer.compress(raw_payload)
        writer.write(packed_payload)
        await writer.drain()
