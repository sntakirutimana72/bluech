import re
import time
from kivy.app import App
from threading import Thread
from kivy.lang import Builder
from guix.loading import Loading
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from guix.customlayers import SquaredLogo
from guix.textinputs import InputTextField
from kivy.properties import ObjectProperty, StringProperty, \
    OptionProperty, ListProperty, NumericProperty
from guix.templates import Clicking, Hovering, IconFullPath, BoxLayer, \
    ButtonTemplate, FocusBehavior, FocusBehaviorHandler, GridLayer

Builder.load_string('''
<SearchEngine>:
    spacing: '2sp'
    padding: '2sp'
    search_keyword: search_keyword.__self__

    SearchInputTextField:
        id: search_keyword
        size_hint: (1, 1)
        placeholder: root.placeholder
    SearchInitiator:
        icon_name: 'search.png'
        on_release: root.search(self)


<CategoryDropDown>:
    padding: '1sp'
    size_hint: (None, None)
    top: 0 if not self.hoster else (self.hoster.y - 2)
    x: 0 if not self.hoster else self.rationalize_pos_x()
    height: dp(len(category_list.children[:3]) * 20 + len(category_list.children[:3]) + 5)

    ScrollingBehavior:
        FocusHandler:
            cols: 1
            spacing: '1sp'
            padding: '2sp'
            size_hint_y: None
            id: category_list
            border_radius: [3]
            background_color: [0, 0, .1, 1]
            height: max(self.parent.height, self.minimum_height)


<DropDownElt>:
    valign: 'middle'
    size_hint_y: None
    font_size: '11sp'
    font_name: 'courbd'
    padding: ('10sp', 0)
    color: [.3, .35, .3, 1]
    text_size: self.width, None
    height: max(dp(20), self.texture_size[1])


<SearchCategory>:
    padding: '1sp'

    Label:
        text: root.text
        size_hint_x: None
        font_size: '10.5sp'
        font_name: 'trebucbd'
        color: [.6, .6, .4, 1]
        width: self.parent.width * .3
    InputTextField:
        disabled: True
        padding: '2sp', 0
        font_size: '11.5sp'
        size_hint: (1, 1)
        id: selected_category
        placeholder: root.hint_text
        background_color: [0, 0, .15, 1]
        disabled_font_color: [.12, .12, .2, 1]
    DropDownArrow:
        icon_name: 'dropdown.png'
        on_release: root.drop_down()

''')


class DropDownElt(Label, FocusBehavior, ButtonTemplate):
    hover_background_color = [0, 1, 1, .1]
    focus_background_color = [0, 1, .6, 1]

    def on_hover(self):
        self._update_hover_features()

    def on_leave(self):
        self._update_hover_features()

    def on_press(self):
        if not self.focusBehaved:
            self.focusBehaved = True
            self.parent.dispatch('on_focusBehavioral', self)

    def on_release(self):
        pass

    def on_focusBehaved(self, *largs):
        self._update_event_features()

    def _update_event_features(self):
        if self.hovered:
            self._update_hover_features()

        self.focus_background_color, self.background_color = [
            self.background_color, self.focus_background_color
        ]
        if self.hovered:
            self._update_hover_features()

    def _update_hover_features(self):
        self.background_color, self.hover_background_color = [
            self.hover_background_color, self.background_color
        ]


class SearchInitiator(Clicking, Hovering, Loading):
    _loader = None
    back_layer_color = ListProperty([0, 0, 0, 1])
    fore_layer_color = ListProperty([0, .2, .5, 0])

    def on_disabled(self, *largs):
        if largs[1]:
            self._loader = Clock.schedule_interval(self._update_angle_, .01)
        else:
            self._loader.cancel()
            self._loader = None

    def on_parent(self, *largs):
        pass

    def on_hover(self):
        self.pace = .16

    def on_leave(self):
        self.pace = .2


class FocusHandler(GridLayer, FocusBehaviorHandler):

    def on_focusBehavioral(self, child):
        if self.behaviorFocus != child:
            if self.behaviorFocus:
                self.behaviorFocus.focusBehaved = False
            self.behaviorFocus = child
            self.parent.parent.set_category_(child.text)


class SearchInputTextField(InputTextField):
    font_color = [.3, .6, .4, 1]
    cursor_color = [0, .8, 1, 1]
    hint_color = [.1, .1, .2, 1]
    disabled_font_color = [.1, .1, .1, 1]
    focus_background_color = [0, 0, .2, 1]
    background_color = ListProperty([0, 0, .15, 1])

    def on_focus(self, *largs):
        self.background_color, self.focus_background_color = [
            self.focus_background_color, self.background_color
        ]


class DropDownArrow(Clicking, SquaredLogo, IconFullPath):
    pass


class CategoryDropDown(BoxLayer):
    _resiz_anim = None
    hoster = ObjectProperty(None, allownone=True)
    background_color = ListProperty([1, 1, .5, 1])

    def _flag_me(self):
        self._resiz_anim = None
        self.disabled = False

    def _anim_resize(self):
        len_children = len(self.ids.category_list.children[:10])
        new_height = len_children * 20 + len_children + 5
        new_top = self.hoster.y  - 2
        self._resiz_anim = Animation(height=new_height, top=new_top, d=.06)
        self._resiz_anim.bind(on_complete=self._resize_finished)
        self._resiz_anim.start(self)

    def on_parent(self, *largs):
        if not largs[1]:
            self.hoster = None
            if self._resiz_anim:
                self._resiz_anim.cancel()
                self._flag_me()
            if len(self.ids.category_list.children) > 3:
                len_children = len(self.ids.category_list.children[:3])
                self.height = len_children * 20 + len_children + 5
        else:
            if len(self.ids.category_list.children) > 3:
                self.disabled = True
                self._anim_resize()

    def rationalize_pos_x(self):
        window_x = self.hoster.to_window(self.hoster.x, 0)[0]
        return window_x + (self.hoster.width * .3)

    def set_category_(self, categ):
        self.hoster.set_category_(categ)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            self.parent.remove_widget(self)
        return super(CategoryDropDown, self).on_touch_down(touch)

    def _resize_finished(self, *largs):
        self._flag_me()


class SearchCategory(BoxLayer):
    background_color = [0, 0, 1, .5]
    border_radius = [3]

    _drop_initiated = None
    dropdown = ObjectProperty(None)
    text = StringProperty('SEARCH CATEGORY')
    hint_text = StringProperty('Select Category')
    _drop_list = ListProperty(None, allownone=True)

    def drop_down(self):
        if self.dropdown and not self.dropdown.parent:
            self.dropdown.hoster = self
            App.get_running_app().root_window.add_widget(self.dropdown)

    def _init_dropdown(self):
        _drop_list_temp = self._empty_drop_list()
        for index, drop_elt in enumerate(_drop_list_temp):
            self._add_dropdown_elt(drop_elt)
            time.sleep(.01)

            if ((index + 1) == len(_drop_list_temp)) and self._drop_list:
                _drop_list_temp = self._empty_drop_list()
        self._release_motions(False)

    def _release_motions(self, is_released):
        self.parent.disabled = is_released

    def _empty_drop_list(self):
        _temp = self._drop_list.copy()
        self._drop_list = None
        return _temp

    def set_drop_list(self, *largs):
        self._drop_list = list(largs)

    def on__drop_list(self, *largs):
        if not largs[1]:
            return
        if not self._drop_initiated:
            self._drop_initiated = True
            Thread(target=self._init_dropdown).start()

    def set_category_(self, search_categ):
        self.hint_text = search_categ

    @mainthread
    def _add_dropdown_elt(self, choice_elt):
        if not self.dropdown:
            self.dropdown = CategoryDropDown(width=(self.width * .7 - self.height))
        self.dropdown.ids.category_list.add_widget(DropDownElt(text=choice_elt))


class SearchEngine(BoxLayer):
    background_color = [0, 0, 1, .5]
    border_radius = [3]

    search_keyword = ObjectProperty(None)
    placeholder = StringProperty('Enter Search Keyword')
    match_cdt = OptionProperty('one', options=['one', 'all'])

    def search(self, initiator):
        self._flag_engine(initiator)
        Thread(
            target=self._linear_searching,
            args=(initiator, '', [])
        ).start()

    def _linear_searching(self, initiator, keyword, search_set):
        time.sleep(5)
        self._flag_engine(initiator, False)

    @mainthread
    def _flag_engine(self, initiator, what_=True):
        if not what_:
            self.search_keyword.text_input.text = ''
        self.disabled = what_
        initiator.fore_layer_color[-1] = .7 if what_ else 0
