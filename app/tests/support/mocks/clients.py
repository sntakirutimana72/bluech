import asyncio as io

from ....utils.layers import PipeLayer
from ....settings import HOST_URL, HOST_PORT

class ClientMockSpec(object):
    _reader: io.StreamReader
    _writer: io.StreamWriter

    async def connect(self, host, port):
        reader, writer = await io.open_connection(host=host, port=port)
        self._reader = reader
        self._writer = writer

    async def disconnect(self):
        try:
            self._writer.close()
            await self._writer.wait_closed()
        except:
            ...

class AppClientSpec(ClientMockSpec):
    async def connect(self, host=HOST_URL, port=HOST_PORT):
        return await super().connect(host, port)

    async def send(self, request: dict):
        await PipeLayer.pump(self._writer, request)

    async def receive(self):
        incoming = await PipeLayer.fetch(self._reader)
        return incoming

class ConnectivityClientSpec(ClientMockSpec):
    async def connect(self, host='localhost', port=8080):
        return await super().connect(host, port)

    async def send(self, data: bytes):
        self._writer.write(data)
        await self._writer.drain()

    async def receive(self):
        data = await self._reader.read()
        return data
