from kivy_modalview import ModalView
from cfg import STYLES
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class KeyboardButton(Button):
    """
        is_default = <bool>: True, если это обычная кнопка и служит для ввода цифр/команд/скобок в строку математического выражения;
                False, если у кнопки есть отдельное предназначение;
        action = <str>: название действия, за которое отвечается действие, при is_default = False; 
    """
    def __init__(self, text, is_default=True, action=None):
        super().__init__(text=str(text),
            background_color=STYLES['keyboard_btn']['bgc'],
            color=STYLES['keyboard_btn']['color'],
            font_size=STYLES['keyboard_btn']['fz'])
        self.is_default = is_default
        self.action = action

class FunctionalButton(Button):
        def __init__(self, text):
            super().__init__(text=str(text),
                background_color=STYLES['functional_btn']['bgc'],
                color=STYLES['functional_btn']['color'],
                font_size=STYLES['functional_btn']['fz'])

class NumsButton(Button):
    def __init__(self, nums=10):
        super().__init__(text=str(str(nums)),
                background_color=STYLES['nums_btn']['bgc'],
                color=STYLES['nums_btn']['color'],
                font_size=STYLES['nums_btn']['fz'])
        self.nums = int(nums)

class NumsModalview(ModalView):
    def __init__(self):
        super().__init__(auto_dismiss=True, size_hint=STYLES['nums_mv']['sh'])
        main_bl = BoxLayout(orientation='vertical', padding=STYLES['nums_mv']['main_bl']['padding'], spacing=STYLES['nums_mv']['main_bl']['spacing'])
        ti = ModalviewIntTextinput() # поле ввода СС

        # слой с кнопками принятия и отмены
        buttons_hb = BoxLayout(orientation='horizontal', spacing=STYLES['nums_mv']['buttons_hb']['spacing'])
        btn_ok = ModaviewButton(text='ok')
        btn_cancel = ModaviewButton(text='cancel')
        buttons_hb.add_widget(btn_ok)
        buttons_hb.add_widget(btn_cancel)
        btn_cancel.on_release = self.dismiss_mv

        nums_hb = BoxLayout(orientation='horizontal', padding=STYLES['nums_mv']['nums_hb']['padding'], spacing=STYLES['nums_mv']['nums_hb']['spacing'])
        nums_2_btn = NumsButton(nums='2')
        nums_8_btn = NumsButton(nums='8')
        nums_10_btn = NumsButton(nums='10')
        nums_16_btn = NumsButton(nums='16')
        nums_hb.add_widget(nums_2_btn)
        nums_hb.add_widget(nums_8_btn)
        nums_hb.add_widget(nums_10_btn)
        nums_hb.add_widget(nums_16_btn)

        main_bl.add_widget(ti)
        main_bl.add_widget(buttons_hb)
        main_bl.add_widget(nums_hb)

        self.main_bl = main_bl
        self.ti = ti
        self.buttons_hb = buttons_hb
        self.btn_ok = btn_ok
        self.btn_cancel = btn_cancel

        self.nums_2_btn = nums_2_btn
        self.nums_8_btn = nums_8_btn
        self.nums_10_btn = nums_10_btn
        self.nums_16_btn = nums_16_btn

        self.add_widget(main_bl)

    def dismiss_mv(self):
        self.ti.clear_saved_value()
        self.dismiss()

class ModaviewButton(Button):
    def __init__(self, text):
        super().__init__(text=str(text),
            background_color=STYLES['modalview_btn']['bgc'],
            color=STYLES['modalview_btn']['color'],
            font_size=STYLES['modalview_btn']['fz'],
            size_hint=STYLES['modalview_btn']['sh'])

class NumsTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter='int'
        self.bind(text=self.on_text)
        self.saved_value = '10'
        self.hint_text = '10'

    def on_text(self, instance, value):
        if len(value) < 3 and not '\n' in value:
            self.saved_value = value
        else:
            self.text = self.saved_value

    def clear_saved_value(self):
        self.saved_value = ''
        self.text = ''

class ModalviewIntTextinput(NumsTextInput):
    def __init__(self):
        super().__init__(
            font_size=STYLES['modalview_int_textinput']['fz'],
            size_hint=STYLES['modalview_int_textinput']['sh'])
