'''Contains graph components using Matplotlib.'''
import matplotlib

matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
from kivy.uix.boxlayout import BoxLayout

import matplotlib.pyplot as plt


class ImageFromData(BoxLayout):
    '''Displays the given image data.'''

    def __init__(self, **kwargs):
        super(ImageFromData, self).__init__(**kwargs)
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
        if not self.check_value(value):
            return

        image_data = self.get_image_data()
        if image_data is None:
            return

        ax = self.ax
        ax.imshow(image_data, aspect='auto', cmap='gray')
        ax.set_axis_off()

        self.fig.canvas.draw()


class Graph(BoxLayout):
    '''Displays Matplotlib graph canvas.'''

    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)
        self.fig, self.ax = plt.subplots(facecolor='black')
        self.ax.set_axis_bgcolor('black')
        self.add_widget(FigureCanvas(self.fig))

    def _redraw_graph(self, instance, value):
        if not self.check_value(value):
            return

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
