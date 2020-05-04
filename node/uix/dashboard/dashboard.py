from os.path import join
from kivy.lang import Builder
from utils.helpers.envs import exec_dir
from utils.workers.updater import Updater
from uix.utility.templates.layouts import BLayout
from uix.utility.displays.connect import ConnectTerminal
from uix.utility.displays.rooms import ChatRoom  # verified
from uix.utility.displays.personnels import PersonnelRepos  # verified
from uix.utility.templates.headbars import HeadBarAppInterface  # verified


Builder.load_file(join(exec_dir(), 'uix', 'dashboard', 'dashboard.kv'))


class Dashboard(BLayout):
    background_color = [0, 0, 1, .4]

    def to_whom(self):
        return self.ids.repos.to_whom()

    def __init__(self, **kwargs):
        self.register_event_type('on_update')
        self.register_event_type('on_connect')
        super(Dashboard, self).__init__(**kwargs)
        self._updater = None

    def what_room(self, room: str):
        if room == '@':
            return self.ids.all_.what_room(f'@@All Members')
        return self.ids.direct.what_room(room)

    def which_room(self, personnel):
        self.what_room(personnel.text)

    def on_update(self, update: bytes):
        if self._updater is None:
            self._updater = Updater(benefactor=self)
            self._updater.run()

        loop = None
        while not loop:
            loop = self._updater.loop
        loop.call_soon_threadsafe(self._updater.submit, update)

    def on_connect(self, status: bool):
        notifier = self.ids.head.get_notifier()

        if status:
            notifier.children[0].terminate()
            self.ids.head.get_connectors('connect').deactivate()
            self.ids.head.get_connectors('disconnect').activate()
            return
        notifier.children[0].relaunch()

    def disconnect(self, instance):
        # instance.deactivate()
        # self.ids.head.get_connectors('connect').activate()
        pass

    def open_connectTerminal(self, launcher):
        self.parent.add_widget(
            ConnectTerminal(launcher=launcher, disabled=True)
        )
