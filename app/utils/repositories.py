from functools import lru_cache
from asyncio import Queue, Lock
from typing import Any

from .db_connect import db_connector

class Repository(object):
    def __init__(self, items: Queue | dict[str, Any]):
        self.items = items
        self.mutex = Lock()

class ChannelsRepository(Repository):
    def __iter__(self):
        yield from self.items.values()

    async def fetch(self, _id):
        async with self.mutex:
            return self.items[_id]

    async def push(self, channel):
        async with self.mutex:
            self.items[channel.uid] = channel

    async def remove(self, _id):
        async with self.mutex:
            del self.items[_id]

    async def clear(self):
        async with self.mutex:
            self.items = {}

class TasksRepository(Repository):
    async def fetch(self) -> dict | None:
        async with self.mutex:
            if self.items.empty():
                return
            return self.items.get_nowait()

    async def push(self, data):
        async with self.mutex:
            self.items.put_nowait(data)

    async def clear(self):
        async with self.mutex:
            for _ in range(self.items.qsize()):
                self.items.get_nowait()

class RepositoriesHub:
    tasks_repository = lru_cache(maxsize=None)(lambda: TasksRepository(Queue()))()
    channels_repository = lru_cache(maxsize=None)(lambda: ChannelsRepository({}))()

@lru_cache(typed=True)
def db_conn(env='development'):
    return db_connector(env)
