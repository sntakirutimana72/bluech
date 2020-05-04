from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ListProperty, ObjectProperty


Builder.load_string("""
<Loading>:
    canvas.before:
        PushMatrix
        Rotate:
            origin: self.center
            angle: self.angle
        Color:
            rgba: self.back_layer_color
        Ellipse:
            angle_start: 0
            angle_end: 190
            pos: self.pos
            size: self.size
    canvas:
        Color:
            rgba: self.fore_layer_color
        Ellipse:
            pos: [self.x + self.pace, self.y + self.pace]
            size: [self.width - (self.pace * 2), self.height - (self.pace * 2)]
    canvas.after:
        PopMatrix

    size_hint_x: None
    width: self.height
"""
)


class Loading(Widget):
    pace = NumericProperty(1.5)
    angle = NumericProperty(0)
    back_layer_color = ListProperty([0, .1, 0, 1])
    fore_layer_color = ListProperty([0, 0, .1, 1])
    launcher = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(Loading, self).__init__(**kwargs)
        self._tuner = Clock.schedule_interval(self._update_angle_, .02)

    def on_parent(self, *largs):
        if not largs[1]:
            self._tuner.cancel()
            self._tuner = None

    def terminate(self):
        launcher = self.launcher
        self._destruct()
        launcher.reset()

    def _destruct(self):
        self.parent.remove_widget(self)
        self.launcher = None

    def relaunch(self):
        launcher = self.launcher
        self._destruct()
        App.get_running_app().root_window.add_widget(launcher)

    def _update_angle_(self, frame: float):
        self.angle -= 5 + frame
