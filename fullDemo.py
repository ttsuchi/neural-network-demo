import selectingDataSet.py
import pca.py
import train.py
import scrollBar.py
from kivy.uix.screenmanager import ScreenManager, Screen
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.lang import Builder

class TestApp(App):
    def build(self):
        my_screenmanager = ScreenManager()
        screen1 = SelectingDataSet(name='screen1')
        screen2 = RunPCA(name='screen2')
        screen3 = train(name='screen3')
        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)
        my_screenmanager.add_widget(screen3)
        return my_screenmanager


if __name__ == '__main__':
    TestApp().run()
