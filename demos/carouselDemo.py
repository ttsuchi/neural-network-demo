from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class CarouselApp(App):
    def build(self):
        carousel = Carousel(direction='right')
        for i in range(10):
            layout = BoxLayout(orientation='vertical')
            image1 = AsyncImage(source=("http://placehold.it/480x270.png&text=slide-%d&.png" % i), allow_stretch=True)
            image2 = AsyncImage(source=("http://placehold.it/480x270.png&text=slide-%d&.png" % (i+1)), allow_stretch=True)
            layout.add_widget(image1)
            layout.add_widget(Label(text='Image %d' % i, font_size=30))
            layout.add_widget(image2)
            layout.add_widget(Label(text='Second Image %d' % (i+1), font_size=30))
            carousel.add_widget(layout)
        return carousel


CarouselApp().run()
