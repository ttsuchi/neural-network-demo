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

        layout = FloatLayout(cols=3, row_force_default=True, row_default_height=40)

        #instantiate the buttons
        cafeButton = ToggleButton(text='CAFE', group='dataset', size_hint=(.2, .1), pos_hint={'x': .2, 'center_y': .6})
        pofaButton = ToggleButton(text='POFA', group='dataset', size_hint=(.2, .1), pos_hint={'center_x': .7, 'center_y': .6})
        nextBtn = Button(text='Next', size_hint=(.25,.1),pos=(300,30))
        loadButton = Button(text='Load Images and Run PCA', size_hint=(.25, .15), pos_hint={'x': .75, 'y': 0})

        #add buttons to the layout
        layout.add_widget(cafeButton)
        layout.add_widget(pofaButton)
        layout.add_widget(loadButton)

        #instantiate the labels
        title = Label(text="Select one of the data sets to load images",font_size=30, pos_hint={'x': 0, 'center_y': .9})
        cafeDescription = Label(text='CA (California) Facial Expressions:\nimages of facial expressions aligned and normalized', font_size=15, pos_hint={'x': -.2, 'center_y': .5})
        pofaDescription = Label(text='Pictures of Facial Affect:\nimages of standard facial expressions', font_size=15, pos_hint={'x': .2, 'center_y': .5})

        #add labels to the layout
        layout.add_widget(title)
        layout.add_widget(cafeDescription)
        layout.add_widget(pofaDescription)

        #binding the buttons to the clk method
        cafeButton.bind(on_press=self.clk)
        pofaButton.bind(on_press=self.clk)
        loadButton.bind(on_press=self.changeScreens)

        self.add_widget(layout)

    def changeScreens(self, obj):
        self.manager.current = 'screen2'


    def clk(self, obj):
        print("Hello World!")


    def callback():
        print 'Button is being pressed.'
        
#if __name__ == '__main__':
 #   selectingDataSet().run()
