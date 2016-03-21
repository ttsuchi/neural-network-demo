from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class SelectingDataSet(Screen):
    def __init__(self, **kwargs):
        super(SelectingDataSet, self).__init__(**kwargs)

        layout = FloatLayout(cols=3, row_force_default=True, row_default_height=40)

        # instantiate the buttons
        cafeButton = Button(text='CAFE', size_hint=(.2, .1), pos_hint={'x': .2, 'center_y': .6})
        pofaButton = Button(text='POFA', size_hint=(.2, .1), pos_hint={'center_x': .7, 'center_y': .6})
        loadButton = Button(text='Next', size_hint=(.25, .15), pos_hint={'x': .75, 'y': 0})

        # add buttons to the layout
        layout.add_widget(cafeButton)
        layout.add_widget(pofaButton)
        layout.add_widget(loadButton)

        # instantiate the labels
        title = Label(text="Select one of the data sets to load images", font_size=30,
                      pos_hint={'x': 0, 'center_y': .9})
        cafeDescription = Label(text="*CAFE Description Here*", font_size=15, pos_hint={'x': -.2, 'center_y': .5})
        pofaDescription = Label(text="*POFA Description Here*", font_size=15, pos_hint={'x': .2, 'center_y': .5})

        # add labels to the layout
        layout.add_widget(title)
        layout.add_widget(cafeDescription)
        layout.add_widget(pofaDescription)

        # binding the buttons to the clk method
        cafeButton.bind(on_press=self.clk)
        pofaButton.bind(on_press=self.clk)
        loadButton.bind(on_press=self.changer)

        self.add_widget(layout)

    def changer(self, *args):
        self.manager.current = 'screen2'

    def clk(self, obj):
        print("Hello World!")
