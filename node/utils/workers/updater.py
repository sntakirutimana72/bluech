import asyncio
from threading import Thread
from kivy.clock import mainthread
from kivy.event import EventDispatcher
from utils.helpers.formatters import decompress
from uix.utility.displays.message import MessageUI
from uix.utility.templates.buttons import BTextInterface


class Updater(EventDispatcher):

    async def _update(self, update: bytes):
        async with asyncio.Lock():
            await self._updates.put(update)
        await asyncio.sleep(.5)

    def submit(self, update: bytes):
        self.loop.create_task(self._update(update))

    def __init__(self, benefactor):
        super().__init__()
        self._thread_ = Thread(target=self._run_forever)
        self._benefactor = benefactor
        self._thread_.daemon = True

        self._pulse = self.loop = None
        self._updates = asyncio.Queue()

    async def _populate(self):
        while True:
            if not self._updates.empty():
                update = await self._updates.get()
                what_, update = await decompress(update)

                if what_ == 'message':

                    @mainthread
                    def populate():
                        self._benefactor.what_room(
                            update['to_']).add_widget(MessageUI(content=update, halign='left')
                        )
                    populate()

                elif what_ == 'user':

                    @mainthread
                    def populate_(username: str):
                        if self._benefactor.ids.all_.active_room == '@@default Room':
                            self._benefactor.ids.all_.rename('@@All Members')

                        personnel_ui = BTextInterface(
                            text=username, size_hint_y=None, height='24dp',
                            color=[1, 1, 1, 1], background_color=[0, 0, 1, .07],
                            text_size=True, font_size='10sp', shadow='2sp'

                        )
                        personnel_ui.bind(on_press=self._benefactor.which_room)
                        self._benefactor.to_whom().add_widget(personnel_ui)

                    for user in update:
                        populate_(f'@{user}')

                await asyncio.sleep(.2)
            else:
                await asyncio.sleep(1)

    def _run_forever(self):
        self.loop = asyncio.get_event_loop_policy().new_event_loop()
        asyncio.set_event_loop(self.loop)
        self._pulse = self.loop.create_task(self._populate())
        self.loop.run_forever()

    def run(self):
        self._thread_.start()
