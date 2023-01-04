import asyncio

class AsyncServerMock(object):
    def __init__(ip = 'localhost', port = 8080):
        self._address = ip, port
        self._mock_server = None
        self._thread = None
        
    def setup():
        # start server connection here and bind it to port
        
    def teardown():
        if self._server:
            # kill server process if running
            
    @property
    def server():
        return self._mock_server