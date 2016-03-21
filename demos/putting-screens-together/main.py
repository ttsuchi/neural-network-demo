import kivy

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from dataset import SelectingDataSet
from pca import RunPCA


class TestApp(App):
    def build(self):
        my_screenmanager = ScreenManager()
        screen1 = SelectingDataSet(name='screen1')
        screen2 = RunPCA(name='screen2')
        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)
        return my_screenmanager


if __name__ == '__main__':
    TestApp().run()
