import asyncio

class AsyncioTestCase(object):
    def __init__():
        try:
            # initiate server instance
        except:
            # isolate errors that might occur during server intitiation
        else:
            # finally given no occurred, set our server variable with server instance to be used later in the application 
        
    def setUp():
        self._server = ... # start server connection here and bind it to port
        
    def teardown():
        if self._server:
            # kill server process if running