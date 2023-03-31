import asyncio as io

from ....utils.middlewares import accept_conn
from ....utils.emitter import Responder
from ....settings import HOST_URL, HOST_PORT

class MockServerSpec:
    _server: io.base_events.Server
    _pulse: io.Task

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

    async def stop_pulse(self):
        try:
            self._pulse.cancel()
            await self._pulse
        except:
            ...

    async def stop_server(self):
        try:
            self._server.close()
            await self._server.wait_closed()
        except:
            ...

    async def terminate(self):
        await self.stop_pulse()
        await self.stop_server()

class AppServerSpec(MockServerSpec):
    def __init__(self, host=HOST_URL, port=HOST_PORT):
        super().__init__(host, port)

    async def initiate(self):
        self._server = await io.start_server(
            accept_conn, host=self._host, port=self._port
        )
        self._pulse = io.create_task(Responder.pulse())
        return self
