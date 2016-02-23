import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.graph import Graph, MeshLinePlot



class selectingDataSet(Screen):

    def __init__(self, **kwargs):
        super (selectingDataSet, self).__init__(**kwargs)

        layout = FloatLayout(cols=3, row_force_default=True, row_default_height=40)

        #instantiate the buttons
        cafeButton = Button(text='CAFE', size_hint=(.2, .1), pos_hint={'x': .2, 'center_y': .6})
        pofaButton = Button(text='POFA', size_hint=(.2, .1), pos_hint={'center_x': .7, 'center_y': .6})
        loadButton = Button(text='Next', size_hint=(.25, .15), pos_hint={'x': .75, 'y': 0})

        #add buttons to the layout
        layout.add_widget(cafeButton)
        layout.add_widget(pofaButton)
        layout.add_widget(loadButton)

        #instantiate the labels
        title = Label(text="Select one of the data sets to load images",font_size=30, pos_hint={'x': 0, 'center_y': .9})
        cafeDescription = Label(text="*CAFE Description Here*", font_size=15, pos_hint={'x': -.2, 'center_y': .5})
        pofaDescription = Label(text="*POFA Description Here*", font_size=15, pos_hint={'x': .2, 'center_y': .5})

        #add labels to the layout
        layout.add_widget(title)
        layout.add_widget(cafeDescription)
        layout.add_widget(pofaDescription)

        #binding the buttons to the clk method
        cafeButton.bind(on_press=self.clk)
        pofaButton.bind(on_press=self.clk)
        loadButton.bind(on_press=self.changer)

        return layout

    def changer(self,*args):
        self.manager.current = 'screen2'


    def clk(self, obj):
        print("Hello World!")


    def callback():
        print 'Button is being pressed.'
        

class TestApp(App):

        def build(self):
            my_screenmanager = ScreenManager()
            screen1 = selectingDataSet(name='screen1')
            screen2 = runPCA(name='screen2')
            my_screenmanager.add_widget(screen1)
            my_screenmanager.add_widget(screen2)
            return my_screenmanager


if __name__ == '__main__':
    TestApp().run()









class numComponentsSelect(FloatLayout):

    def __init__(self, **kwargs):
        super(numComponentsSelect, self).__init__(**kwargs)
        self.numComponents = Label(text='Number of components:  ',pos=(0,250))
        #self.numComponents.bind(value=self.sliderChange)
        compSlider = Slider(min=1, max=109,value=25,pos=(0,200))
        compSlider.bind(value=self.sliderChange)
        self.add_widget(self.numComponents)
        self.add_widget(compSlider)

        # after images
        layout = FloatLayout()
        self.before1 = Image(source='face1.png',pos=(-300,100))
        self.before2 = Image(source='face2.png',pos=(-170,100))
        layout.add_widget(self.before1)
        layout.add_widget(self.before2)
        self.add_widget(layout)

    def sliderChange(instance,obj,value):
        instance.numComponents = Label(text=('Number of components: ' + str(round(value))))
        instance.before1 = Image(source='face1.png')
        instance.before2 = Image(source='face2.png')
        instance.numComponents.canvas.ask_update()
        instance._trigger_layout()

    def numUpdate(instance,obj,value):
        obj.text=value


class runPCA(Screen):

    def __init__(self,**kwargs):
        super (runPCA, self).__init__(**kwargs)

        layout = FloatLayout()
        layout.add_widget(beforeImages())
        layout.add_widget(numComponentsSelect())
        layout.add_widget(pcaGraph())
        nextBtn = Button(text='Next', size_hint=(.25,.1),pos=(300,30))
        layout.add_widget(nextBtn)
        return layout
