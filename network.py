from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput

class network(App):
    def build(self):
        layout = FloatLayout()

        layout.add_widget(Label(text='Actual Image', size_hint=(.2,.1), 
            pos_hint={'x':.02, 'center_y': .98}))
        layout.add_widget(Label(text='Network Image', size_hint=(.2,.1),
            pos_hint={'x':.2, 'center_y': .98}))
        layout.add_widget(Label(text='Actual Representation', size_hint=(.2,.1),
            pos_hint={'x':.38, 'center_y': .98}))
        layout.add_widget(Label(text='Networks Representation', size_hint=(.2,.1),
            pos_hint={'x':.60, 'center_y': .98}))




        #First column: Actual image
        #First column: Actual image
        #First column: Actual image
        #First column: Actual image
        
        layout.add_widget(Image(source='face1.png',pos=(-300,200)))
        layout.add_widget(Image(source='face2.png',pos=(-300,25)))

        #Second column: Network's image reconstruction
        layout.add_widget(Image(source='face1.png',pos=(-165,200)))
        layout.add_widget(Image(source='face2.png',pos=(-165,25)))


        return layout

if __name__ == "__main__":
    network().run()



