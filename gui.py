from kivy.app import App
from kivy.uix.behaviors import button

from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy_modalview import ModalView

from kivy.config import Config

Config.set('graphics', 'width', 900)
Config.set('graphics', 'height', 1600)
Config.set('graphics', 'resizable', 0)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

class KeyboardButton(Button):
    def __init__(self, text):
        super().__init__(text=str(text),
            background_color=(3, 3, 3),
            color=(0.05, 0.05, 0.05),
            font_size='20sp')

class FunctionalButton(Button):
        def __init__(self, text):
            super().__init__(text=str(text),
                background_color=(2.4, 2.4, 2.4),
                color=(0.05, 0.05, 0.05),
                font_size='15sp')

class ModalviewIntInput(ModalView):
    def __init__(self):
        super().__init__(auto_dismiss=True, size_hint=[0.75, 0.25])
        vb = BoxLayout(orientation='vertical', padding=20)
        ti = ModalviewIntTextinput() # поле ввода СС

        # слой с кнопками принятия и отмены
        buttons_hb = BoxLayout(orientation='horizontal', spacing=15)
        btn_ok = ModaviewButton(text='ok')
        btn_cancel = ModaviewButton(text='cancel')
        buttons_hb.add_widget(btn_ok)
        buttons_hb.add_widget(btn_cancel)
        btn_cancel.on_release = self.dismiss_mv

        vb.add_widget(ti)
        vb.add_widget(buttons_hb)

        self.vb = vb
        self.ti = ti
        self.buttons_hb = buttons_hb
        self.btn_ok = btn_ok
        self.btn_cancel = btn_cancel
        self.add_widget(vb)

    def dismiss_mv(self):
        self.ti.clear_saved_value()
        self.dismiss()

class ModaviewButton(Button):
    def __init__(self, text):
        super().__init__(text=str(text),
            background_color=(1.4, 1.4, 1.4),
            color=(0.05, 0.05, 0.05),
            size_hint=[1, 0.8],
            font_size='15sp')

class ModalviewIntTextinput(TextInput):
    def __init__(self):
        super().__init__(size_hint=[1, 0.75],
            font_size='35sp', 
            input_filter='int')

        self.bind(text=self.on_text)
        self.saved_value = ''

    def on_text(self, instance, value):
        if len(value) < 3:
            self.saved_value = value
        else:
            self.text = self.saved_value

    def clear_saved_value(self):
        self.saved_value = ''
        self.text = ''

class MainApp(App):
    KEYBOARD_KEYS = ['1', '2', '3', 'A', 'B', 'C', 'D', 'E',
                '4', '5', '6', 'F', 'G', 'H', 'I', 'J',
                '7', '8', '9', 'K', 'L', 'M', 'N', 'O',
                '(', '0', ')', 'P', 'Q', 'R', 'S', 'T',
                '+', '-', '*', 'U', 'V', 'W', 'X', 'Y',
                '/', '^', ' ', 'Z']
    
    def build(self):
        self.convertion_mv = ModalviewIntInput()
        self.convertion_mv_ti = self.convertion_mv.ti


        self.changing_mv = ModalviewIntInput()
        self.changing_mv_ti = self.changing_mv.ti


        settings_menu_al = AnchorLayout(size_hint=[1, 0.05])
        settings_menu_btn = Button(text='...')
        settings_menu_al.add_widget(settings_menu_btn)


        convertions_menu_al = AnchorLayout(size_hint=[0.05, 1], anchor_x='left', anchor_y='center')
        convertions_menu_btn = Button(text='...')
        convertions_menu_al.add_widget(convertions_menu_btn)


        line_al = AnchorLayout(size_hint=[0.90, 1], anchor_x='center', anchor_y='center')
        line_ti = TextInput(font_size='60sp', disabled=True, background_color=(255, 255, 255))
        line_al.add_widget(line_ti)


        commands_executions_menu_al = AnchorLayout(size_hint=[0.05, 1], anchor_x='right', anchor_y='center')
        commands_executions_menu_btn = Button(text='...')
        commands_executions_menu_al.add_widget(commands_executions_menu_btn)


        middle_hb = BoxLayout(orientation='horizontal', size_hint=[1, 0.45])
        middle_hb.add_widget(convertions_menu_al)
        middle_hb.add_widget(line_al)
        middle_hb.add_widget(commands_executions_menu_al)


        functional_tab_hb = BoxLayout(orientation='horizontal', size_hint=[1, 0.05])

        cursor_offset_left_btn = FunctionalButton('<-')
        convert_btn = FunctionalButton('conv')
        convert_btn.on_release = self.convertion_mv.open
        change_btn = FunctionalButton('change')
        change_btn.on_release = self.changing_mv.open
        backspace_btn = FunctionalButton('backspace')
        cursor_offset_right_btn = FunctionalButton('->')

        functional_tab_hb.add_widget(cursor_offset_left_btn)
        functional_tab_hb.add_widget(convert_btn)
        functional_tab_hb.add_widget(change_btn)
        functional_tab_hb.add_widget(backspace_btn)
        functional_tab_hb.add_widget(cursor_offset_right_btn)


        keyboard_al = AnchorLayout(size_hint=[1, 0.45])
        keyboard_gl = GridLayout(cols=8, spacing=1)
        keyboard_al.add_widget(keyboard_gl)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(settings_menu_al)
        main_layout.add_widget(middle_hb)
        main_layout.add_widget(functional_tab_hb)
        main_layout.add_widget(keyboard_al)


        self.keyboard_gl = keyboard_gl
        self.fill_keyboard()

        return main_layout

    def fill_keyboard(self):
        for key in self.KEYBOARD_KEYS:
            self.keyboard_gl.add_widget(Widget() if key == ' ' else KeyboardButton(str(key)))

if __name__ == '__main__':
    MainApp().run()