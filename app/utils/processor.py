from .interfaces import Connection
from .dispatch import dispatch
from .pipe import fetch

class Processor:
    def __init__(reader, writer):
        self._reader = reader
        self._writer = writer
        self._request = None
        
        asyncio.create_task(self._service())
        
    async def _service():
        # new connection is still in transit and haven't been cleared to operate
        try:
            payload = await fetch(self._reader)
            self._process_request(payload)
        except:
            ...
        
    def _process_request(payload):
        ...