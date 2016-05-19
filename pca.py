import matplotlib

matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import NumericProperty, ObjectProperty

import matplotlib.pyplot as plt
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
                    MPLImage:
                        dataset: app.dataset
                        image_index: 0
                    MPLImage:
                        dataset: app.dataset
                        image_index: 1
            BoxLayout:
                orientation: 'vertical'
                id: after_images
                Label:
                    size_hint: (1, 0.2)
                    text: 'Reconstruction with %d components' % app.pca_components
                    halign: 'center'
                BoxLayout:
                    orientation: 'horizontal'
                    MPLImage:
                        dataset: app.dataset
                        image_index: 0
                        pca_data: app.pca_data
                        pca_components: app.pca_components
                    MPLImage:
                        dataset: app.dataset
                        image_index: 1
                        pca_data: app.pca_data
                        pca_components: app.pca_components

        MPLGraph:
            size_hint: (0.65, 1)
            id: pca_graph
            padding: 5
            pca_data: app.pca_data
            maximum_pca_components: app.maximum_pca_components
            pca_components: app.pca_components

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


class MPLImage(BoxLayout):
    dataset = ObjectProperty()
    image_index = NumericProperty(-1)
    pca_data = ObjectProperty(rebind=True)
    pca_components = NumericProperty()

    def __init__(self, **kwargs):
        super(MPLImage, self).__init__(**kwargs)
        self.fig, self.ax = plt.subplots(facecolor='black')
        self.ax.set_axis_bgcolor('black')
        self.add_widget(FigureCanvas(self.fig))

        self.bind(
            dataset=self._redraw_graph,
            image_index=self._redraw_graph,
            pca_components=self._redraw_graph,
            pca_data=self._redraw_graph
        )

    def _redraw_graph(self, instance, value):
        if value is None or self.dataset is None or self.image_index < 0:
            return

        image_size = self.dataset.images.shape[1:]
        image = self.dataset.images[self.image_index]

        if self.pca_data is not None:
            image_data = image.flatten()
            if len(image_data) != self.pca_data.V.shape[1]:
                Logger.info('Incompatible image data size: %d vs %s' % (len(image_data), str(self.pca_data.V.shape)))
                return
            image = self.pca_data.reconstruct(image.flatten(), self.pca_components).reshape(image_size)

        ax = self.ax
        ax.imshow(image, aspect='normal', cmap='gray')
        ax.set_axis_off()

        self.fig.canvas.draw()


class MPLGraph(BoxLayout):
    maximum_pca_components = NumericProperty()
    pca_components = NumericProperty()
    pca_data = ObjectProperty(rebind=True)

    def __init__(self, **kwargs):
        super(MPLGraph, self).__init__(**kwargs)
        self.fig, self.ax = plt.subplots(facecolor='black')
        self.ax.set_axis_bgcolor('black')
        self.add_widget(FigureCanvas(self.fig))

        self.bind(
            maximum_pca_components=self._redraw_graph,
            pca_components=self._redraw_graph,
            pca_data=self._redraw_graph
        )

    def _redraw_graph(self, instance, value):
        if value is None or self.pca_data is None or self.maximum_pca_components == 0 or self.pca_components == 0:
            return

        if self.pca_data.explained_variance.shape[
            0] != self.maximum_pca_components or self.pca_components >= self.maximum_pca_components:
            return

        Logger.info("Updating PCA graph for max %d with %s at %d" % (
        self.maximum_pca_components, str(self.pca_data.explained_variance.shape), self.pca_components))

        ax = self.ax
        ax.cla()
        self.draw_graph(self.ax)

        # Clean up the axes
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        self.fig.canvas.draw()

    def draw_graph(self, ax):
        v = self.pca_data.explained_variance.cumsum()
        ax.plot(arange(self.maximum_pca_components), v, color='white', linewidth=5)

        ax.set_xlabel('Number of Components')
        ax.set_ylabel('Total Explained Variance')
        ax.set_xlim([0, self.maximum_pca_components])
        ax.set_ylim([0, 1.0])
        ax.axhline(v[self.pca_components - 1], color='blue', linewidth=1)

        from numpy.linalg.linalg import LinAlgError
        try:
            ax.axvline(self.pca_components, color='blue', linewidth=3)
        except LinAlgError:
            pass


class RunPCA(Screen):
    def __init__(self, **kwargs):
        super(RunPCA, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
