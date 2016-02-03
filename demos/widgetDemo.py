from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.image import Image

class widgetDemo(App):

    def build(self):
        layout = GridLayout(cols=1)
        btn = Button(text='Example',width=100,height=40)
        layout.add_widget(btn)
        layout.add_widget(Slider(min=-100, max=100, value=25))
        layout.add_widget(Image(source='diagram.png'))
        return layout
    def callback():
        print 'The button is being pressed.'

if __name__ == '__main__':
    widgetDemo().run()

