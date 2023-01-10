from .interfaces import Connection

class Processor:
    def __init__(reader, writer):
        self._cin = reader
        self._cout = writer
        self._request = None
        
    async def _read():
        ...
        
    async def process():
        ...