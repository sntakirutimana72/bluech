from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from uix.utility.templates.layouts import BLayout
from uix.utility.templates.behaviors import Clicking
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty, ObjectProperty


Builder.load_string("""
<TogglePassword>:
    canvas:
        Color:
            rgba: [1, 1, 1, int(not self.disabled)]
        Rectangle:
            pos: [self.x + dp(self.pace), self.y + dp(self.pace)]
            size: [self.width - dp(self.pace * 2), \
                self.height - dp(self.pace * 2)]
    size_hint_x: None
    width: self.height

<InputInterface>:
    background_color: [0, 0, 0, 0]

<InputFieldInterface>:
    text_input: text_input.__self__
    size_hint_y: None
    padding: '1sp'
    height: '32dp'

    BLayout:
        padding: ('10sp', 0)
        background_color: root.foreground_color
        InputInterface:
            id: text_input
            font_name: root.font_name
            multiline: root.multiline
            write_tab: root.write_tab
            font_size: root.font_size
            password: root.is_password
            hint_text: root.placeholder
            cursor_color: root.cursor_color
            hint_text_color: root.hint_color
            foreground_color: root.font_color
            disabled_foreground_color: root.disabled_font_color

<PasswordFieldInterface>:
    toggle: toggle.__self__
    spacing: '6sp'

    TogglePassword:
        id: toggle
        disabled: True
""")


class InputInterface(TextInput):

    def on_text(self, *largs):
        self.parent.parent.dispatch('on_text_validate', *largs)

    def on_focus(self, *largs):
        self.parent.parent.dispatch('on_focus', *largs)


class InputFieldInterface(BLayout):
    placeholder = StringProperty('')
    multiline = BooleanProperty(False)
    write_tab = BooleanProperty(False)
    font_size = NumericProperty('15sp')
    is_password = BooleanProperty(False)
    font_name = StringProperty('courbd')
    hint_color = ListProperty([0, 1, 0, .2])
    font_color = ListProperty([.4, .3, .3, 1])
    cursor_color = ListProperty([.3, 1, .5, 1])
    foreground_color = ListProperty([0, 0, 0, 0])
    disabled_font_color = ListProperty([.1, .6, .3, 1])

    text_input = ObjectProperty(None)
    focus_background_color = [1, 0, 0, .1]
    background_color = ListProperty([0, 0, 0, 0])

    def __init__(self, **kwargs):
        self.register_event_type('on_focus')
        self.register_event_type('on_text_validate')
        super(InputFieldInterface, self).__init__(**kwargs)

    def on_text_validate(self, *largs):
        pass

    def on_focus(self, *largs):
        self.background_color, self.focus_background_color = [
            self.focus_background_color, self.background_color
        ]


class TogglePassword(Clicking):
    pace = NumericProperty(5)

    def on_press(self):
        self.parent.is_password = not self.parent.is_password


class PasswordFieldInterface(InputFieldInterface):
    toggle = ObjectProperty(None)

    def _toggle(self, do_disable=True):
        if do_disable is None and not self.toggle.disabled:
            self.toggle.disabled = self.is_password = True
        elif do_disable is not None:
            if self.toggle.disabled:
                self.toggle.disabled = False

    def on_is_password(self, widget, value):
        if not self.text_input:
            return
        if not self.text_input.text:
            return
        self._toggle(value)

    def on_text_validate(self, widget, value):
        do_disable = self.is_password if value else None
        self._toggle(do_disable=do_disable)
