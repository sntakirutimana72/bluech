import asyncio as io

from ..declarations import RequestSpecs
from ....utils.layers import PipeLayer
from ....settings import HOST_URL, HOST_PORT

class ClientMockSpec(object):
    reader: io.StreamReader
    writer: io.StreamWriter
    connected: bool = False

    async def connect(self, host=HOST_URL, port=HOST_PORT):
        if not self.connected:
            reader, writer = await io.open_connection(host=host, port=port)
            self.reader = reader
            self.writer = writer
            self.connected = True
        return self

    async def disconnect(self):
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except:
            ...
        self.connected = False

    async def send(self, request: dict):
        raise NotImplementedError

    async def receive(self):
        raise NotImplementedError

class AppClientSpec(ClientMockSpec):
    async def send(self, request: dict):
        await PipeLayer.pump(self.writer, request)

    async def receive(self):
        incoming = await PipeLayer.fetch(self.reader)
        return incoming

    async def login(self, **credentials):
        await self.connect()
        await self.send(RequestSpecs.signin(**credentials))
        return await self.receive()

    async def logout(self):
        await self.send(RequestSpecs.signout())
        return await self.receive()

class ConnectivityClientSpec(ClientMockSpec):
    async def connect(self, host='localhost', port=8080):
        return await super().connect(host, port)

    async def send(self, data: bytes):
        self.writer.write(data)
        await self.writer.drain()

    async def receive(self):
        data = await self.reader.read()
        return data
