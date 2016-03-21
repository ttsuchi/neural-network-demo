from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.image import Image


class RunPCA(Screen):
    def __init__(self, **kwargs):
        super(RunPCA, self).__init__(**kwargs)

        layout = FloatLayout()
        # layout.add_widget(beforeImages())
        layout.add_widget(NumComponentsSelect())
        # layout.add_widget(pcaGraph())
        nextBtn = Button(text='Next', size_hint=(.25, .1), pos=(300, 30))
        layout.add_widget(nextBtn)
        self.add_widget(layout)


class NumComponentsSelect(FloatLayout):
    def __init__(self, **kwargs):
        super(NumComponentsSelect, self).__init__(**kwargs)
        self.numComponents = Label(text='Number of components:  ', pos=(0, 250))
        # self.numComponents.bind(value=self.sliderChange)
        compSlider = Slider(min=1, max=109, value=25, pos=(0, 200))
        compSlider.bind(value=self.sliderChange)
        self.add_widget(self.numComponents)
        self.add_widget(compSlider)

        # after images
        layout = FloatLayout()
        self.before1 = Image(source='face1.png', pos=(-300, 100))
        self.before2 = Image(source='face2.png', pos=(-170, 100))
        layout.add_widget(self.before1)
        layout.add_widget(self.before2)
        self.add_widget(layout)

    def sliderChange(self, obj, value):
        self.numComponents = Label(text=('Number of components: ' + str(round(value))))
        self.before1 = Image(source='face1.png')
        self.before2 = Image(source='face2.png')
        self.numComponents.canvas.ask_update()
        self._trigger_layout()

    def numUpdate(self, obj, value):
        obj.text = value
