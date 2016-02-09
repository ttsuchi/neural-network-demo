from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

class runPCA(App):

    def build(self):
        layout = FloatLayout()
        layout.add_widget(beforeImages())
        layout.add_widget(numComponentsSelect())
        explainBtn = Button(text='Explanation', size_hint=(.25,.1),pos=(200,10))
        nextBtn = Button(text='Next', size_hint=(.25,.1),pos=(420,10))
        layout.add_widget(explainBtn)
        layout.add_widget(nextBtn)
        return layout

class numComponentsSelect(FloatLayout):

    def __init__(self, **kwargs):
        super(numComponentsSelect, self).__init__(**kwargs)
        #self.cols = 1
        #self.row_default_height=10
        self.numComponents = Label(text='Number of components:  ',pos=(0,250))
        compSlider = Slider(min=1, max=109,value=25,pos=(0,200))
        self.add_widget(self.numComponents)
        self.add_widget(compSlider)
        compSlider.bind(value=self.sliderChange)

        # after images
        layout = FloatLayout()
        self.before1 = Image(source='face1.png',pos=(-300,100))
        self.before2 = Image(source='face2.png',pos=(-170,100))
        layout.add_widget(self.before1)
        layout.add_widget(self.before2)
        self.add_widget(layout)

    def sliderChange(instance,idek,value):
        idek.numComponents = Label(text=('Number of components: ' + str(value)))
        idek.before1 = Image(source='face1.png')
        idek.before2 = Image(source='face2.png')

class beforeImages(FloatLayout):

    def __init__(self, **kwargs):
        super(beforeImages, self).__init__(**kwargs)
        #self.rows=1
        self.add_widget(Image(source='face1.png',pos=(-300,-100)))
        self.add_widget(Image(source='face2.png',pos=(-170,-100)))

if __name__ == "__main__":
    runPCA().run()

