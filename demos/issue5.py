from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

class Example(App):

    def build(self):
        layout = GridLayout(cols=5, spacing=15, row_force_default=True, 
          row_default_height=75, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        label_layout = FloatLayout()

        layout.bind(minimum_height=layout.setter('height'))

        label_layout.add_widget(Label(text='Actual Image', size_hint=(.2,.1), 
          pos_hint={'x':.04, 'center_y': .45}))
        label_layout.add_widget(Label(text='Network Image', size_hint=(.2,.1),
          pos_hint={'x':.31, 'center_y': .45}))
        label_layout.add_widget(Label(text='Network Portrayal', size_hint=(.2,.1),
          pos_hint={'x':.52, 'center_y': .45}))
        label_layout.add_widget(Label(text='Actual Portrayal', size_hint=(.2,.1),
          pos_hint={'x':.70, 'center_y': .45}))
        label_layout.add_widget(Label(text='Correct?', size_hint=(.2,.1),
          pos_hint={'x':.83, 'center_y': .45}))

        for j in range(157):
          #First column: Actual image
          layout.add_widget(Image(source='face1.png'))

          #Second column: Network's image reconstruction
          layout.add_widget(Image(source='face1.png'))

          #Third column: Network Representation
          layout.add_widget(Label(text='mad', size_hint=(.5,.5)))

          #Fourth column: Actual representation
          layout.add_widget(Label(text='happy', size_hint=(.5,.5)))

          #Fifth column: correct/incorrect
          layout.add_widget(Label(text='1', size_hint=(.5,.5)))

        root = ScrollView(size_hint=(1, .4))
        root.add_widget(layout)
        root.bar_width = 10
        label_layout.add_widget(root)
        return label_layout

if __name__ == '__main__':
    Example().run()
