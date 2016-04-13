from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.uix.screenmanager import Screen

class SelectingDataSet(Screen):

    def __init__(self, **kwargs):
        super(SelectingDataSet, self).__init__(**kwargs)

        self.selectedSet = "none"

        layout = FloatLayout(cols=3, row_force_default=True, row_default_height=40)

        #instantiate the buttons
        cafeButton = ToggleButton(text='CAFE', group='dataset', size_hint=(.2, .1), pos_hint={'x': .2, 'center_y': .6})
        pofaButton = ToggleButton(text='POFA', group='dataset', size_hint=(.2, .1), pos_hint={'center_x': .7, 'center_y': .6})
        nextBtn = Button(text='Next', size_hint=(.25,.1),pos=(300,30))
        loadButton = Button(text='Next', size_hint=(.25, .1), pos=(410,30))

        #add buttons to the layout
        layout.add_widget(cafeButton)
        layout.add_widget(pofaButton)
        layout.add_widget(loadButton)

        #instantiate the labels
        title1 = Label(text="Please select one of the data ",font_size=30, pos_hint={'x': 0, 'center_y': .8})
        title2 = Label(text="sets to load images and run PCA.",font_size=30, pos_hint={'x': 0, 'center_y': .72})
        cafeDescription = Label(text='CA (California) Facial Expressions:\nimages of facial expressions aligned and normalized', font_size=15, pos_hint={'x': -.2, 'center_y': .5})
        pofaDescription = Label(text='Pictures of Facial Affect:\nimages of standard facial expressions', font_size=15, pos_hint={'x': .2, 'center_y': .5})

        #add labels to the layout
        layout.add_widget(title1)
        layout.add_widget(title2)
        layout.add_widget(cafeDescription)
        layout.add_widget(pofaDescription)

        #binding the buttons to the clk method
        cafeButton.bind(on_press=self.cafeselect)
        pofaButton.bind(on_press=self.pofaselect)
        loadButton.bind(on_press=self.changeScreens)

        self.add_widget(layout)

    def changeScreens(self, obj):
        if self.selectedSet != "none":
            self.manager.current = 'screen2'


    def cafeselect(self, obj):
        if self.selectedSet == "none" or self.selectedSet == "pofa":
            self.selectedSet = "cafe"
        else:
            self.selectedSet = "none"

    def pofaselect(self, obj):
        if self.selectedSet == "none" or self.selectedSet == "cafe":
            self.selectedSet = "pofa"
        else:
            self.selectedSet = "none"

#if __name__ == '__main__':
 #   selectingDataSet().run()
