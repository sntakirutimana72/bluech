import asyncio as io

from .layers import Response, ChannelLayer
from .repositories import RepositoriesHub as Hub

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
    async def edit_username_success(**options):
        async with Hub.tasks_repository.mutex:
            async with Hub.channels_repository.mutex:
                channel: ChannelLayer = Hub.channels_repository.items.get(options['id'])
                if channel is None:
                    return
                response = Response.edit_username_success(channel.resource)
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
                ...
            await io.sleep(1.25)
