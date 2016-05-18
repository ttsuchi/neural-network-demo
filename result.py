from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.screenmanager import Screen


class Example(Screen):

    def __init__(self, **kwargs):
        super(Example, self).__init__(**kwargs)
        layout = GridLayout(cols=5, spacing=15, row_force_default=True, 
                row_default_height=75, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        label_layout = FloatLayout()


        # back button

        backButton = Button(text='Back', size_hint=(.15, .1), pos=(60,500))
        label_layout.add_widget(backButton)

        backButton.bind(on_press=self.goBack)


        graph = Graph(xLabel='X',ylabel='Y',x_ticks_minor=5, \
                x_ticks_major=25,y_ticks_major=1,y_grid_label=True, \
                x_grid_label=True,padding=5,x_grid=True,y_grid=True, \
                xmin=-0,xmax=100,ymin=-1,size_hint=(.5,.5),pos=(200,275))
        plot = MeshLinePlot(color=[1,0,0,1])
        plot.points = [(x,700/x) for x in range(1,101)]
        graph.add_plot(plot)

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
        self.add_widget(label_layout)

    def goBack(self,obj):
            App.get_running_app().go_back()

#if __name__ == '__main__':
 #   Example().run()
