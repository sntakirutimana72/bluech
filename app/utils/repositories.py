from functools import lru_cache
from asyncio import Queue, Lock
from typing import Any

from .db_connect import db_connector

class Repository(object):
    def __init__(self, items: Queue | dict[str, Any]):
        self._items = items
        self._mutex = Lock()

class ChannelsRepository(Repository):
    async def fetch(self, _id):
        async with self._mutex:
            return self._items[_id]

    async def push(self, channel):
        async with self._mutex:
            self._items[channel.uid] = channel

    async def remove(self, _id):
        async with self._mutex:
            del self._items[_id]

    async def clear(self):
        async with self._mutex:
            self._items = {}

class TasksRepository(Repository):
    async def fetch(self):
        async with self._mutex:
            if self._items.empty():
                return
            return self._items.get_nowait()

    async def push(self, data):
        async with self._mutex:
            self._items.put_nowait(data)

    async def clear(self):
        async with self._mutex:
            for _ in range(self._items.qsize()):
                self._items.get_nowait()

class RepositoriesHub:
    tasks_repository = lru_cache(maxsize=None)(lambda: TasksRepository(Queue()))()
    channels_repository = lru_cache(maxsize=None)(lambda: ChannelsRepository({}))()

@lru_cache(typed=True)
def db_conn(env='development'):
    return db_connector(env)
