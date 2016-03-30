import kivy

kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from selectingDataSet import SelectingDataSet
from pca import RunPCA
from train import Train
from scrollBar import Example


class TestApp(App):
    def build(self):
        my_screenmanager = ScreenManager()
        screen1 = SelectingDataSet(name='screen1')
        screen2 = RunPCA(name='screen2')
        screen3 = Train(name='screen3')
        screen4 = Example(name='screen4')
        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)
        my_screenmanager.add_widget(screen3)
        my_screenmanager.add_widget(screen4)
        return my_screenmanager


if __name__ == '__main__':
    TestApp().run()
