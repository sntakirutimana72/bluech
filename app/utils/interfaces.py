from asyncio import Lock, Queue
from uuid import uuid4
from typing import Union, List, Dict, Any

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class RouteRef:

    def __init__(self, route_path):
        self.method, self.path = route_path.lsplit(':', 1)

    @property
    def full_path(self):
        return f'{self.method}:{self.path}'

class Request:

    def __init__(self, req: Dict[str, Any]):
        self.route_ref = RouteRef(req.pop('protocol'))
        
        for name, value in req.items():
            setattr(self, name, value)

    @property
    def route_path(self) -> str:
        return self.route_ref.path
        
    @property
    def method(self) -> str:
        return self.route_ref.method
        
    @property
    def full_path(self) -> str:
        return self.route_ref.full_path

class Queuable:

    def __init__(self, q = Queue(), lock: Lock = Lock()):
        self._q = q
        self._lock = lock

    async def pull(self):
        async with self._lock:
            if self._q.empty():
                return
            return self._q.get_nowait()

    async def push(self, data: Any):
        async with self._lock:
            self._q.put_nowait(data)

    async def clear(self):
        async with self._lock:
            for _ in range(self._q.qsize()):
                self._q.get_nowait()
                
class ChannelsQ:

    def __init__(self, q = {}, lock: Lock = Lock()):
        self._q = q
        self._lock = lock
        
    async def push(self, channel):
        async with self._lock:
            self._q[channel.channel_id] = channel

    async def remove(self, channel_id):
        async with self._lock:
            del self._q[channel_id]

    async def clear(self):
        async with self._lock:
            self._q = {}
