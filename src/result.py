import threading

import matplotlib.pyplot as plt
from kivy.app import App
from kivy.clock import mainthread
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
from kivy.graphics.texture import Texture
from kivy.graphics.vertex_instructions import Rectangle
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

        TrainingGraph:
            id: training_graph
            size_hint: (.6, 1)

    ScrollView:
        id: result_scrollview
        disabled: True
        size_hint: (1, .6)
        do_scroll_x: False
        do_scroll_y: True
        scroll_type: ['bars', 'content']
        bar_width: 10

        GridLayout:
            id: result_grid
            cols: 5
            spacing: 15
            row_force_default: True
            row_default_height: 75
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: 'Actual Image'
            Label:
                text: 'Network Image'
            Label:
                text: 'Network Portrayal'
            Label:
                text: 'Actual Portrayal'
            Label:
                text: 'Correct?'
'''


class TrainingGraph(FigureCanvas):
    def __init__(self, **kwargs):
        fig, self.axs = plt.subplots(2, sharex=True)
        super(TrainingGraph, self).__init__(fig, **kwargs)
        self.rmse = None
        self.cerr = None

    def check_value(self, value):
        return True

    @mainthread
    def plot(self, epoch, epochs, rmse, cerr, minimum_rmse):
        if epoch < 1:
            return

        for ax in self.axs:
            ax.cla()
        ax1, ax2 = self.axs

        ax1.plot(arange(epoch), rmse[:, 0], label='Test', color='blue', ls="-")
        ax1.plot(arange(epoch), rmse[:, 1], label='Train', color='blue', ls="--")
        ax1.set_ylabel('RMSE')
        ax1.set_ylim([0, 2.0])
        ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=2, mode="expand", borderaxespad=0.)
        # TODO: figure out whether to use number of epochs or minimum rmse
        if minimum_rmse > 0:
            ax1.axhline(self.minimum_rmse, color='blue', linewidth=1, linestyle='--')

        ax2.plot(arange(epoch), cerr[:, 0], color='white', ls="-")
        ax2.plot(arange(epoch), cerr[:, 1], color='white', ls="--")
        ax2.set_ylabel('Class. Err')
        ax2.set_ylim([0, 1.0])

        for ax in self.axs:
            ax.set_xlabel('Epochs')
            ax.set_xlim([0, epochs])
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()

        self.draw()


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

        # Sample content
        # grid = self.ids.result_grid
        # for j in range(157):
        #     # First column: Actual image
        #     grid.add_widget(Image(source='face1.png'))
        #
        #     # Second column: Network's image reconstruction
        #     grid.add_widget(Image(source='face1.png'))
        #
        #     # Third column: Network Representation
        #     grid.add_widget(Label(text='mad', size_hint=(.5, .5)))
        #
        #     # Fourth column: Actual representation
        #     grid.add_widget(Label(text='happy', size_hint=(.5, .5)))
        #
        #     # Fifth column: correct/incorrect
        #     grid.add_widget(Label(text='1', size_hint=(.5, .5)))

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

    def _run_training(self):
        graph = self.ids.training_graph
        for epoch, epochs, rmse, cerr, is_last in self.network.resume_training():
            if (epoch % 10) == 1 or is_last:
                Logger.debug('epoch: %d, rmse shape: %s' % (epoch, str(rmse.shape)))
                graph.plot(epoch, epochs, rmse, cerr, self.network.minimum_rmse)

            if self.training_paused:
                break

        Logger.info('Exit training thread')
        self.display_results()
