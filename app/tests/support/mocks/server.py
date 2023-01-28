import asyncio

class ConnectivityMockServer:
    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port
        self._con_counter = 0
        self._server = None

    async def initiate(self):
        self._server = await asyncio.start_server(
            self._on_connected, host=self._host, port=self._port
        )
        print(f'Server started..on {self._host}:{self._port}')

    async def _on_connected(self, _, writer):
        print('Client connected!')
        self._con_counter += 1
        await self._handshake(writer)

        # close pipeline
        writer.close()
        await writer.wait_closed()

    @staticmethod
    async def _handshake(writer):
        writer.write(b'helo')
        await writer.drain()
