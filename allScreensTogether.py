import kivy

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.garden.graph import Graph, MeshLinePlot


class SelectingDataSet(Screen):
    def __init__(self, **kwargs):
        super(SelectingDataSet, self).__init__(**kwargs)

        layout = FloatLayout(cols=3, row_force_default=True, row_default_height=40)

        # instantiate the buttons
        cafeButton = Button(text='CAFE', size_hint=(.2, .1), pos_hint={'x': .2, 'center_y': .6})
        pofaButton = Button(text='POFA', size_hint=(.2, .1), pos_hint={'center_x': .7, 'center_y': .6})
        loadButton = Button(text='Next', size_hint=(.25, .15), pos_hint={'x': .75, 'y': 0})

        # add buttons to the layout
        layout.add_widget(cafeButton)
        layout.add_widget(pofaButton)
        layout.add_widget(loadButton)

        # instantiate the labels
        title = Label(text="Select one of the data sets to load images", font_size=30,
                      pos_hint={'x': 0, 'center_y': .9})
        cafeDescription = Label(text="The California Facial Expressions (CAFE)", font_size=15, pos_hint={'x': -.2, 'center_y': .5})
        pofaDescription = Label(text="The Pictures of Facial Affect (POFA)", font_size=15, pos_hint={'x': .2, 'center_y': .5})

        # add labels to the layout
        layout.add_widget(title)
        layout.add_widget(cafeDescription)
        layout.add_widget(pofaDescription)

        # binding the buttons to the clk method
        cafeButton.bind(on_press=self.clk)
        pofaButton.bind(on_press=self.clk)
        loadButton.bind(on_press=self.changer)

        self.add_widget(layout)

    def changer(self, *args):
        self.manager.current = 'screen2'

    def clk(self, obj):
        print("Hello World!")


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


class RunPCA(Screen):
    def __init__(self, **kwargs):
        super(RunPCA, self).__init__(**kwargs)

        layout = FloatLayout()
        #layout.add_widget(beforeImages())
        layout.add_widget(NumComponentsSelect())
        #layout.add_widget(pcaGraph())
        nextBtn = Button(text='Next', size_hint=(.25, .1), pos=(300, 30))
        nextBtn.bind(on_press=self.changer2)
        layout.add_widget(nextBtn)
        self.add_widget(layout)
        
    def changer2(self, *args):
        self.manager.current = 'screen3'



class train(Screen):
    def __init__(self, **kwargs):
        super(train, self).__init__(**kwargs)

 #      textInput = TextInput(text = 'hello')
        
        # Main layout for gui
        layout = FloatLayout()
        
        # Buttons for layout
        layout.add_widget(Button(text='Train for gender', size_hint=(.2, .1), pos_hint={'x': .1, 'center_y': .83}))
        layout.add_widget(Button(text='Train for expression', size_hint=(.2, .1), pos_hint={'x': .4, 'center_y': .83}))
        layout.add_widget(Button(text='Train for identity', size_hint=(.2, .1), pos_hint={'center_x': .8, 'center_y': .83}))
        layout.add_widget(Button(text='Previous'
            , size_hint=(.2, .1), pos_hint={'x': .15, 'center_y': .15}))
        trainButton = Button(text='Train', size_hint=(.2, .1), pos_hint={'x': .6, 'center_y': .15})
        layout.add_widget(trainButton)
        trainButton.bind(on_press=self.changer3)




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

        self.add_widget(layout)
        #return layout

    def changer3(self, *args):
        self.manager.current = 'screen4'







class scrollBar(Screen):

    def __init__(self, **kwargs):
        super(scrollBar, self).__init__(**kwargs)

        layout = GridLayout(cols=5, spacing=15, row_force_default=True, 
                row_default_height=75, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        label_layout = FloatLayout()
        graph = Graph(xLabel='X',ylabel='Y',x_ticks_minor=5, \
                        x_ticks_major=25,y_ticks_major=1,y_grid_label=True, \
                        x_grid_label=True,padding=5,x_grid=True,y_grid=True, \
                        xmin=-0,xmax=100,ymin=-1,size_hint=(.5,.5),pos=(200,275))
        plot = MeshLinePlot(color=[1,0,0,1])
        plot.points = [(x,700/x) for x in range(1,101)]
        graph.add_plot(plot)
        label_layout.add_widget(graph)








        layout.bind(minimum_height=layout.setter('height'))

        label_layout.add_widget(Label(text='Actual Image', size_hint=(.2,.1), 
            pos_hint={'x':.04, 'center_y': .45}))
        label_layout.add_widget(Label(text='Network Image', size_hint=(.2,.1),
            pos_hint={'x':.31, 'center_y': .45}))
        label_layout.add_widget(Label(text='Network Portrayal', size_hint=(.2,.1),
            pos_hint={'x':.51, 'center_y': .45}))
        label_layout.add_widget(Label(text='Actual Portrayal', size_hint=(.2,.1),
            pos_hint={'x':.68, 'center_y': .45}))
        label_layout.add_widget(Label(text='Correct?', size_hint=(.2,.1),
            pos_hint={'x':.82, 'center_y': .45}))

        for j in range(157):
            #First column: Actual image
          layout.add_widget(Image(source='face1.png'))

          #Second column: Network's image reconstruction
          layout.add_widget(Image(source='face1.png'))

          #Third column: Network Representation
          layout.add_widget(Label(text='mad', size_hint=(.5,.5)))

          #Fourth column: Actual representation
          layout.add_widget(Label(text='happy', size_hint=(.5,.5)))

          #Fifth column: correct/incorrect
          layout.add_widget(Label(text='1', size_hint=(.5,.5)))

        root = ScrollView(size_hint=(1, .4))





        root.add_widget(layout)
        root.bar_width = 10
        label_layout.add_widget(root)
        #return label_layout








class TestApp(App):
    def build(self):
        my_screenmanager = ScreenManager()
        screen1 = SelectingDataSet(name='screen1')
        screen2 = RunPCA(name='screen2')
        screen3 = train(name='screen3')
        screen4 = scrollBar(name='screen4')
        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)
        my_screenmanager.add_widget(screen3)
        my_screenmanager.add_widget(screen4)
        return my_screenmanager


if __name__ == '__main__':
    TestApp().run()
