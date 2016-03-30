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

class RunPCA(Screen):

    def __init__(self, **kwargs):
        super(RunPCA, self).__init__(**kwargs)

        layout = FloatLayout()
        layout.add_widget(beforeImages())
        layout.add_widget(numComponentsSelect())
        layout.add_widget(pcaGraph())
        nextBtn = Button(text='Next', size_hint=(.25,.1),pos=(300,30))
        nextBtn.bind(on_press=self.changeScreens)
        layout.add_widget(nextBtn)
        self.add_widget(layout)

    def changeScreens(self, obj):
        self.manager.current = 'screen3'

class numComponentsSelect(FloatLayout):

    def __init__(self, **kwargs):
        super(numComponentsSelect, self).__init__(**kwargs)
        self.numComponents = Label(text='Number of components:  ',pos=(0,250))
        ''' this line doesn't seem to do anything but the binding doesn't work
         without it ''' 
        self.numComponents.text = 'Number of components: '
        compSlider = Slider(min=1, max=109,value=25,pos=(0,200))
        compSlider.bind(value=self.sliderChange)
        self.add_widget(self.numComponents)
        self.add_widget(compSlider)

        # after images
        layout = FloatLayout()
        self.before1 = Image(source='face1.png',pos=(-300,-100))
        #self.before1.source = 'face1.png'
        self.before2 = Image(source='face2.png',pos=(-170,-100))
        #self.before2.source = 'face2.png'
        layout.add_widget(self.before1)
        layout.add_widget(self.before2)
        self.add_widget(layout)

    def sliderChange(instance,obj,value):
        instance.numComponents.text = 'Number of components: ' + str(int(value))
        instance.before1.source='face2.png'
        instance.before2.source='face1.png'
        instance.numComponents.canvas.ask_update()
        instance._trigger_layout()

    def numUpdate(instance,obj,value):
        obj.text=value

class beforeImages(FloatLayout):

    def __init__(self, **kwargs):
        super(beforeImages, self).__init__(**kwargs)
        #self.rows=1
        self.add_widget(Image(source='face1.png',pos=(-300,100)))
        self.add_widget(Image(source='face2.png',pos=(-170,100)))


class pcaGraph(FloatLayout):

    def __init__(self, **kwargs):
        super(pcaGraph, self).__init__(**kwargs)
        graph = Graph(xLabel='X',ylabel='Y',x_ticks_minor=5, \
                x_ticks_major=25,y_ticks_major=1,y_grid_label=True, \
                x_grid_label=True,padding=5,x_grid=True,y_grid=True, \
                xmin=-0,xmax=100,ymin=-1,size_hint=(.6,.6),pos=(300,130))
        plot = MeshLinePlot(color=[1,0,0,1])
        plot.points = [(x,700/x) for x in range(1,101)]
        graph.add_plot(plot)
        self.add_widget(graph)

#if __name__ == "__main__":
 #   runPCA().run()

