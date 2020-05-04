from kivy.lang import Builder
from kivy.uix.label import Label
from uix.utility.templates.layouts import Layouts, BLayout
from uix.utility.templates.behaviors import Clicking, Hovering
from kivy.properties import ListProperty, StringProperty, NumericProperty, BooleanProperty

Builder.load_string("""
<Interface>:
    padding: self.shadow

<BTextInterface>:
    TextLayout:
        text: root.text
        color: root.color
        markup: root.markup
        halign: root.halign
        valign: root.valign
        padding: root.padder
        shorten: root.shorten
        font_size: root.font_size
        font_name: root.font_name
        background_color: root.cover + [1]
        disabled_color: root.disabled_color
        text_size: self.size if root.text_size else self.text_size

<HBResizeInterface>:
    RCGraffitiLayout:
        canvas:
            PushMatrix
            Color:
                rgba: [*root.graffiti_color, root.toggle_graffiti]
            Rotate:
                angle: root.angle
                origin: self.center
            SmoothLine:
                width: 1.1
                points: [self.center_x, self.y + dp(4), \
                    self.center_x, self.top - dp(4)]
            SmoothLine:
                width: 1.1
                points: [self.x + dp(4), self.center_y, \
                    self.right - dp(4), self.center_y]
        canvas.after:
            PopMatrix

<HBMinimizeInterface>:
    MGraffitiLayout:
        canvas:
            Color:
                rgba: [*root.graffiti_color, root.toggle_graffiti]
            SmoothLine:
                points: [self.x + dp(4), self.center_y, \
                    self.right - dp(4), self.center_y]
""")


class Interface(BLayout, Clicking, Hovering):
    cover = ListProperty([0, 0, .15])
    background_color = ListProperty([0, 0, 1, .5])
    shadow = NumericProperty('1sp')

    def on_press(self):
        pass

    def on_hover(self):
        pass

    def on_leave(self):
        pass

    def on_release(self):
        pass


class BTextInterface(Interface):
    text = StringProperty('')
    padder = ListProperty([0, 0])
    markup = BooleanProperty(False)
    halign = StringProperty('left')
    shorten = BooleanProperty(False)
    valign = StringProperty('middle')
    text_size = BooleanProperty(None)
    font_size = NumericProperty('12sp')
    color = ListProperty([.2, .2, .2, 1])
    font_name = StringProperty('Roboto-Bold')
    disabled_color = ListProperty([.1, .1, .1, 1])

    class TextLayout(Label, Layouts):
        pass


class BToggleTextInterface(BTextInterface):
    __toggled__ = None

    @classmethod
    def _toggle(cls, instance):
        pass


class HBInterface(Interface):
    toggle_graffiti = NumericProperty(0)
    graffiti_color = ListProperty([1, 1, .8])
    background_color = ListProperty([0, 0, 0, 0])
    hover_background_color = ListProperty([1, 1, 1, .1])

    def on_hover(self):
        pass

    def on_leave(self):
        pass


class HBResizeInterface(HBInterface):
    angle = NumericProperty(0)

    class RCGraffitiLayout(Layouts):
        pass


class HBMinimizeInterface(HBInterface):

    class MGraffitiLayout(Layouts):
        pass


class HBCloseInterface(HBResizeInterface):
    angle = 45
