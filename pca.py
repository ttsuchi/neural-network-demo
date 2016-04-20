from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.screenmanager import Screen
from kivy.graphics import Line

class RunPCA(Screen):

    def __init__(self, **kwargs):
        super(RunPCA, self).__init__(**kwargs)

        layout = FloatLayout()
        layout.add_widget(beforeImages())
        layout.add_widget(numComponentsSelect())
        layout.add_widget(pcaGraph())
        nextBtn = Button(text='Next', size_hint=(.25,.1),pos=(410,30))
        nextBtn.bind(on_press=self.changeScreens)
        prevBtn = Button(text='Back', size_hint=(.25,.1),pos=(190,30))
        prevBtn.bind(on_press=self.goBack)
        layout.add_widget(nextBtn)
        layout.add_widget(prevBtn)
        layout.add_widget(Label(text='  Drag the slider to select the number of components you\'d like to analyze. \nThe more components you select, the more variance your dataset will have.' \
                , pos=(0,265)))
        self.add_widget(layout)

    def changeScreens(self, obj):
        self.manager.current = 'screen3'

    def goBack(self, obj):
        self.manager.current = 'screen1'

class numComponentsSelect(FloatLayout):

    def __init__(self, **kwargs):
        super(numComponentsSelect, self).__init__(**kwargs)
        self.numComponents = Label(text='Number of components: 25 ',pos=(0,215))
        ''' this line doesn't seem to do anything but the binding doesn't work
         without it ''' 
        self.numComponents.text = self.numComponents.text
        compSlider = Slider(min=1, max=109,value=25,pos=(55,190), size_hint=(.9,1))
        compSlider.value = 25
        compSlider.bind(value=self.sliderChange)
        self.add_widget(self.numComponents)
        self.add_widget(compSlider)

        # line for graph
        with self.canvas:
            Line(points=[450, 150, 450, 450], width=1)

        # after images
        layout = FloatLayout()
        self.before1 = Image(source='face1.png',pos=(-300,-110))
        self.before2 = Image(source='face2.png',pos=(-170,-110))
        layout.add_widget(self.before1)
        layout.add_widget(self.before2)
        self.recLabel = Label(text='Reconstruction with 25 components', pos=(-235, -20))
        self.add_widget(self.recLabel)
        self.add_widget(layout)

    def sliderChange(instance,obj,value):
        instance.numComponents.text = 'Number of components: ' + str(int(value))
        instance.before1.source='face2.png'
        instance.before2.source='face1.png'
        instance.recLabel.text='Reconstruction with ' + str(int(value)) + ' components'

    def numUpdate(instance,obj,value):
        obj.text=value

class beforeImages(FloatLayout):

    def __init__(self, **kwargs):
        super(beforeImages, self).__init__(**kwargs)
        self.add_widget(Image(source='face1.png',pos=(-300,78)))
        self.add_widget(Image(source='face2.png',pos=(-170,78)))
        self.add_widget(Label(text='Original', pos=(-235,170)))


class pcaGraph(FloatLayout):

    def __init__(self, **kwargs):
        super(pcaGraph, self).__init__(**kwargs)
        graph = Graph(xlabel='Component number',ylabel='Variance provided by additinoal component',x_ticks_minor=5, \
                x_ticks_major=25,y_ticks_major=1,y_grid_label=True, \
                x_grid_label=True,padding=5,x_grid=True,y_grid=True, \
                xmin=-0,xmax=100,ymin=-1,size_hint=(.55,.60),pos=(325,100))
        plot = MeshLinePlot(color=[1,0,0,1])
        plot.points = [(x,700/x) for x in range(1,101)]
        graph.add_plot(plot)
        self.add_widget(graph)

#if __name__ == "__main__":
 #   runPCA().run()

