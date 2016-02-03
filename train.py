from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.image import Image

class train(App):

    def build(self):
        layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)
        layout.add_widget(Button(text='Train for gender', size_hint_x=None, width=500))
        layout.add_widget(Button(text='Train for expression'))


        
        return layout
    def callback():
        print 'button is being pressed.'
        
if __name__ == '__main__':
    train().run()
