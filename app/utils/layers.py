import asyncio as io
import typing as yi
import pathlib as plib
import aiofiles as aio
import aiofiles.os as aios

from .repositories import RepositoriesHub
from .interfaces import AttributeDict
from .exceptions import CustomException
from ..serializers.commons import PayloadJSONSerializer
from ..serializers.models import *
from ..settings import AVATARS_PATH
from ..models import *

class ChannelLayer:
    def __init__(self, writer: io.StreamWriter, uid: int | str):
        self.uid = uid
        self.writer = writer

    @property
    def resource(self) -> User:
        return User.get_by_id(self.uid)

    async def write(self, payload: dict[str, yi.Any]):
        await PipeLayer.pump(self.writer, payload)

class TasksLayer:
    @staticmethod
    def new(proto, _id, **options):
        new_task = AttributeDict({**options, 'proto': proto, 'id': _id})
        return new_task

    @classmethod
    async def build(cls, proto, resource_id=None, **options):
        await RepositoriesHub.tasks_repository.push(cls.new(proto, resource_id, **options))

class Response:
    @staticmethod
    def make(status=200, **kwargs) -> dict[str, yi.Any]:
        return {'status': status, **kwargs}

    @classmethod
    def internal_error(cls, **options):
        if not options:
            options = CustomException().to_json
        return cls.make(**options)

    @classmethod
    def respond_with_user_serializer(cls, user: User, **kwargs):
        return cls.make(user=UserSerializer(user).to_json, **kwargs)

    @classmethod
    def new_message_success(cls, message):
        return cls.make(message=MessageSerializer(message).to_json, proto='new_message')

    @classmethod
    def edit_message_success(cls, message):
        return cls.make(message=MessageSerializer(message).to_json, proto='edit_message')

    @classmethod
    def remove_message_success(cls, user, **kwargs):
        return cls.make(proto='remove_message', benefactor=UserSerializer(user).to_json, **kwargs)

    @classmethod
    def all_messages(cls, query, current_user):
        return cls.make(
            messages=MessageListQuerySerializer(query, current_user=current_user).to_json,
            proto='all_messages'
        )

    @classmethod
    def signin_success(cls, user):
        return cls.respond_with_user_serializer(user, proto='signin_success')

    @classmethod
    def signout_success(cls):
        return cls.make(proto='signout_success')

    @classmethod
    def edit_username_success(cls, user):
        return cls.respond_with_user_serializer(user, proto='edit_username_success')

    @classmethod
    def change_user_avatar_success(cls, user):
        return cls.respond_with_user_serializer(user, proto='change_avatar_success')

    @classmethod
    def connected(cls, user):
        return cls.respond_with_user_serializer(user, proto='connected')

    @classmethod
    def disconnected(cls, user_id):
        return cls.make(ssid=user_id, proto='disconnected')

    @classmethod
    def all_users(cls, query):
        return cls.make(users=UserListQuerySerializer(query).to_json, proto='all_users')

class PipeLayer:
    @staticmethod
    def get_download_path(parent_dir: plib.Path, filename: str):
        complete_path = parent_dir / filename
        is_overwrite = complete_path.exists()
        if is_overwrite:
            current_stem = complete_path.stem
            complete_path = complete_path.with_stem(f'{current_stem}.copy')
        return complete_path, complete_path.exists()

    @staticmethod
    def get_filename(stem: str, content_type: str):
        suffix = content_type.split('/')[1].lower()
        return f'{stem}.{suffix}'

    @staticmethod
    def download_buffer(overall_size: int, buffer=1024):
        return overall_size if overall_size < buffer else buffer

    @classmethod
    async def download(cls, pipe: io.StreamReader, **kwargs):
        content_size: int = kwargs.pop('content_length')
        remaining_content_size = content_size
        buffer_size = cls.download_buffer(content_size)
        download_path, is_overwrite = cls.get_download_path(**kwargs)
        try:
            async with aio.open(download_path, 'wb') as pointer:
                while remaining_content_size > 0:
                    chunk = await pipe.read(buffer_size)
                    await pointer.write(chunk)
                    remaining_content_size -= buffer_size
                    if buffer_size > remaining_content_size:
                        buffer_size = remaining_content_size
        except:
            if is_overwrite and download_path.exists():
                await aios.remove(download_path)
        else:
            if is_overwrite:
                original_stem = download_path.stem.rstrip('.copy')
                actual_path = download_path.with_stem(original_stem)
                await aios.remove(actual_path)  # remove pre-existing first
                await aios.rename(download_path, actual_path)  # rename the copy as the original

    @classmethod
    async def download_avatar(cls, pipe: io.StreamReader, **kwargs):
        content_type = kwargs.pop('content_type')
        current_user = kwargs.pop('current_user')
        kwargs['filename'] = cls.get_filename(f'avatar_{current_user}', content_type)
        done = await cls.download(pipe, parent_dir=AVATARS_PATH, **kwargs)
        return done

    @staticmethod
    async def fetch(reader: io.StreamReader):
        content_size = await reader.read(4)
        buffer_size = 1024
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
