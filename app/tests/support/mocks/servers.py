import asyncio as io

from ....utils.middlewares import accept_conn
from ....settings import HOST_URL, HOST_PORT

class MockServerSpec:
    _server: io.base_events.Server

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    def _console_debug(self):
        print()
        print('*' * 160)
        print(f'{self.__class__.__name__} server listening on {self._host}:{self._port}')
        print('*' * 160)

    def is_closed(self):
        return self._server.is_serving()

    async def terminate(self):
        try:
            self._server.close()
        except:
            ...
        finally:
            await self._server.wait_closed()

class AppServerSpec(MockServerSpec):
    def __init__(self, host=HOST_URL, port=HOST_PORT):
        super().__init__(host, port)

    async def initiate(self):
        self._server = await io.start_server(
            accept_conn, host=self._host, port=self._port
        )
        return self

class ConnectivityMockServer(MockServerSpec):
    def __init__(self, host='localhost', port=8080):
        super().__init__(host, port)
        self.con_counter = 0

    async def initiate(self):
        self._server = await io.start_server(
            self._on_connected, host=self._host, port=self._port
        )
        self._console_debug()

    async def _on_connected(self, _, writer):
        print('Client connected!')
        self.con_counter += 1
        await self._handshake(writer)

        # close pipeline
        writer.close()
        await writer.wait_closed()

    @staticmethod
    async def _handshake(writer):
        writer.write(b'helo')
        await writer.drain()
