from time import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from utils.helpers.formatters import timesign
from uix.utility.templates.layouts import Layouts
from uix.utility.displays.message import MessageUI
from uix.utility.templates.textinputs import InputFieldInterface


Builder.load_string("""
<Room>:
    BLayout:
        background_color: [0, 0, .1, 1]
        ScrollingLayout:
            GridLayout:
                cols: 1
                id: display
                spacing: '1sp'
                padding: '3sp'
                size_hint_y: None
                height: max(root.height, self.minimum_height)


<RoomHeader>:
    font_name: 'courbd'
    size_hint_y: None
    font_size: '13sp'
    valign: 'middle'
    height: '26dp'


<ChatRoom>:
    orientation: 'vertical'
    padding: 0, '5sp'
    spacing: '3sp'

    RoomHeader:
        text: root.active_room
    ScreenManager:
        id: rooms
        Room:
            name: 'default'
    MessageInput:
        id: message_input
        font_size: '13sp'
        font_color: [.2, 1, .2, 1]
        hint_color: [.1, .1, .1, 1]
        background_color: [0, 0, 1, .2]
        foreground_color: [0, 0, .12, 1]
        placeholder: 'Enter Message Here'
        disabled_font_color: [.1, .1, .1, 1]
        disabled: rooms.current == 'default'
        focus_background_color: [0, 1, 0, .1]
""")


class Room(Screen):

    def get_display(self):
        return self.ids.display


class ChatRoom(BoxLayout):
    active_room = StringProperty('@@default Room')

    def what_room(self, room: str):
        self.rename(room)

        if not self.ids.rooms.has_screen(room):
            room_screen = Room(name=room)
            self.ids.rooms.add_widget(room_screen)
        else:
            room_screen = self.ids.rooms.get_screen(room)

        self.ids.rooms.current = room

        return room_screen.get_display()

    def rename(self, new_name: str):
        if self.ids.rooms.current == 'default':
            self.ids.rooms.get_screen('default').name = new_name
        self.active_room = new_name

    def map_message(self, message: str):
        timestamp = time()
        receiver = self.active_room

        json_format = {
            'from_': '@Me',
            'msg_': message,
            'route': '/message',
            'time_': timesign(timestamp)
        }
        self.what_room(receiver).add_widget(
            MessageUI(content=json_format)
        )

        del json_format['from_']
        json_format['time_'] = timestamp
        json_format['to_'] = receiver.replace('@@All Members', '').strip('@')
        App.get_running_app().submit_message(json_format)


class RoomHeader(Label, Layouts):
    background_color = [.2, 1, .2, 1]


class MessageInput(InputFieldInterface):

    def on_focus(self, *largs):
        super().on_focus(*largs)

        message = self.text_input.text.strip()
        if not largs[1] and message:
            self.parent.map_message(message)
            self.text_input.text = ''
