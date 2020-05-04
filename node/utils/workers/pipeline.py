import asyncio
from threading import Thread
from utils.auth import sys_, ssl_
from kivy.clock import mainthread
from kivy.event import EventDispatcher
from utils.loggers.ilogger import logging
from utils.helpers.skt_connect import cliconnect
from utils.helpers.formatters import payloader, reader, writer


class Pipeline(EventDispatcher):

    __events__ = (
        'on_update',    # trigger for updates like messages & users
        'on_connect',  # triggered when connected and cleared by server
    )

    async def _submit(self, message: dict):
        await self._outs.put(payloader(message))
        self._write_pulse()

    async def _connecting(self, *largs):
        if not (self._connecting_ or self._node):
            self._connecting_ = True

            skt_client = cliconnect(largs[0])
            isAccepted = None

            if skt_client:
                authenticating = self.loop.create_task(sys_.authenticate(skt_client, largs[1]))
                await authenticating

                isAccepted = authenticating.result()
                if isAccepted:
                    self._node = skt_client
                    self._read_pulse()

            @mainthread
            def notify():
                self.dispatch('on_connect', isAccepted)

            notify()

        self._connecting_ = None

    def submit(self, message: dict):
        self.loop.create_task(self._submit(message))

    async def run_pulse(self):
        while True:
            await asyncio.sleep(5)

    def connect(self, *largs):
        self.loop.create_task(self._connecting(*largs))

    def on_connect(self, *_):
        pass

    async def _writer(self):
        while not self._outs.empty():
            try:
                message = await self._outs.get()
                await writer(self._node, message)
            except Exception as e:
                pass

            await asyncio.sleep(.2)

    async def _reader(self):
        try:
            message = await reader(self._node)

            @mainthread
            def notify():
                self.dispatch('on_update', message)

            notify()
        except Exception as e:
            logging(e)

        self.loop.call_later(1, self._read_pulse)

    def on_update(self, *_):
        pass

    def _write_pulse(self):
        if self._pulse is None or self._pulse.done():
            self._pulse = self.loop.create_task(self._writer())

    def _run_forever(self):
        self.loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self.run_pulse())
        self.loop.run_forever()

    def _read_pulse(self):
        self.loop.create_task(self._reader())

    def __init__(self):
        super().__init__()
        self._thread_ = Thread(target=self._run_forever)
        self._thread_.daemon = True
        self._outs = asyncio.Queue()
        self._node = self._pulse = None
        self._connecting_ = self.loop = None

    def run(self):
        self._thread_.start()
