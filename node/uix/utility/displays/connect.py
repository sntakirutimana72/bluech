from kivy.app import App
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from uix.utility.templates.layouts import BLayout
from uix.utility.templates.loading import Loading
from uix.utility.templates.headbars import HeadBarInterface
from uix.utility.templates.buttons import BTextInterface  # verified
from uix.utility.templates.textinputs import InputFieldInterface  # verified


Builder.load_string("""
<FieldSticker@Label>:
    font_size: f'{min(min(*self.size) // 2, 18)}dp'
    font_name: 'trebucbd'
    color: [.4, .4, 0, 1]
    text_size: self.size
    valign: 'middle'
    shorten: True

<ConnectTerminal>:
    pos_hint: {'center_x': .15, 'center_y': .15}
    orientation: 'vertical'
    size_hint: (None, None)
    size: ('70dp', '60dp')
    padding: '1sp'

    ConnectHBInterface:
    GLayout:
        cols: 1
        spacing: '15sp'
        padding: '20sp', '12sp'
        background_color: [0, 0, .03, 1]

        GridLayout:
            rows: 4
            padding: '25sp', 0

            FieldSticker:
                text: 'ENTER IP'
            FieldSticker:
                text: 'ENTER PORT'
            InputFieldInterface:
                id: ip
                placeholder: '- - - -'
            InputFieldInterface:
                id: port
                placeholder: '- - - -'

            FieldSticker:
                text: 'ENTER USERNAME'
            FieldSticker:
                text: 'ENTER PASSWORD'
            InputFieldInterface:
                id: username
                placeholder: '- - - - - - - -'
            InputFieldInterface:
                id: passphrase
                placeholder: '- - - - - - - -'

        BTextInterface:
            font_size: f'{min(min(*self.size) / 2, 12)}sp'
            background_color: [0, 0, 1, .1]
            on_press: root.connect_(*args)
            text: 'connect now'
            cover: [.2, 1, .2]
            size_hint_y: None
            height: '25dp'
""")


class ConnectTerminal(BLayout):
    background_color = [0, 0, 1, .2]
    launcher = ObjectProperty(None, allownone=True)

    def _repositioning(self, repos: bool, _forced: bool):
        if repos:
            reposition = Animation(
                size=(500, 250), d=.16,
                pos_hint={
                    'center_x': .5,
                    'center_y': .5
                }
            )
        else:
            reposition = Animation(
                size=(70, 60), d=.16,
                pos_hint={
                    'center_x': .15,
                    'center_y': .15
                }
            )
        if _forced:
            reposition.bind(on_complete=self._clear)
        else:
            reposition.bind(on_complete=self._ready)

        reposition.start(self)

    def _ready(self, animator: Animation, obj):
        self.disabled = not self.disabled

        if self.disabled:
            self.parent.remove_widget(self)

    def _clear(self, animator: Animation, obj):
        self.parent.remove_widget(self)
        self.reset()

    def on_parent(self, widget, parent):
        if parent:
            self._repositioning(True, False)

    def connect_(self, launcher):
        launcher.disabled = True

        # ********* validation block *********
        connect_address = (
            self.ids.ip.text_input.text,
            int(self.ids.port.text_input.text)
        )
        credentials = {
            'username': self.ids.username.text_input.text,
            'password': self.ids.passphrase.text_input.text
        }
        # ********************************************

        app = App.get_running_app()
        app.run_worker()

        self._repositioning(False, False)
        self.launcher.parent.add_widget(Loading(launcher=self))
        app.connect(connect_address, credentials)

    def on_close(self):
        self._repositioning(False, True)

    def reset(self):
        self.launcher.disabled = False
        self.launcher = None


class ConnectHBInterface(HeadBarInterface):
    title = 'Connect Terminal'
    background_color = [0, 0, .03, 1]

    def on_close(self):
        self.parent.on_close()
