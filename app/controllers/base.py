import asyncio

from ..utils.interfaces import Request

class Base(object):
    def __init__(self, request: Request):
        self._request = request
        
    @property
    def user_id(self) -> int:
        return self.session.user_id
    
    @property
    def session(self):
        return self._request.session

    def _executor(self):
        exec_name = f'_{self._request.method.lower()!r}'
        return getattr(self, exec_name)

    def exec(self) -> asyncio.Future:
        return self._executor()()
