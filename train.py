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
from kivy.lang import Builder

kv = '''
FloatLayout:

    ToggleButton:
        text: 'Train for Gender'
        pos_hint: {'x':.1, 'center_y': .83}
        on_press: app.training = 'gender'
        state: 'down' if app.training == 'gender' else 'normal'
        size_hint: (.2, .1)
        group: 'training'
        allow_no_selection: False


    ToggleButton:
        text: 'Train for Expression'
        pos_hint: {'x': .4, 'center_y': .83}
        on_press: app.training = 'expression'
        state: 'down' if app.training == 'expression' else 'normal'
        size_hint: (.2, .1)
        group: 'training'
        allow_no_selection: False


    ToggleButton:
        text: 'Train for Identity'
        pos_hint: {'center_x': .8, 'center_y': .83}
        on_press: app.training = 'identity'
        state: 'down' if app.training == 'identity' else 'normal'
        size_hint: (.2, .1)
        group: 'training'
        allow_no_selection: False



    Button:
        text: 'Train'
        size_hint: (.25, .1)
        pos: (410, 30)
        on_press: app.go_next()

    Button:
        text: 'Back'
        size_hint: (.25, .1)
        pos: (190, 30)
        on_press: app.go_back()


    TextInput:
        text: '10'
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .65}
        value: app.hiddenunits
        on_text_validate: app.hiddenunits = self.value
    Label:
        pos_hint: {'x': .1, 'center_y': .65}
        text: '# hidden units'
        size_hint: (.2, .1)
                

    TextInput:
        text: '0'
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .55}
        value: app.numValidInput
        on_text_validate: app.numValidInput = self.value
    Label: 
        pos_hint: {'x': .1, 'center_y': .55}
        text: '# validations'
        size_hint: (.2, .1)


    TextInput:
        text: '0'
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .45}
        value: app.numTestData
        on_text_validate: app.numTestData = self.value
    Label: 
        pos_hint: {'x': .1, 'center_y': .45}
        text: '# test data'
        size_hint: (.2, .1)


    TextInput:
        text: '0.1'
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .35}
        value: app.hiddenUnitsLearningRate
        on_text_validate: app.hiddenUnitsLearningRate = self.value
    Label: 
        pos_hint: {'x': .1, 'center_y': .36}
        text: 'hidden units'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .1, 'center_y': .34}
        text: 'learning rate'
        size_hint: (.2, .1)
    

    TextInput:
        text: '0.2'
        size_hint: (.07, .05)
        pos_hint: {'x': .8, 'center_y': .65}
        value: app.outputUnitsLearningRate
        on_text_validate: app.outputUnitsLearningRate = self.value
    Label: 
        pos_hint: {'x': .6, 'center_y': .66}
        text: 'output units'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .6, 'center_y': .64}
        text: 'learning rate'
        size_hint: (.2, .1)
        
    
    TextInput:
        text: '0.2'
        size_hint: (.07, .05)
        pos_hint: {'x': .8, 'center_y': .55}
        value: app.momentum
        on_text_validate: app.momentum = self.value
    Label: 
        pos_hint: {'x': .6, 'center_y': .55}
        text: 'momentum rate'
        size_hint: (.2, .1)
        
    
    TextInput:
        text: '0'
        size_hint: (.07, .05)
        pos_hint: {'x': .8, 'center_y': .45}
        value: app.epochs
        on_text_validate: app.epochs = self.value
    Label: 
        pos_hint: {'x': .6, 'center_y': .46}
        text: '# of epochs'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .6, 'center_y': .44}
        text: 'needed to train'
        size_hint: (.2, .1)

    
    TextInput:
        text: '0'
        size_hint: (.07, .05)
        pos_hint: {'x': .8, 'center_y': .35}
        value: app.rmse
        on_text_validate: app.rmse = self.value
    Label: 
        pos_hint: {'x': .6, 'center_y': .35}
        text: 'or minimum RMSE'
        size_hint: (.2, .1)
'''

class runTrain(Screen):
    def __init__(self, **kwargs):
        super(runTrain, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
