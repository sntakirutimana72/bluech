from asyncio import Lock, Queue, StreamReader, StreamWriter
from uuid import uuid4
from typing import Union, List, Dict, Any

from .serializers import json_parse

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
class Connection:
    def __init__(reader: StreamReader, writer: StreamWriter):
        self.uid = uuid4()
        self.reader = reader
        self.writer = writer
        
class RefUrl:
    def __init__(url_path):
        self.method, self.path = url_path.lsplit(':', 1)
        
    @property
    def full_path():
        return f'{self.method}:{self.path}'
        
class Request:
    def __init__(payload: Dict[str, Any]):
        url_path = payload.pop('route')
        self.ref_url = RefUrl(url_path)
        
        for name, value in payload.items():
            setattr(self, name, value)
        
    @property
    def as_json() -> Union[str, List[Any], Dict[str, Any]]:
        if self.content_type != 'json':
            return self.body
        return json_parse(self.body)
        
    @property
    def rel_path() -> str:
        return self.ref_url.path

class Queuable:
    def __init__(q: Queue = Queue(), lock: Lock = Lock()):
        self._q = q
        self._lock = lock
        
    async def pull():
        async with self._lock:
            if self._q.empty():
                return
            return self._q.get_nowait()
        
    async def push(data: Any):
        async with self._lock:
            self._q.put_nowait(data)
        
    async def clear():
        async with self._lock:
            for _ in self._q.qsize():
                self._q.get_nowait()
        