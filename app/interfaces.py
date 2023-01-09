from asyncio import Queue, Lock

class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
class Shareable:
    def __init__(q = Queue(), lock = Lock()):
        self._q = q
        self._lock = lock
        
    async def pull():
        async with self._lock:
            if self._q.empty():
                return
            return self._q.get_nowait()
        
    async def push(data):
        async with self._lock:
            self._q.put_nowait(data)
        
    async def clear():
        async with self._lock:
            for _ in self._q.qsize():
                self._q.get_nowait()
        