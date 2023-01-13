import asyncio

from ..utils.interfaces import Request

class Base(object):

    def __init__(self, request: Request):
        self._request = request

    def _executor(self):
        exec_name = f'_{self._request.method.lower()!r}'
        # Find a right handler based on the request method
        return getattr(self, exec_name)

    def exec(self) -> asyncio.Future:
        return self._executor()()
