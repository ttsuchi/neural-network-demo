from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


kv = '''
FloatLayout:
    cols: 3
    row_force_default: True
    row_default_height: 40

    Spinner:
        text: 'POFA'
        values: 'CAFE', 'POFA'
        size_hint: (.2, .1)
        pos_hint: { 'x': .2, 'center_y': .5 }
        on_text: app.dataset_name = self.text

    Label:
        text: app.dataset['DESCR']
        font_size: 20
        pos_hint: {'x': .2, 'center_y': .5}

    Button:
        text: 'Next'
        size_hint: (.25, .1)
        pos: (410, 30)
        on_press: app.go_next()

    Label:
        text: "Please select one of the data sets to load"
        font_size: 30
        pos_hint: {'x': 0, 'center_y': .8}

    Label:
        text: "images and run Principal Component Analysis."
        font_size: 30
        pos_hint: {'x': 0, 'center_y': .72}

'''


class SelectDataSet(Screen):
    def __init__(self, **kwargs):
        super(SelectDataSet, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
