from asyncio import Lock, Queue, StreamReader, StreamWriter
from uuid import uuid4
from typing import Union, List, Dict, Any

from .serializers import json_parse

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Connection:
    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.uid = uuid4()
        self.reader = reader
        self.writer = writer

class RefUrl:
    def __init__(self, url_path):
        self.method, self.path = url_path.lsplit(':', 1)

    @property
    def full_path(self):
        return f'{self.method}:{self.path}'

class Request:
    def __init__(self, payload: Dict[str, Any]):
        self.ref_url = RefUrl(payload.route)
        self.content_type = payload.content_type
        self.content_length = payload.content_length
        self.body = payload.body

    @property
    def as_json(self) -> Union[str, List[Any], Dict[str, Any]]:
        if self.content_type != 'json':
            return self.body
        return json_parse(self.body)

    @property
    def rel_path(self) -> str:
        return self.ref_url.path

class Queuable:
    def __init__(self, q: Queue = Queue(), lock: Lock = Lock()):
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
