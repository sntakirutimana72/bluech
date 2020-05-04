from kivy.uix.widget import Widget
from kivy.core.window import Window
from pyautogui import position as pypos
from kivy.properties import OptionProperty, BooleanProperty


class Hovering(object):
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_hover')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self._mouse_pos)
        super(Hovering, self).__init__(**kwargs)

    def _mouse_pos(self, *largs):
        if not self.get_root_window():
            return
        obj_pos = largs[1]
        mouse_entered = self.collide_point(*self.to_widget(*obj_pos))

        if self.hovered == mouse_entered:
            return
        self.hovered = mouse_entered
        self.dispatch('on_hover' if mouse_entered else 'on_leave')

    def on_hover(self):
        pass

    def on_leave(self):
        pass


class Dragging(Widget):
    draggable_obj = OptionProperty('layer', options=['layer', 'app', 'none'])

    def __init__(self, **kwargs):
        self.register_event_type('on_drag_window') if self.draggable_obj != 'none' else ''
        super(Dragging, self).__init__(**kwargs)
        self.dragging_ref_pos = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            for child in self.ids.values():
                if child.collide_point(*touch.pos):
                    return super(Dragging, self).on_touch_down(touch)
            if self.draggable_obj == 'none':
                return True

            touch.grab(self)
            Window.grab_mouse()
            self._regulate_current_pos()
            return True
        return super(Dragging, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            self.dispatch('on_drag_window')

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            Window.ungrab_mouse()
        else:
            return super(Dragging, self).on_touch_up(touch)

    def on_drag_window(self):
        if self.draggable_obj == 'layer':
            current_mouse_pos = self.to_local(*pypos())
            self.parent.x, self.parent.top = [current_mouse_pos[0] - self.dragging_ref_pos[0],
                                              current_mouse_pos[1] - self.dragging_ref_pos[1]]
        elif self.draggable_obj == 'app':
            current_mouse_pos = pypos()
            Window.left, Window.top = [current_mouse_pos[0] - self.dragging_ref_pos[0],
                                       current_mouse_pos[1] - self.dragging_ref_pos[1]]

    def _regulate_current_pos(self):
        if self.draggable_obj == 'layer':
            current_mouse_pos = self.to_local(*pypos())
            current_win_left, current_win_top = self.parent.x, self.parent.top
        elif self.draggable_obj == 'app':
            current_mouse_pos = pypos()
            current_win_left, current_win_top = Window.left, Window.top

        self.dragging_ref_pos = [current_mouse_pos[0] - current_win_left,
                                 current_mouse_pos[1] - current_win_top]


class Clicking(Widget):

    def __init__(self, **kwargs):
        self.register_event_type('on_view')
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        super(Clicking, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.dispatch('on_view')
            else:
                self.dispatch('on_press')
            return True
        return super(Clicking, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.dispatch('on_release')
            return True
        return super(Clicking, self).on_touch_up(touch)

    def on_view(self):
        pass

    def on_press(self):
        pass

    def on_release(self):
        pass
