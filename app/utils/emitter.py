import asyncio as io
import traceback as trc

from .layers import Response, ChannelLayer
from .repositories import RepositoriesHub as Hub
from ..models import Message, User

class Filters:
    @staticmethod
    def other_participants(except_recently):
        for channel in Hub.channels_repository:
            if channel.is_writable and channel.uid != except_recently:
                yield channel

class Responder:
    @classmethod
    def get_handler(cls, name: str):
        return getattr(cls, name)

    @staticmethod
    async def connected(**options):
        ...

    @staticmethod
    async def disconnected(**options):
        ...

    @staticmethod
    async def edit_username(**options):
        async with Hub.tasks_repository.mutex:
            async with Hub.channels_repository.mutex:
                channel: ChannelLayer | None = Hub.channels_repository.items.get(options['id'])
                if channel is None:
                    return
                response = Response.edit_username_success(channel.resource)
        await channel.write(response)

    @staticmethod
    async def change_user_avatar(**options):
        async with Hub.tasks_repository.mutex:
            async with Hub.channels_repository.mutex:
                channel: ChannelLayer | None = Hub.channels_repository.items.get(options['id'])
                if channel is None:
                    return
                response = Response.change_user_avatar_success(channel.resource)
        await channel.write(response)

    @staticmethod
    async def new_message(**options):
        async with Hub.channels_repository.mutex:
            resource: Message = Message.get_by_id(options['id'])
            rec_id = resource.recipient.id
            channel: ChannelLayer | None = Hub.channels_repository.items.get(rec_id)
            if channel is None:
                return
            response = Response.new_message_success(resource)
        await channel.write(response)

    @staticmethod
    async def edit_message(**options):
        async with Hub.channels_repository.mutex:
            resource: Message = Message.get_by_id(options['id'])
            rec_id = resource.recipient.id
            channel: ChannelLayer | None = Hub.channels_repository.items.get(rec_id)
            if channel is None:
                return
            response = Response.edit_message_success(resource)
        await channel.write(response)

    @staticmethod
    async def remove_message(**options):
        async with Hub.channels_repository.mutex:
            msg_id = options['id']
            items = options['from_'], options['to_']
            for (i, j) in (items, items[::-1]):
                channel: ChannelLayer | None = Hub.channels_repository.items.get(i)
                if channel:
                    resource = User.get_by_id(j)
                    response = Response.remove_message_success(resource, message_id=msg_id)
                    await channel.write(response)

    @classmethod
    async def pulse(cls):
        while 1:
            try:
                task = await Hub.tasks_repository.fetch()
                if task:
                    proto = task.pop('proto')
                    handler = cls.get_handler(proto)
                    await handler(**task)
            except:
                print(trc.print_exc())
            await io.sleep(1.25)
