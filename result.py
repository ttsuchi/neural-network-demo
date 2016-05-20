import threading

from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from numpy import *

from graph import Graph

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
            epochs: app.epochs
            minimum_rmse: app.minimum_rmse

    ScrollView:
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


class TrainingGraph(Graph):
    epochs = NumericProperty()
    minimum_rmse = NumericProperty(0.0)
    epoch = NumericProperty()

    def __init__(self, **kwargs):
        super(TrainingGraph, self).__init__(**kwargs)
        self.rmse = None
        self.cerr = None

    def check_value(self, value):
        return True

    @mainthread
    def redraw(self, instance):
        self._redraw_graph(instance, None)

    def draw_graph(self, ax):
        self.epoch = len(self.rmse)
        if self.epoch < 1:
            return

        ax.plot(arange(self.epoch), self.rmse, color='blue', linewidth=3)
        ax.plot(arange(self.epoch), self.cerr, color='red', linewidth=3)
        ax.legend(['RMSE', 'CErr'])

        ax.set_xlabel('Epochs')
        ax.set_ylabel('RMSE')
        ax.set_ylim([0, 1.0])

        # TODO: figure out whether to use number of epochs or minimum rmse
        if self.epochs > 0:
            ax.set_xlim([0, self.epochs])
        else:
            ax.axhline(self.minimum_rmse, color='blue', linewidth=1, linestyle='--')


class TrainingResult(Screen):
    def __init__(self, **kwargs):
        super(TrainingResult, self).__init__(**kwargs)
        contents = Builder.load_string(kv)
        self.add_widget(contents)
        self.ids = contents.ids

        # Sample content
        grid = self.ids.result_grid
        for j in range(157):
            # First column: Actual image
            grid.add_widget(Image(source='face1.png'))

            # Second column: Network's image reconstruction
            grid.add_widget(Image(source='face1.png'))

            # Third column: Network Representation
            grid.add_widget(Label(text='mad', size_hint=(.5, .5)))

            # Fourth column: Actual representation
            grid.add_widget(Label(text='happy', size_hint=(.5, .5)))

            # Fifth column: correct/incorrect
            grid.add_widget(Label(text='1', size_hint=(.5, .5)))

        # Bind the buttons
        def back_pressed(instance):
            self._pause_training(instance)
            App.get_running_app().go_back()
        self.ids.back_button.bind(on_press=back_pressed)

        # Start the training thread when the screen is displayed
        self.bind(on_enter=self._start_training)

    # Manage network training
    def _start_training(self, instance):
        Logger.info('Starting training')
        # Reset the epochs
        self.ids.training_graph.epoch = 0
        self._resume_training(self)

    def _resume_training(self, instance):
        Logger.info('Resuming training')
        self.pause_training = False
        pause_button = self.ids.pause_button
        pause_button.text = 'Pause'
        pause_button.unbind(on_press=self._resume_training)
        pause_button.bind(on_press=self._pause_training)

        # Make sure the thread stops on application exit
        App.get_running_app().unbind(on_stop=self._pause_training)
        App.get_running_app().bind(on_stop=self._pause_training)

        threading.Thread(target=self._do_train).start()

    def _pause_training(self, instance):
        self.pause_training = True
        pause_button = self.ids.pause_button
        pause_button.text = 'Resume'
        pause_button.unbind(on_press=self._pause_training)
        pause_button.bind(on_press=self._resume_training)

    def _do_train(self):
        app = App.get_running_app()
        graph = self.ids.training_graph

        import time
        from numpy import exp
        epoch = graph.epoch
        while epoch < app.epochs:
            if self.pause_training:
                break
            time.sleep(1)

            xs = arange(epoch) / 5.0
            rmse = exp(-xs)
            cerr = 0.5 * (exp(-xs))
            graph.rmse = rmse
            graph.cerr = cerr
            graph.redraw(self)

            epoch += 1
        Logger.info('Exit training thread')
