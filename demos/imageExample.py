from kivy.uix.image import Image
from kivy.app import App
class imageExample(App):
    def build(self):
        return Image(source='diagram.png')

if __name__ == '__main__':
    imageExample().run()
