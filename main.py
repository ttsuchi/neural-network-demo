import kivy

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import OptionProperty, BoundedNumericProperty, AliasProperty
from kivy.logger import Logger

from dataset import SelectDataSet
from pca import RunPCA
from training_parameters import TrainingParameters
from result import TrainingResult
from neural_network import PCAData

ALL_SCREENS = [SelectDataSet, RunPCA, TrainingParameters, TrainingResult]


class NeuralNetworkDemoApp(App):
    # Application properties
    # See https://kivy.org/docs/api-kivy.properties.html
    # for available kinds of properties.

    # The dataset
    dataset_name = OptionProperty("POFA", options=["CAFE", "POFA"])

    dataset_cache = {}

    def _load_dataset(self):
        if self.dataset_name not in NeuralNetworkDemoApp.dataset_cache.keys():
            filename = 'data/%s.pkl' % self.dataset_name.lower()
            import pickle
            Logger.info('Loading data from %s' % filename)
            with open(filename, 'r') as f:
                NeuralNetworkDemoApp.dataset_cache[self.dataset_name] = pickle.load(f)
        return NeuralNetworkDemoApp.dataset_cache[self.dataset_name]

    dataset = AliasProperty(_load_dataset, None, bind=['dataset_name'])
    maximum_pca_components = AliasProperty(lambda self: min(self.dataset.data.shape), None, bind=['dataset'])

    # PCA components (the max will be controlled by the maximum_pca_components)
    pca_components = BoundedNumericProperty(10, min=1)

    # PCA transformed data
    pca_data = AliasProperty(lambda self: PCAData(self.dataset), None, bind=['dataset'])

    # train inputs
    num_hidden_units = BoundedNumericProperty(10, min=1)
    num_valid_input = BoundedNumericProperty(0, min=0)
    num_test_data = BoundedNumericProperty(0, min=0)
    hidden_units_learning_rate = BoundedNumericProperty(0.1, min=0.001, max=1.0)
    output_units_learning_rate = BoundedNumericProperty(0.2, min=0.001, max=1.0)
    momentum = BoundedNumericProperty(0.2, min=0, max=1.0)
    epochs = BoundedNumericProperty(100, min=1, max=5000)
    minimum_rmse = BoundedNumericProperty(0, min=0.0, max=1.0)

    # the categories of training
    training = OptionProperty('Expression', options=['Gender', 'Expression', 'Identity'])

    #
    # Main Kivy code for building the application UI.
    #
    def build(self):
        '''Build the application UI.'''
        self.manager = ScreenManager()
        for i, screen_cls in enumerate(ALL_SCREENS):
            self.manager.add_widget(screen_cls(name='Screen %d' % (i + 1)))
        self.manager.current = 'Screen 1'

        # Dispatch all events in order to initialize UIs
        for property_name in self.properties():
            Logger.info('Initializing UI for %s' % property_name)
            self.property(property_name).dispatch(self)

        return self.manager

    # Manage the screen transitions
    def go_next(self):
        '''Go to the next screen.'''
        self.manager.transition.direction = 'left'
        Logger.info('Moving to ' + self.manager.next())
        self.manager.current = self.manager.next()

    def go_back(self):
        '''Go back one screen.'''
        self.manager.transition.direction = 'right'
        Logger.info('Moving to ' + self.manager.previous())
        self.manager.current = self.manager.previous()


if __name__ == '__main__':
    NeuralNetworkDemoApp().run()
