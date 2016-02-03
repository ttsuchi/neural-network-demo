from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

class selectingDataSet(App):

    def build(self):
        layout = GridLayout(cols=4, row_force_default=True, row_default_height=40)
        button1 = Button(text='CAFE', size_hint_x=None, width=100, pos_hint={'x':.05, 'y':.2})
        button2 = Button(text='POFA', size_hint_x=None, width=100)
        button1.bind(on_press=self.clk)
        button2.bind(on_press=self.clk)
        
        l = Label(text="Select one of the data sets to load images",font_size=150)
        
        layout.add_widget(button1)
        layout.add_widget(button2)

        return layout


    def clk(self, obj):
        print("Hello World!")


    def callback():
        print 'Button is being pressed.'
        
if __name__ == '__main__':
    selectingDataSet().run()