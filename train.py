from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

class Train(Screen):

    def __init__(self, **kwargs):
        super(Train, self).__init__(**kwargs)
        
        # Main layout for gui
        layout = FloatLayout()
        
        # Buttons for layout
        layout.add_widget(ToggleButton(text='Train for gender', group='training', size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .83}))
        layout.add_widget(ToggleButton(text='Train for expression', group='training', size_hint=(.2, .1), pos_hint={'x': .4, 'center_y': .83}))
        layout.add_widget(ToggleButton(text='Train for identity', group='training', size_hint=(.2, .1), pos_hint={'center_x': .8, 'center_y': .83}))
        backButton = Button(text='Back', size_hint=(.25, .1), pos=(190,30))
        loadButton = Button(text='Train', size_hint=(.25, .1), pos=(410,30))
        layout.add_widget(loadButton)
        layout.add_widget(backButton)
        loadButton.bind(on_press=self.changeScreens)
        backButton.bind(on_press=self.goBack)



        #Labels and Input Text Boxes
        self.hiddenUnits = 10
        layout.add_widget(Label(text="# of hidden units", size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .65}))
        hiddenUnitsInput = TextInput(text='10', size_hint=(.07, .05), pos_hint={'x': .3, 'center_y': .65}) 
        layout.add_widget(hiddenUnitsInput)
        hiddenUnitsInput.bind(on_text_validate=self.updateHiddenUnits)

        self.numValid = 0
        layout.add_widget(Label(text="# of validations", size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .55}))
        numValidInput = TextInput(text='0', size_hint=(.07, .05), pos_hint={'x': .3, 'center_y': .55})
        layout.add_widget(numValidInput)
        numValidInput.bind(on_text_validate=self.updateNumValid)

        self.numTestData = 0
        layout.add_widget(Label(text="# of test data", size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .45}))
        numTestDataInput = TextInput(text='0', size_hint=(.07, .05), pos_hint={'x': .3, 'center_y': .45})
        layout.add_widget(numTestDataInput)
        numValidInput.bind(on_text_validate=self.updateNumTestData)
        
        self.hiddenUnitsLearningRate = 0.1
        layout.add_widget(Label(text="hidden units \n    learning rate", size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .35}))
        hiddenUnitsLearningRateInput = TextInput(text='0.1', size_hint=(.07, .05), pos_hint={'x': .3, 'center_y': .35})
        layout.add_widget(hiddenUnitsLearningRateInput)
        hiddenUnitsLearningRateInput.bind(on_text_validate=self.updateHiddenUnitsLearningRate)


        layout.add_widget(Label(text="output units \nlearning rate", size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .65}))
        layout.add_widget(TextInput(text='0.2', size_hint=(.07, .05), pos_hint={'x': .8, 'center_y': .65}))

        layout.add_widget(Label(text="momentum rate", size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .55}))
        layout.add_widget(TextInput(text='0.2', size_hint=(.07, .05), pos_hint={'x': .8, 'center_y': .55}))

        layout.add_widget(Label(text="# of epochs needed \n  to train", size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .45}))
        layout.add_widget(TextInput(text='0', size_hint=(.07, .05), pos_hint={'x': .8, 'center_y': .45}))

        layout.add_widget(Label(text="or minimum RMSE", size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .35}))
        layout.add_widget(TextInput(text='0.2', size_hint=(.07, .05), pos_hint={'x': .8, 'center_y': .35}))


        self.add_widget(layout)

    def changeScreens(self, obj):
        self.manager.current = 'screen4'

    def goBack(self,obj):
        self.manager.current = 'screen2'

    def updateHiddenUnits(self,obj,value):
        self.hiddenUnits = value

    def updateNumValid(self,obj,value):
        self.numValid = value

    def updateNumTestData(self,obj,value):
        self.numTestData = value

    def updateHiddenUnitsLearningRate(self,obj,value):
        self.hiddenUnitsLearningRate = value

#if __name__ == '__main__':
 #   train().run()
