import asyncio as io
import traceback as trc

from .layers import Response
from .repositories import RepositoriesHub as Hub
from .sql import UserQueryManager
from ..models import Message, User

class Filters:
    @staticmethod
    def other_participants(only: list):
        for channel in Hub.channels_repository:
            if channel.uid in only:
                yield channel

    @staticmethod
    def other_ids(only: list):
        return [p.uid for p in Hub.channels_repository if p.uid in only]

class Responder:
    @classmethod
    def get_handler(cls, name: str):
        return getattr(cls, name)

    @staticmethod
    async def signin(**options):
        async with Hub.channels_repository.mutex:
            ssid = options['id']
            if channel := Hub.channels_repository.items.get(ssid):
                if options['ids']:
                    users_query = UserQueryManager.all_users(ssid, options['ids'])
                    await channel.write(Response.all_users(users_query))

                    con_response = Response.connected(channel.resource)
                    for p_channel in Filters.other_participants(options['ids']):
                        await p_channel.write(con_response)

    @staticmethod
    async def signout(**options):
        async with Hub.channels_repository.mutex:
            discon_response = Response.disconnected(options['ssid'])
            for channel in Filters.other_participants(options['ids']):
                await channel.write(discon_response)

    @staticmethod
    async def edit_username(**options):
        async with Hub.channels_repository.mutex:
            if channel := Hub.channels_repository.items.get(options['id']):
                response = Response.edit_username_success(channel.resource)
                await channel.write(response)

    @staticmethod
    async def change_user_avatar(**options):
        async with Hub.channels_repository.mutex:
            if channel := Hub.channels_repository.items.get(options['id']):
                response = Response.change_user_avatar_success(channel.resource)
                await channel.write(response)

    @staticmethod
    async def new_message(**options):
        async with Hub.channels_repository.mutex:
            resource: Message = Message.get_by_id(options['id'])
            rec_id = resource.recipient.id

            if channel := Hub.channels_repository.items.get(rec_id):
                await channel.write(Response.new_message_success(resource))

    @staticmethod
    async def edit_message(**options):
        async with Hub.channels_repository.mutex:
            resource: Message = Message.get_by_id(options['id'])
            rec_id = resource.recipient.id

            if channel := Hub.channels_repository.items.get(rec_id):
                await channel.write(Response.edit_message_success(resource))

    @staticmethod
    async def remove_message(**options):
        async with Hub.channels_repository.mutex:
            msg_id = options['id']
            items = options['from_'], options['to_']

            for (i, j) in (items, items[::-1]):
                if channel := Hub.channels_repository.items.get(i):
                    res = User.get_by_id(j)
                    await channel.write(Response.remove_message_success(res, message_id=msg_id))

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
