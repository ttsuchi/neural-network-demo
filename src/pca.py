from kivy.clock import mainthread
from kivy_garden_graph import Graph, LinePlot
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from numpy import *

kv = '''
BoxLayout:
    orientation: 'vertical'
    padding: [0, 10]
    Label:
        text:
            " Drag the slider to select the number of components you'd like to analyze.\\n" + \
            "The more components you select, the more variance your dataset will have."
        halign: 'center'
        size_hint: (1, 0.1)

    BoxLayout:
        orientation: 'vertical'
        size_hint: (1, 0.15)
        id: num_components_select
        Label:
            text: "Number of components: %d" % app.pca_components
            halign: 'center'
        AnchorLayout:
            anchor_x: 'center'
            Slider:
                size_hint: (.8, 1)
                min: 1
                max: app.maximum_pca_components
                value: app.pca_components
                on_value: app.pca_components = self.value

    BoxLayout:
        orientation: 'horizontal'
        padding: [30, 30]
        BoxLayout:
            size_hint: (0.35, 1)
            orientation: 'vertical'
            BoxLayout:
                orientation: 'vertical'
                id: before_images
                Label:
                    size_hint: (1, 0.2)
                    text: 'Original'
                    halign: 'center'
                BoxLayout:
                    orientation: 'horizontal'
                    PCAFaceImage:
                        dataset: app.dataset
                        index: 0
                    PCAFaceImage:
                        dataset: app.dataset
                        index: 1
            BoxLayout:
                orientation: 'vertical'
                id: after_images
                Label:
                    size_hint: (1, 0.2)
                    text: 'Reconstruction with %d components' % app.pca_components
                    halign: 'center'
                BoxLayout:
                    orientation: 'horizontal'
                    PCAFaceImage:
                        dataset: app.dataset
                        index: 0
                        pca_transformer: app.pca_transformer
                    PCAFaceImage:
                        dataset: app.dataset
                        index: 1
                        pca_transformer: app.pca_transformer

        PCAGraph:
            size_hint: (0.65, 1)
            id: pca_graph
            pca_data: app.pca_data
            maximum_pca_components: app.maximum_pca_components
            pca_components: app.pca_components
            padding: 5
            xlabel: 'Number of Components'
            xmin: 0
            xmax: app.maximum_pca_components
            x_ticks_minor: 5
            x_ticks_major: 25
            x_grid: True
            x_grid_label: True
            ylabel: 'Total Explained Variance'
            ymin: 0
            ymax: 1.0
            y_ticks_major: .25
            y_grid: True
            y_grid_label: True

    BoxLayout:
        size_hint: (1, .15)
        orientation: 'horizontal'
        AnchorLayout:
            anchor_x: 'right'
            anchor_y: 'center'
            padding: [10, 0]
            Button:
                text: 'Back'
                on_press: app.go_back()
                size_hint: (.6, .8)
        AnchorLayout:
            anchor_x: 'left'
            anchor_y: 'center'
            padding: [10, 0]
            Button:
                text: 'Next'
                on_press: app.go_next()
                size_hint: (.6, .8)
'''


class PCAFaceImage(Image):
    dataset = ObjectProperty()
    index = NumericProperty(-1)
    pca_transformer = ObjectProperty()

    def __init__(self, **kwargs):
        super(PCAFaceImage, self).__init__(**kwargs)
        self.bind(
            dataset=self.plot_image,
            index=self.plot_image,
            pca_transformer=self.plot_image
        )

    def plot_image(self, instance, value):
        if value is None or self.dataset is None or self.index < 0:
            return

        _, height, width = self.dataset['images'].shape
        self.texture = Texture.create(size=(width, height), colorfmt='luminance')

        image_data = self.dataset['images'][self.index]
        if self.pca_transformer is not None:
            if len(self.pca_transformer.mean_) != len(image_data.flatten()):
                return
            image_data = self.pca_transformer.reconstruct(image_data)

        self.texture.blit_buffer((image_data[::-1] * 255).astype(ubyte).tostring(), colorfmt='luminance',
                                 bufferfmt='ubyte')
        self.canvas.ask_update()


class PCAGraph(Graph):
    maximum_pca_components = NumericProperty()
    pca_components = NumericProperty()
    pca_data = ObjectProperty()

    def __init__(self, **kwargs):
        self._with_stencilbuffer = False # See https://github.com/kivy-garden/garden.graph/issues/7
        super(PCAGraph, self).__init__(**kwargs)
        self.pca_plot = LinePlot(color=[1, 1, 1, 1], line_width=3)
        self.vline = LinePlot(color=[0, 0, 1, 1], line_width=2)
        self.hline = LinePlot(color=[0, 0, 1, 1], line_width=2)
        [self.add_plot(p) for p in (self.pca_plot, self.vline, self.hline)]

        self.bind(
            maximum_pca_components=self.plot_pca_variance,
            pca_data=self.plot_pca_variance,
            pca_components=self.plot_pca_components,
        )

    @mainthread
    def plot_pca_variance(self, instance, value):
        if value is None \
                or self.pca_data is None \
                or self.maximum_pca_components < 0 \
                or self.pca_components < 0 \
                or self.pca_data.explained_variance.shape[0] != self.maximum_pca_components \
                or self.pca_components >= self.maximum_pca_components:
            return

        Logger.debug("Updating PCA graph for max %d with %s at %d" % (
            self.maximum_pca_components, str(self.pca_data.explained_variance.shape), self.pca_components))

        v = self.pca_data.explained_variance.cumsum()
        self.pca_plot.points = [(float(x), float(y)) for (x, y) in zip(arange(self.maximum_pca_components), v)]
        self.pca_plot.draw()
        self.plot_pca_components(instance, value)

    @mainthread
    def plot_pca_components(self, instance, value):
        if value is None \
                or self.pca_data is None \
                or self.maximum_pca_components < 0 \
                or self.pca_components < 0 \
                or self.pca_data.explained_variance.shape[0] != self.maximum_pca_components \
                or self.pca_components >= self.maximum_pca_components:
            return

        v = self.pca_data.explained_variance.cumsum()
        x_, y_ = float(self.pca_components), float(v[int(self.pca_components - 1)])
        self.vline.points = [(x_, 0.0), (x_, 1.0)]
        self.hline.points = [(0, y_), (float(self.maximum_pca_components) - 1, y_)]
        [p.draw() for p in (self.vline, self.hline)]


class RunPCA(Screen):
    def __init__(self, **kwargs):
        super(RunPCA, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
