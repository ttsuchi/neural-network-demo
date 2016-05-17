from kivy.app import App
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.graphics import Line

kv = '''
FloatLayout:
    FloatLayout:
        id: before_images
        Image:
            source: 'face1.png'
            pos: (-300, 78)
        Image:
            source: 'face2.png'
            pos: (-170, 78)
        Label:
            text: 'Original'
            pos: (-235, 170)

    FloatLayout:
        id: after_images
        Image:
            source: 'face1.png'
            pos: (-300, -110)
        Image:
            source: 'face2.png'
            pos: (-170, -110)
        Label:
            text: 'Reconstruction with %d components' % app.pca_components
            pos: (-235, -20)

    FloatLayout:
        id: num_components_select
        Slider:
            pos: (55, 190)
            size_hint: (.9, 1)
            min: 1
            max: app.maximum_pca_components
            value: app.pca_components
            on_value: app.pca_components = self.value
        Label:
            pos: (0, 215)
            text: "Number of components: %d" % app.pca_components

    PCAGraph:
        id: pca_graph
        padding: 5
        xlabel: 'Component number'
        x_grid: True
        xmin: 0
        xmax: app.maximum_pca_components
        x_grid_label:True
        x_ticks_minor: 5
        x_ticks_major: 10
        y_grid: True
        y_grid_label: True
        ylabel: 'Variance provided by additional component'
        y_ticks_major: .5
        y_ticks_minor: .1
        ymin: 0
        ymax: 1.0
        size_hint: (.55, .60)
        pos: (325, 100)
    Button:
        text: 'Back'
        size_hint: (.25, .1)
        pos: (190, 30)
        on_press: app.go_back()
    Button:
        text: 'Next'
        size_hint: (.25, .1)
        pos: (410, 30)
        on_press: app.go_next()
    Label:
        text:
            " Drag the slider to select the number of components you'd like to analyze.\\n" + \
            "The more components you select, the more variance your dataset will have."
        pos: (0, 265)
'''


class PCAGraph(Graph):
    firstline = True
    def __init__(self, **kwargs):
        super(PCAGraph, self).__init__(**kwargs)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(float(x), 1.0 / float(x)) for x in range(1, int(self.xmax))]
        self.add_plot(plot)
        Logger.info("Added Graph")

        # Now manually register line drawing when the pca_components change
        def on_pca_components(caller, value):
            Logger.info('Drawing %d' % value)
            with self.canvas:
                if self.firstline:
                    self.line = Line(points=[445, 150, 445, 450], width=1)
                    self.firstline = False
                graph_width = 390.0
                graph_zero = 365.0
                width_one = graph_width / float(self.xmax) 
                components_x = graph_zero + value*width_one
                self.line.points=[components_x, 150, components_x, 450]
                # this commented line goes across the bottom of the graph
                # Line(points=[365, 150, 755, 150], width=1)

        App.get_running_app().bind(pca_components=on_pca_components)


class RunPCA(Screen):
    def __init__(self, **kwargs):
        super(RunPCA, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
