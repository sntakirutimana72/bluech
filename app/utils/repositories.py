from functools import lru_cache
from asyncio import Queue, Lock
from typing import Any

from .db_connect import db_connector
from .layers import ChannelLayer

class Repository(object):

    def __init__(self, items: Queue | dict[str, Any]):
        self._items = items
        self._mutex = Lock()

    async def fetch(self, *args):
        raise NotImplemented

    async def push(self, data: ChannelLayer | Any):
        raise NotImplemented

    async def clear(self):
        raise NotImplemented

    @property
    def name(self):
        cls_name = self.__class__.__name__
        this_name = cls_name.rstrip('Repository')
        return this_name.lower()

class ChannelsRepository(Repository):

    async def fetch(self, channel_id):
        async with self._mutex:
            return self._items[channel_id]

    async def push(self, channel: ChannelLayer):
        async with self._mutex:
            self._items[channel.channel_id] = channel

    async def remove(self, channel_id):
        async with self._mutex:
            del self._items[channel_id]

    async def clear(self):
        async with self._mutex:
            self._items = {}

class TasksRepository(Repository):

    async def fetch(self):
        async with self._mutex:
            if self._items.empty():
                return
            return self._items.get_nowait()

    async def push(self, data: ChannelLayer | Any):
        async with self._mutex:
            self._items.put_nowait(data)

    async def clear(self):
        async with self._mutex:
            for _ in range(self._items.qsize()):
                self._items.get_nowait()

@lru_cache(typed=True)
def db_conn(env='development'):
    return db_connector(env)

@lru_cache
def channels_repository():
    return ChannelsRepository({})

@lru_cache
def tasks_repository():
    return TasksRepository(Queue())
