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
        text: '10'
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .65}
        value: app.hidden_units
        on_text_validate: app.hidden_units = self.value
    Label:
        pos_hint: {'x': .1, 'center_y': .65}
        text: '# hidden units'
        size_hint: (.2, .1)
                

    TextInput:
        text: '0'
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .55}
        value: app.num_valid_input
        on_text_validate: app.num_valid_input = self.value
    Label: 
        pos_hint: {'x': .1, 'center_y': .55}
        text: '# validations'
        size_hint: (.2, .1)


    TextInput:
        text: '0'
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .45}
        value: app.num_test_data
        on_text_validate: app.num_test_data = self.value
    Label: 
        pos_hint: {'x': .1, 'center_y': .45}
        text: '# test data'
        size_hint: (.2, .1)


    TextInput:
        text: '0.1'
        size_hint: (.07, .05)
        pos_hint: {'x': .3, 'center_y': .35}
        value: app.hidden_units_learning_rate
        on_text_validate: app.hidden_units_learning_rate = self.value
    Label: 
        pos_hint: {'x': .1, 'center_y': .36}
        text: 'hidden units'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .1, 'center_y': .34}
        text: 'learning rate'
        size_hint: (.2, .1)
    

    TextInput:
        text: '0.2'
        size_hint: (.07, .05)
        pos_hint: {'x': .8, 'center_y': .65}
        value: app.output_units_learning_rate
        on_text_validate: app.output_units_learning_rate = self.value
    Label: 
        pos_hint: {'x': .6, 'center_y': .66}
        text: 'output units'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .6, 'center_y': .64}
        text: 'learning rate'
        size_hint: (.2, .1)
        
    
    TextInput:
        text: '0.2'
        size_hint: (.07, .05)
        pos_hint: {'x': .8, 'center_y': .55}
        value: app.momentum
        on_text_validate: app.momentum = self.value
    Label: 
        pos_hint: {'x': .6, 'center_y': .55}
        text: 'momentum rate'
        size_hint: (.2, .1)
        
    
    TextInput:
        text: '0'
        size_hint: (.07, .05)
        pos_hint: {'x': .8, 'center_y': .45}
        value: app.epochs
        on_text_validate: app.epochs = self.value
    Label: 
        pos_hint: {'x': .6, 'center_y': .46}
        text: '# of epochs'
        size_hint: (.2, .1)
    Label:
        pos_hint: {'x': .6, 'center_y': .44}
        text: 'needed to train'
        size_hint: (.2, .1)

    
    TextInput:
        text: '0'
        size_hint: (.07, .05)
        pos_hint: {'x': .8, 'center_y': .35}
        value: app.minimum_rmse
        on_text_validate: app.minimum_rmse = self.value
    Label: 
        pos_hint: {'x': .6, 'center_y': .35}
        text: 'or minimum RMSE'
        size_hint: (.2, .1)
'''


class runTrain(Screen):
    def __init__(self, **kwargs):
        super(runTrain, self).__init__(**kwargs)
        self.add_widget(Builder.load_string(kv))
