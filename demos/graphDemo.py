import kivy
kivy.require('1.9.1')

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import time
import threading

from numpy import *
import matplotlib.pyplot as plt

class AnimatingGraphDemo(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        button = Button(text='Press me')
        button.bind(on_press=lambda instance: threading.Thread(target=self._schedule).start())
        layout.add_widget(button)
        layout.add_widget(Button(text='This does nothing'))

        self.fig, self.ax = plt.subplots()
        layout.add_widget(self.fig.canvas)
        return layout

    def _schedule(self, worker = None):
        if worker is None:
            worker = self.worker_loop()
        if next(worker, None) is not None:
            Clock.schedule_once(lambda dt: self._schedule(worker))

    def worker_loop(self):
        for t in range(20):
            # do some calculation here
            data = power(linspace(0, 2.0, 100), t / 10.0)
            # Simulate a long calculation
            time.sleep(1)

            self.update_plot(data, 't = %d' % t)

            yield True

    @mainthread
    def update_plot(self, data, title):
        self.ax.cla()
        self.ax.plot(linspace(0, 2.0, 100), data)
        self.ax.set_title(title)
        self.fig.canvas.draw()

if __name__ == '__main__':
    AnimatingGraphDemo().run()
