from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.properties import ListProperty, NumericProperty, ObjectProperty


Builder.load_string("""
<Layouts>:
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.left_border_color
        SmoothLine:
            width: self.border_width
            points: [*self.pos, self.x, self.top]
        Color:
            rgba: self.right_border_color
        SmoothLine:
            width: self.border_width
            points: [self.right, self.y, self.right, self.top]
        Color:
            rgba: self.down_border_color
        SmoothLine:
            width: self.border_width
            points: [*self.pos, self.right, self.y]
        Color:
            rgba: self.top_border_color
        SmoothLine:
            width: self.border_width
            points: [self.x, self.top, self.right, self.top]
""")


class Layouts(Widget):
    border_width = NumericProperty(1)
    hover_background_color = ListProperty(None)
    focus_background_color = ListProperty(None)
    background_color = ListProperty([0, 0, 0, 0])
    top_border_color = ListProperty([0, 0, 0, 0])
    down_border_color = ListProperty([0, 0, 0, 0])
    left_border_color = ListProperty([0, 0, 0, 0])
    right_border_color = ListProperty([0, 0, 0, 0])


class ScrollingLayout(ScrollView):
    bar_width = NumericProperty(5)
    bar_color = ListProperty([.3, .7, .5, .2])
    effect_cls = ObjectProperty(OpacityScrollEffect)
    bar_inactive_color = ListProperty([.3, .7, .5, .2])


class BLayout(BoxLayout, Layouts):
    pass


class GLayout(GridLayout, Layouts):
    pass
