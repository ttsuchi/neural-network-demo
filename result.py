from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from kivy.uix.image import Image
from kivy.uix.label import Label

kv = '''
BoxLayout:
    orientation: 'vertical'
    padding: [30]
    BoxLayout:
        size_hint: (1, .4)
        orientation: 'horizontal'
        BoxLayout:
            size_hint: (.4, 1)
            orientation: 'vertical'
            BoxLayout:
                orientation: 'vertical'
                AnchorLayout:
                    anchor_x: 'center'
                    anchor_y: 'center'
                    Button:
                        text: 'Back'
                        size_hint: (.8, .5)
                        on_press: app.go_back()
                AnchorLayout:
                    anchor_x: 'center'
                    anchor_y: 'center'
                    Button:
                        text: 'Pause'
                        size_hint: (.8, .5)

        BoxLayout:
            size_hint: (.6, 1)

    ScrollView:
        size_hint: (1, .6)
        do_scroll_x: False
        do_scroll_y: True
        scroll_type: ['bars', 'content']
        bar_width: 10

        GridLayout:
            id: result_grid
            cols: 5
            spacing: 15
            row_force_default: True
            row_default_height: 75
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: 'Actual Image'
            Label:
                text: 'Network Image'
            Label:
                text: 'Network Portrayal'
            Label:
                text: 'Actual Portrayal'
            Label:
                text: 'Correct?'
'''

class TrainingResult(Screen):
    def __init__(self, **kwargs):
        super(TrainingResult, self).__init__(**kwargs)
        contents = Builder.load_string(kv)
        self.add_widget(contents)

        # Sample content
        grid = contents.ids.result_grid
        for j in range(157):
            # First column: Actual image
            grid.add_widget(Image(source='face1.png'))

            # Second column: Network's image reconstruction
            grid.add_widget(Image(source='face1.png'))

            # Third column: Network Representation
            grid.add_widget(Label(text='mad', size_hint=(.5, .5)))

            # Fourth column: Actual representation
            grid.add_widget(Label(text='happy', size_hint=(.5, .5)))

            # Fifth column: correct/incorrect
            grid.add_widget(Label(text='1', size_hint=(.5, .5)))

