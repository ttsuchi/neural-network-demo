from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class Example(App):

    def build(self):
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(30):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            layout.add_widget(btn)
        root = ScrollView()
        root.add_widget(layout)
        return root

if __name__ == '__main__':
    Example().run()
