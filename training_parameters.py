from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

kv = '''
FloatLayout:

    ToggleButton:
        text: 'Train for Gender'
        pos_hint: {'x':.1, 'center_y': .83}
        on_press: app.training = 'Gender'
        state: 'down' if app.training == 'Gender' else 'normal'
        size_hint: (.2, .1)
        group: 'training'
        allow_no_selection: False


    ToggleButton:
        text: 'Train for Expression'
        pos_hint: {'x': .4, 'center_y': .83}
        on_press: app.training = 'Expression'
        state: 'down' if app.training == 'Expression' else 'normal'
        size_hint: (.2, .1)
        group: 'training'
        allow_no_selection: False


    ToggleButton:
        text: 'Train for Identity'
        pos_hint: {'center_x': .8, 'center_y': .83}
        on_press: app.training = 'Identity'
        state: 'down' if app.training == 'Identity' else 'normal'
        size_hint: (.2, .1)
        group: 'training'
        allow_no_selection: False



    Button:
        text: 'Train'
        size_hint: (.25, .1)
        pos: (410, 30)
        on_press: app.go_next()

    Button:
        text: 'Back'
        size_hint: (.25, .1)
        pos: (190, 30)
        on_press: app.go_back()


    TextInput:
        text: str(app.num_hidden_units)
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .65}
        on_text_validate: app.num_hidden_units = int(self.value)
    Label:
        pos_hint: {'x': .05, 'center_y': .65}
        text: '# hidden units'
        size_hint: (.2, .1)


    Slider:
        pos: (30, 330)
        size_hint: (.3, .1)
        min: 1
        max: 100
        value: app.num_hidden_units
        on_value: app.num_hidden_units = self.value



    TextInput:
        text: str(app.num_valid_input)
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .55}
        on_text_validate: app.num_valid_input = int(self.value)
    Label:
        pos_hint: {'x': .05, 'center_y': .55}
        text: '# validations'
        size_hint: (.2, .1)

    Slider:
        pos: (30, 272)
        size_hint: (.3, .1)
        min: 1
        max: 100
        value: app.num_valid_input
        on_value: app.num_valid_input = self.value


    TextInput:
        text: str(app.num_test_data)
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .45}
        on_text_validate: app.num_test_data = int(self.value)
    Label:
        pos_hint: {'x': .05, 'center_y': .45}
        text: '# test data'
        size_hint: (.2, .1)

    Slider:
        pos: (30, 212)
        size_hint: (.3, .1)
        min: 1
        max: 100
        value: app.num_test_data
        on_value: app.num_test_data = self.value


    TextInput:
        text: str(app.hidden_units_learning_rate)
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .34}
        on_text_validate: app.hidden_units_learning_rate = float(self.value)
    Label:
        pos_hint: {'x': .05, 'center_y': .36}
        text: 'hidden units'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .05, 'center_y': .34}
        text: 'learning rate'
        size_hint: (.2, .1)

    Slider:
        pos: (30, 147)
        size_hint: (.3, .1)
        min: 0.001
        max: 1.0
        value: app.hidden_units_learning_rate
        on_value: app.hidden_units_learning_rate = self.value



    TextInput:
        text: str(app.output_units_learning_rate)
        size_hint: (.07, .05)
        pos_hint: {'x': .9, 'center_y': .65}
        on_text_validate: app.output_units_learning_rate = float(self.value)
    Label:
        pos_hint: {'x': .65, 'center_y': .66}
        text: 'output units'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .65, 'center_y': .64}
        text: 'learning rate'
        size_hint: (.2, .1)

    Slider:
        pos: (525, 330)
        size_hint: (.3, .1)
        min: 0.001
        max: 1.0
        value: app.output_units_learning_rate
        on_value: app.output_units_learning_rate = self.value


    TextInput:
        text: str(app.momentum)
        size_hint: (.07, .05)
        pos_hint: {'x': .9, 'center_y': .55}
        on_text_validate: app.momentum = float(self.value)
    Label:
        pos_hint: {'x': .65, 'center_y': .55}
        text: 'momentum rate'
        size_hint: (.2, .1)
    Slider:
        pos: (525, 272)
        size_hint: (.3, .1)
        min: 0.001
        max: 1.0
        value: app.momentum
        on_value: app.momentum = self.value


    TextInput:
        text: str(app.epochs)
        size_hint: (.07, .05)
        pos_hint: {'x': .9, 'center_y': .45}
        on_text_validate: app.epochs = int(self.value)
    Label:
        pos_hint: {'x': .65, 'center_y': .46}
        text: '# of epochs'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .65, 'center_y': .44}
        text: 'needed to train'
        size_hint: (.2, .1)

    Slider:
        pos: (525, 212)
        size_hint: (.3, .1)
        min: 0
        max: 10000
        value: app.epochs
        on_value: app.epochs = self.value



    TextInput:
        text: str(app.minimum_rmse)
        size_hint: (.07, .05)
        pos_hint: {'x': .9, 'center_y': .35}
        on_text_validate: app.minimum_rmse = int(self.value)
    Label:
        pos_hint: {'x': .65, 'center_y': .35}
        text: 'or minimum RMSE'
        size_hint: (.2, .1)

    Slider:
        pos: (525, 147)
        size_hint: (.3, .1)
        min: 1
        max: 100
        value: app.minimum_rmse
        on_value: app.minimum_rmse = self.value
'''


class TrainingParameters(Screen):
    def __init__(self, **kwargs):
        super(TrainingParameters, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
