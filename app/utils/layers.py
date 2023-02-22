import asyncio as io
import typing as yi

from .repositories import RepositoriesHub
from .interfaces import AttributeDict
from .exceptions import CustomException
from ..serializers.commons import PayloadJSONSerializer
from ..serializers.models import UserSerializer
from ..models import *

class ChannelLayer:
    def __init__(self, writer: io.StreamWriter, uid: int | str):
        self.uid = uid
        self.writer = writer

    @property
    def is_writable(self):
        return self.writer is None

    @property
    def resource(self) -> User | Channel:
        if self.is_writable:
            return User.get_by_id(self.uid)
        return Channel.get_by_id(self.uid)

    async def write(self, payload: dict[str, yi.Any]):
        if not self.is_writable:
            raise
        await PipeLayer.pump(self.writer, payload)

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
    def make(status=200, **kwargs):
        return {'status': status, **kwargs}

    @classmethod
    def internal_error(cls, **options):
        if not options:
            options = CustomException().to_json
        return cls.make(**options)

    @classmethod
    def signin_success(cls, user):
        return cls.make(user=UserSerializer(user).to_json, proto='signin_success')

    @classmethod
    def signout_success(cls):
        return cls.make(proto='signout_success')

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
