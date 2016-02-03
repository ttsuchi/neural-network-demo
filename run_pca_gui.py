from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

class runPCA(App):

    def build(self):
        layout = GridLayout(cols=1)
        layout.add_widget(beforeImages())
        layout.add_widget(numComponentsSelect())
        explainBtn = Button(text='Explanation')
        layout.add_widget(explainBtn)
        nextBtn = Button(text='Next')
        layout.add_widget(nextBtn)
        return layout

class numComponentsSelect(BoxLayout):

    def __init__(self, **kwargs):
        super(numComponentsSelect, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.numComponents = Label(text='Number of components:  ')
        compSlider = Slider(min=1, max=109)
        self.add_widget(self.numComponents)
        self.add_widget(compSlider)
        compSlider.bind(value=self.sliderChange)

        # after images
        layout = BoxLayout(orientation='horizontal')
        self.before1 = Image(source='face1')
        self.before2 = Image(source='face2')
        layout.add_widget(self.before1)
        layout.add_widget(self.before2)

    def sliderChange(instance, value):
        self.numComponents.txt = 'Number of components: ' + value
        self.before1 = Image(source='face1')
        self.before2 = Image(source='face2')

class beforeImages(BoxLayout):

    def __init__(self, **kwargs):
        super(beforeImages, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.add_widget(Image(source='face1'))
        self.add_widget(Image(source='face2'))

if __name__ == "__main__":
    runPCA().run()

