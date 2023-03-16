import asyncio as io
import typing as ty

from ..utils.interfaces import Request
from ..utils.layers import TasksLayer

class Base(object):
    def __init__(self, request: Request):
        self.request = request

    @property
    def user_id(self) -> int:
        return self.session.user_id

    @property
    def session(self):
        return self.request.session

    def get_handler(self) -> ty.Type[io.Future]:
        handler = f'_{self.request.method.lower()}'
        return getattr(self, handler)

    def exec(self):
        return self.get_handler()

    async def build_task(self, **kwargs):
        await TasksLayer.build(self.request.protocol, **kwargs)
