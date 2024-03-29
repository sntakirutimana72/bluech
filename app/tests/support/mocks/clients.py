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

    async def disconnect(self):
        await self.logout()
        await super().disconnect()

    async def login(self, **credentials):
        await self.connect()
        await self.send(RequestSpecs.signin(**credentials))
        return await self.receive()

    async def logout(self):
        await self.send(RequestSpecs.signout())
        return await self.receive()

    async def edit_username(self, **options):
        await self.send({**RequestSpecs.edit_username(**options)})
        return await self.receive()

    async def change_user_avatar(self, **options):
        content: bytes = options.pop('content')
        await self.send({**RequestSpecs.change_user_avatar(), **options})
        self.writer.write(content)
        await self.writer.drain()
        return await self.receive()

    async def post_message(self, params_sid, **kwargs):
        await self.send(getattr(RequestSpecs, params_sid)(**kwargs))

    async def get_all_messages(self, recipient: int, page=1):
        await self.send(RequestSpecs.all_messages(recipient, page))
        return await self.receive()
