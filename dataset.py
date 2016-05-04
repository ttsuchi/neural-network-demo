from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

kv = '''
FloatLayout:
    cols: 3
    row_force_default: True
    row_default_height: 40

    ToggleButton:
        group: 'select_dataset'
        size_hint: (.2, .1)
        allow_no_selection: False
        text: 'CAFE'
        on_press: app.dataset = 'CAFE'
        state: 'down' if app.dataset == 'CAFE' else 'normal'
        pos_hint: { 'x': .2, 'center_y': .6 }

    ToggleButton:
        group: 'select_dataset'
        size_hint: (.2, .1)
        allow_no_selection: False
        text: 'POFA'
        on_press: app.dataset = 'POFA'
        state: 'down' if app.dataset == 'POFA' else 'normal'
        pos_hint: {'center_x': .7, 'center_y': .6}

    Button:
        text: 'Next'
        size_hint: (.25, .1)
        pos: (410, 30)
        on_press: app.go_next()

    Label:
        text: "Please select one of the data "
        font_size: 30
        pos_hint: {'x': 0, 'center_y': .8}

    Label:
        text: "sets to load images and run PCA."
        font_size: 30
        pos_hint: {'x': 0, 'center_y': .72}

    Label:
        text:
            'CA (California) Facial Expressions:\\n' + \
            'images of facial expressions aligned and normalized'
        font_size: 15
        pos_hint: {'x': -.2, 'center_y': .5}

    Label:
        text:
            'Pictures of Facial Affect:\\n' + \
            'images of standard facial expressions'
        font_size: 15
        pos_hint: {'x': .2, 'center_y': .5}
'''


class SelectDataSet(Screen):
    def __init__(self, **kwargs):
        super(SelectDataSet, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
