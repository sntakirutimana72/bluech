import asyncio

from ..utils.interfaces import Request

class Base(object):

    def __init__(self, request: Request, *options):
        self._request = request
        self._options = options
        # Compose the handler name based on the request
        method = self._request.ref_url.method
        coro_name = f'_{method.lower()!r}'
        # Assert existence of the request handler based on the request method
        if hasattr(self, coro_name):
            coro_name = '_not_found'  # default for all routes without handlers
        # Find a right handler based on the request method
        coro = getattr(self, coro_name)
        # Create a task in which the coro handler is called
        asyncio.create_task(coro())
