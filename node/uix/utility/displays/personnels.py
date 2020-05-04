from kivy.lang import Builder
from kivy.uix.label import Label
from uix.utility.templates.layouts import BLayout, Layouts


Builder.load_string("""
<ReposHeader>:
    font_name: 'courbd'
    size_hint_y: None
    font_size: '13sp'
    valign: 'middle'
    height: '26dp'


<PersonnelRepos>:
    orientation: 'vertical'
    spacing: '5sp'
    padding: '5sp'

    BoxLayout:
        orientation: 'vertical'

        ReposHeader:
            text: 'Connected Users'
        ScrollingLayout:
            GLayout:
                cols: 1
                id: personnel
                spacing: '1sp'
                padding: '2sp', '5sp'
                size_hint_y: None
                height: max(self.parent.height, self.minimum_height)
    BoxLayout:
        orientation: 'vertical'

        ReposHeader:
            text: 'Chatting Groups'
        ScrollingLayout:
            GLayout:
                cols: 1
                id: groups
                spacing: '1sp'
                padding: '2sp', '5sp'
                size_hint_y: None
                height: max(self.parent.height, self.minimum_height)
""")


class PersonnelRepos(BLayout):
    background_color = [0, 0, .1, 1]

    def to_whom(self):
        return self.ids.personnel


class ReposHeader(Label, Layouts):
    background_color = [.4, 0, .3, 1]
