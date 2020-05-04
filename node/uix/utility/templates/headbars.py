from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from uix.utility.templates.layouts import BLayout
from uix.utility.templates.behaviors import Dragging, Hovering
from uix.utility.templates.buttons import BTextInterface  # verified
from kivy.properties import NumericProperty, StringProperty, ListProperty, OptionProperty


Builder.load_string("""
<TitleInterface>:
    shorten: True
    valign: 'middle'
    font_size: '11sp'
    padding: ('5sp', 0)
    text_size: self.size
    font_name: 'Roboto-Bold'

<InterfaceControls>:
    size_hint_x: None
    padding: 0, '3sp'
    spacing: '2sp'
    width: '70dp'

    HBMinimizeInterface:
        id: minimize
        on_release: root.on_minimize()
        toggle_graffiti: root.toggle_graffiti if not self.disabled else .1
    HBResizeInterface:
        id: resize
        on_release: root.on_resize()
        toggle_graffiti: root.toggle_graffiti if not self.disabled else .1
    HBCloseInterface:
        id: close
        on_release: root.on_close()
        toggle_graffiti: root.toggle_graffiti

<HeadBarInterface>:
    padding: '5sp', 0
    size_hint_y: None
    height: dp(28)

    # Title-part
    TitleInterface:
        size_hint_x: .5
        text: root.title
        color: root.title_color

    # Function Controls Container
    OtherControls:
        id: other_controls

    # Button Controls Container
    InterfaceControls:
        id: header_controls
        disable_controls: root.disable_controls
""")


class TitleInterface(Label):
    pass


class OtherControls(BLayout):
    pass


class InterfaceControls(BoxLayout, Hovering):
    toggle_graffiti = NumericProperty(.5)
    disable_controls = OptionProperty('', options=['', '&ri', '&mi', 'mi&ri'])

    def on_hover(self):
        self.toggle_graffiti = 1

    def on_leave(self):
        self.toggle_graffiti = .5

    def on_close(self):
        self.parent.dispatch('on_close')

    def on_resize(self):
        self.parent.dispatch('on_resize')

    def on_minimize(self):
        self.parent.dispatch('on_minimize')

    def on_disable_controls(self, interface, disabler):
        if disabler in ['&ri', 'mi&ri']:
            self.ids.resize.disabled = True
        elif disabler in ['&mi', 'mi&ri']:
            self.ids.minimize.disabled = True


class HeadBarInterface(BLayout, Dragging):
    logo_name = StringProperty('')
    title = StringProperty('SYAI BChatter')
    title_color = ListProperty([1, 1, 1, 1])
    background_color = ListProperty([0, 0, .1, 1])
    disable_controls = OptionProperty('', options=['', '&ri', '&mi', 'mi&ri'])

    def __init__(self, **kwargs):
        self.register_event_type('on_close')
        self.register_event_type('on_resize')
        self.register_event_type('on_minimize')
        super(HeadBarInterface, self).__init__(**kwargs)

    def on_close(self):
        pass

    def on_resize(self):
        pass

    def on_minimize(self):
        pass


class HeadBarAppInterface(HeadBarInterface):
    draggable_obj = 'app'

    def __init__(self, **kwargs):
        super(HeadBarAppInterface, self).__init__(**kwargs)
        self._runner = Clock.schedule_interval(self._add_controls, .2)

    def _add_controls(self, frame: float):
        if self.ids:
            self._runner.cancel()
            self._runner = None
            app_root = App.get_running_app().root

            class ConnectInterface(BTextInterface):

                def activate(self):
                    self.cover = [.1, .6, .1]
                    self.bind(on_press=app_root.open_connectTerminal)

                def deactivate(self):
                    self.cover = [0, 0, .15]
                    self.unbind(on_press=app_root.open_connectTerminal)

            class DisconnectInterface(BTextInterface):

                def activate(self):
                    self.cover = [1, .2, .2]
                    self.bind(on_press=app_root.disconnect)

                def deactivate(self):
                    self.cover = [.2, .1, .1]
                    self.unbind(on_press=app_root.disconnect)

            connect_interface = ConnectInterface(
                size_hint_x=None, width='70dp', background_color=[0, 0, 0, 0],
                shadow='2sp', text='connect', font_size='10.5sp'
            )
            disconnect_interface = DisconnectInterface(
                size_hint_x=None, width='80dp', background_color=[0, 0, 0, 0],
                shadow='2sp', text='disconnect', font_size='10.5sp'
            )
            other_controls = self.ids.other_controls
            self.ids.update({
                'connect': connect_interface,
                'disconnect': disconnect_interface
            })
            connect_interface.activate()

            other_controls.spacing = '10sp'
            other_controls.padding = ['10sp', '3sp']
            other_controls.add_widget(connect_interface)
            other_controls.add_widget(disconnect_interface)

    def get_connectors(self, name: str):
        return self.ids[name]

    def get_notifier(self):
        return self.ids.other_controls

    def on_minimize(self):
        # application minimizing method
        App.get_running_app().root_window.minimize()

    def on_resize(self):
        # application resizing method
        pass

    def on_close(self):
        # application closing method
        App.stop(App.get_running_app())
