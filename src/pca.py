import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
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

        self.texture.blit_buffer((image_data[::-1] * 255).astype(ubyte).tostring(), colorfmt='luminance', bufferfmt='ubyte')
        self.canvas.ask_update()


class PCAGraph(FigureCanvas):
    maximum_pca_components = NumericProperty()
    pca_components = NumericProperty()
    pca_data = ObjectProperty()

    def __init__(self, **kwargs):
        fig, ax = plt.subplots()
        super(PCAGraph, self).__init__(fig, **kwargs)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        self.ax = ax

        self.bind(
            maximum_pca_components=self.plot_pca_variance,
            pca_components=self.plot_pca_variance,
            pca_data=self.plot_pca_variance
        )

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

        ax = self.ax
        ax.cla()
        v = self.pca_data.explained_variance.cumsum()
        ax.plot(arange(self.maximum_pca_components), v)

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
        self.draw()


class RunPCA(Screen):
    def __init__(self, **kwargs):
        super(RunPCA, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
