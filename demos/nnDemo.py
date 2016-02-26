from threading import Thread

from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.uix.button import Button

from neural_network import create_network

kv = '''
BoxLayout:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (95, 60)
        play: False
        allow_stretch: True
        keep_ratio: True
    ProgressBar:
        id: run_bar
        max: 1.0
        height: '12dp'
        width: 0.8

    RunButton:
        text: 'Run'
        size_hint_y: None
        height: '48dp'
'''


class RunButton(Button):
    def on_press(self, *args):
        Thread(target=self.run).start()

    def run(self):
        camera = App.get_running_app().root.ids.camera
        if not camera.play:
            self.disabled = True
            net = create_network(target='expression')
            epochs = 1e3
            for rmse, cerr, t, epochs in net.train(epochs=epochs):
                App.get_running_app().update_progress(float(t + 1) / float(epochs))

            self.text = 'Predict'
            camera.play = True
            self.disabled = False

        else:
            print(camera.texture.size)
            pixels = camera.texture.pixels
            print(pixels)


class NNDemo(App):
    @mainthread
    def update_progress(self, n):
        self.root.ids.run_bar.value = n

    def build(self):
        return Builder.load_string(kv)


NNDemo().run()
