import kivy

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import OptionProperty, BoundedNumericProperty, AliasProperty
from kivy.logger import Logger

from dataset import SelectDataSet
from pca import RunPCA
from train import Train
from result import Example

ALL_SCREENS = [SelectDataSet, RunPCA, Train, Example]

class NeuralNetworkDemoApp(App):
    # Application properties
    # See https://kivy.org/docs/api-kivy.properties.html
    # for available kinds of properties.

    # The dataset
    dataset = OptionProperty("POFA", options=["CAFE", "POFA"])

    # Maximum number of PCA components allowed
    def _get_maximum_pca_components(self):
        # TODO replace this dummy code
        if self.dataset == 'POFA':
            return 50
        else:
            return 100

    maximum_pca_components = AliasProperty(_get_maximum_pca_components, None, bind=['dataset'])

    # PCA components (the max will be controlled by the maximum_pca_components)
    pca_components = BoundedNumericProperty(10, min=1)



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
