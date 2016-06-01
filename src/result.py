import threading

from kivy.app import App
from kivy.clock import mainthread
from kivy.garden.graph import Graph, LinePlot
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from numpy import *

from neural_network import NeuralNetwork

kv = '''
BoxLayout:
    orientation: 'vertical'
    padding: [30]
    BoxLayout:
        size_hint: (1, .4)
        orientation: 'horizontal'
        BoxLayout:
            size_hint: (.4, 1)
            orientation: 'vertical'
            BoxLayout:
                orientation: 'vertical'
                AnchorLayout:
                    anchor_x: 'center'
                    anchor_y: 'center'
                    Button:
                        id: back_button
                        text: 'Back'
                        size_hint: (.8, .5)

                AnchorLayout:
                    anchor_x: 'center'
                    anchor_y: 'center'
                    Button:
                        id: pause_button
                        text: 'Pause'
                        size_hint: (.8, .5)

        BoxLayout:
            orientation: 'vertical'
            size_hint: (.6, 1)
            TrainingGraph:
                id: rmse_graph
                padding: 3
                xlabel: 'Epochs'
                xmin: 0
                xmax: app.epochs
                x_ticks_major: 250
                x_grid: True
                x_grid_label: True
                ylabel: 'RMSE'
                ymin: 0
                ymax: 2.0
                y_ticks_major: .5
                y_grid: True
                y_grid_label: True

            TrainingGraph:
                id: cerr_graph
                padding: 3
                xlabel: 'Epochs'
                xmin: 0
                xmax: app.epochs
                x_ticks_major: 250
                x_grid: True
                x_grid_label: True
                ylabel: 'Cls.Err.'
                ymin: 0
                ymax: 1.0
                y_ticks_major: .25
                y_grid: True
                y_grid_label: True

    GridLayout:
        id: table_header
        disabled: True
        cols: 1
        spacing: 15
        row_force_default: True
        row_default_height: 50
        size_hint_y: None
        height: self.minimum_height

        Label:
            text: '      Actual Image                              Network Image                      Guess               Answer             Correct?'

    ScrollView:
        id: result_scrollview
        disabled: True
        size_hint: (1, .55)
        do_scroll_x: False
        do_scroll_y: True
        scroll_type: ['bars', 'content']
        bar_width: 20
        bar_color: [1, 1, 1, 1]
        bar_inactive_color: [1, 1, 1, 1]
        scroll_wheel_distance: 50

        GridLayout:
            id: result_grid
            cols: 5
            spacing: 15
            row_force_default: True
            row_default_height: 50
            size_hint_y: None
            height: self.minimum_height

'''


class TrainingGraph(Graph):
    def __init__(self, **kwargs):
        self._with_stencilbuffer = False  # See https://github.com/kivy-garden/garden.graph/issues/7
        super(TrainingGraph, self).__init__(**kwargs)
        self.train_plot = LinePlot(color=[0, 0, 1, 1], line_width=2)
        self.test_plot = LinePlot(color=[1, 1, 1, 1], line_width=2)
        [self.add_plot(p) for p in [self.train_plot, self.test_plot]]

    def check_value(self, value):
        return True

    @mainthread
    def plot(self, epoch, epochs, err, minimum_rmse):
        if epoch < 1:
            return

        self.train_plot.points = [(float(x), float(y)) for x, y in zip(arange(epoch), err[:, 0])]
        self.test_plot.points  = [(float(x), float(y)) for x, y in zip(arange(epoch), err[:, 1])]
        [p.draw() for p in (self.train_plot, self.test_plot)]


class ResultImage(Image):
    def __init__(self, image_data, **kwargs):
        height, width = image_data.shape
        super(ResultImage, self).__init__(size=(width, height), **kwargs)
        self.texture = Texture.create(size=(width, height), colorfmt='luminance')
        self.texture.blit_buffer((image_data * 255).astype(ubyte).tostring(), colorfmt='luminance', bufferfmt='ubyte')
        self.texture.flip_vertical()


class TrainingResult(Screen):
    def __init__(self, **kwargs):
        super(TrainingResult, self).__init__(**kwargs)
        contents = Builder.load_string(kv)
        self.add_widget(contents)
        self.ids = contents.ids

        # Bind the network
        self.network = NeuralNetwork(App.get_running_app())

        # Bind the buttons
        def back_pressed(instance):
            self.pause_training(instance)
            App.get_running_app().go_back()

        self.ids.back_button.bind(on_press=back_pressed)

        # Start the training thread when the screen is displayed
        self.bind(on_enter=self.start_training)

    # Manage network training
    def start_training(self, instance):
        Logger.info('Starting training')
        self.network.reset_training()
        self.resume_training(self)

    def resume_training(self, instance):
        Logger.info('Resuming training')
        self.clear_results()

        self.training_paused = False
        pause_button = self.ids.pause_button
        pause_button.text = 'Pause'
        pause_button.unbind(on_press=self.resume_training)
        pause_button.bind(on_press=self.pause_training)

        # Make sure the thread stops on application exit
        App.get_running_app().unbind(on_stop=self.pause_training)
        App.get_running_app().bind(on_stop=self.pause_training)

        threading.Thread(target=self._run_training).start()

    def pause_training(self, instance):
        self.training_paused = True
        pause_button = self.ids.pause_button
        pause_button.text = 'Resume'
        pause_button.unbind(on_press=self.pause_training)
        pause_button.bind(on_press=self.resume_training)

        self.display_results()

    def clear_results(self):
        '''Clears all children of the grid, except for the header labels.'''
        grid = self.ids.result_grid
        grid.clear_widgets()

    @mainthread
    def display_results(self):
        '''Shows the result of the training in the grid.'''
        grid = self.ids.result_grid

        predictions, reconstructions = self.network.predict_all()
        predictions_correct = predictions == self.network.targets
        for is_test, image, reconstruction, prediction, target, prediction_correct in \
                zip(self.network.idx_test, self.network.app.dataset['images'], reconstructions, predictions,
                    self.network.targets, predictions_correct):
            # First column: Actual image
            grid.add_widget(ResultImage(image))

            # Second column: Network's image reconstruction
            grid.add_widget(ResultImage(reconstruction))

            # Third column: Network Representation
            grid.add_widget(Label(text=self.network.target_names[prediction + 1], size_hint=(.5, .5)))

            # Fourth column: Actual representation
            grid.add_widget(Label(text=self.network.target_names[target + 1], size_hint=(.5, .5)))

            # Fifth column: correct/incorrect
            grid.add_widget(Label(text='%d' % prediction_correct, size_hint=(.5, .5)))

        self.ids.result_scrollview.disabled = False
        self.ids.table_header.disabled = False

    def _run_training(self):
        for epoch, epochs, rmse, cerr, is_last in self.network.resume_training():
            if (epoch % 10) == 1 or is_last:
                Logger.debug('epoch: %d, rmse shape: %s' % (epoch, str(rmse.shape)))
                self.ids.rmse_graph.plot(epoch, epochs, rmse, self.network.minimum_rmse)
                self.ids.cerr_graph.plot(epoch, epochs, cerr, self.network.minimum_rmse)

            if self.training_paused:
                break

        Logger.info('Exit training thread')
        self.display_results()
