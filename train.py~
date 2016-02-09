from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput

class train(App):

    def build(self):

 #       textInput = TextInput(text = 'hello')
        
        # Main layout for gui
        layout = FloatLayout()
        
        # Buttons for layout
        layout.add_widget(Button(text='Train for gender', size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .83}))
        layout.add_widget(Button(text='Train for expression', size_hint=(.2, .1), pos_hint={'x': .4, 'center_y': .83}))
        layout.add_widget(Button(text='Train for identity', size_hint=(.2, .1), pos_hint={'center_x': .8, 'center_y': .83}))
        layout.add_widget(Button(text='            Train Net\n  With Above Parameters'
            , size_hint=(.25, .1), pos_hint={'x': .15, 'center_y': .15}))
        layout.add_widget(Button(text='Reset', size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .15}))




        #Labels and Input Text Boxes
        layout.add_widget(Label(text="# of hidden units", size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .65}))
        layout.add_widget(TextInput(text='0.1', size_hint=(.07, .05), pos_hint={'x': .3, 'center_y': .65}))


        layout.add_widget(Label(text="# of validations", size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .55}))
        layout.add_widget(TextInput(text='0.1', size_hint=(.07, .05), pos_hint={'x': .3, 'center_y': .55}))

        layout.add_widget(Label(text="# of test data", size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .45}))
        layout.add_widget(TextInput(text='0.1', size_hint=(.07, .05), pos_hint={'x': .3, 'center_y': .45}))
        
        layout.add_widget(Label(text="# of hidden units \n    learning rate", size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .35}))
        layout.add_widget(TextInput(text='0.1', size_hint=(.07, .05), pos_hint={'x': .3, 'center_y': .35}))


        layout.add_widget(Label(text="output units \nlearning rate", size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .65}))
        layout.add_widget(TextInput(text='0.2', size_hint=(.07, .05), pos_hint={'x': .8, 'center_y': .65}))

        layout.add_widget(Label(text="momentum rate", size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .55}))
        layout.add_widget(TextInput(text='0.2', size_hint=(.07, .05), pos_hint={'x': .8, 'center_y': .55}))

        layout.add_widget(Label(text="# of epochs needed \n  to train", size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .45}))
        layout.add_widget(TextInput(text='0.2', size_hint=(.07, .05), pos_hint={'x': .8, 'center_y': .45}))

        layout.add_widget(Label(text="or minimum RMSE", size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .35}))
        layout.add_widget(TextInput(text='0.2', size_hint=(.07, .05), pos_hint={'x': .8, 'center_y': .35}))


        #layout.add_widget(DropDown(size_hint=(.1, .1), pos_hint={'x': .8, 'center_y': .65}).add_widget(Label(text="1")))


        return layout


    def callback():
        print 'button is being pressed.'

if __name__ == '__main__':
    train().run()
