class Base(object):
    def __init__(reader, db):
        self._reader = reader
        self._db = db
        
        self._queries = None
        self._request = None
        self._route_name = None
        
    async def _read():
        ...
        
    async def process():
        ...
