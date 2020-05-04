from kivy.lang import Builder
from uix.utility.templates.layouts import BLayout
from kivy.properties import DictProperty, ListProperty, StringProperty


Builder.load_string("""
<IdentificationUI@Label>:
    markup: True
    valign: 'middle'
    size_hint_y: None
    font_size: '12.5sp'
    font_name: 'courbd'
    text_size: self.width, None
    height: max(self.texture_size[1], dp(20))

<MessageUI>:
    padding: '3sp'
    spacing: '5sp'
    size_hint_y: None
    orientation: 'vertical'
    height: self.minimum_height

    IdentificationUI:
        halign: root.halign
        text: root.content['from_']
        color: [.35, .2, .2, 1] if self.halign == 'right' else [.3, 0, .3, 1]
    IdentificationUI:
        halign: root.halign
        text: root.content['msg_']
        color: [.2, .2, .2, 1] if self.halign == 'right' else [.1, .3, .2, 1]
    IdentificationUI:
        color: [.2, .4, .4, .4]
        text: root.content['time_']
        halign: 'left' if root.halign == 'right' else 'right'
""")


class MessageUI(BLayout):
    content = DictProperty({'from_': '', 'msg_': '', 'time_': '', 'to_': ''})
    background_color = ListProperty([0, 0, .12, 1])
    halign = StringProperty('right')
