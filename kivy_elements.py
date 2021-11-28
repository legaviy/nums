from kivy_modalview import ModalView
from cfg import STYLES, _inter_to_letters, LATIN_ALPHABET, _inter_sign_to_num, KEYS_ICONS
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import *

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
        # if self.text in KEYS_ICONS:
        #     self.text = ''

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

class ConvertionModalview(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initial_build()
        self.conv_tables = []

    def initial_build(self):
        self.size_hint = [0.8, 0.95]
        layout = BoxLayout(orientation='vertical')
        sv = ScrollView(size_hint=[0.95, 0.9])
        root = GridLayout(cols=1, size_hint_y=None)
        sv.add_widget(root)

        self.sv = sv
        root.bind(minimum_height=root.setter('height'))
        self.root = root

        btn_close_al = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=[1, 0.05])
        btn_close = Button(text='Close')
        btn_close.on_release = self.dismiss
        
        sv_al = AnchorLayout(anchor_x='center', anchor_y='top')
        sv_al.add_widget(sv)
        layout.add_widget(sv_al)
        btn_close_al.add_widget(btn_close)
        layout.add_widget(btn_close_al)
        self.add_widget(layout)

    def set_conv_tables(self, conv_tables):
        self.conv_tables = conv_tables

    def fill(self):
        self.clear_widgets()
        self.initial_build()
        for i, conv_table in enumerate(self.conv_tables):
            if not conv_table.numb.nums == conv_table.result.nums:
                bl = BoxLayout(orientation='vertical', size_hint_y=None)
                bl.bind(minimum_height=bl.setter('height'))

                if conv_table.mode == 'to_dec':
                    sum = ' + '.join([f'{x[0]}{f"({_inter_sign_to_num(x[0])})" if x[0] in LATIN_ALPHABET else ""} × {x[1]}[sup]{x[2]}[/sup]' for x in conv_table.table + conv_table.table_frct])
                    label = Label(text=f'{str(conv_table.numb)} -> {str(conv_table.result)}\n{sum} = {str(conv_table.result)}', markup=True, size_hint_y=None, height=300)
                    label.bind(size=label.setter('text_size'))
                    bl.add_widget(label)
                elif conv_table.mode == 'from_dec':
                    label = Label(text=f'(integer) {str(conv_table.numb)} -> {str(conv_table.result)}', markup=True, size_hint_y=None)
                    label.bind(size=label.setter('text_size')) 

                    gd_intg = GridLayout(cols=4, size_hint_y=None)
                    gd_intg.bind(minimum_height=gd_intg.setter('height'))

                    gd_intg.add_widget(Label(text='devided', size_hint_y=None))
                    gd_intg.add_widget(Label(text='devider', size_hint_y=None))
                    gd_intg.add_widget(Label(text='integer', size_hint_y=None))
                    gd_intg.add_widget(Label(text='remainder', size_hint_y=None))

                    for row in conv_table.table:
                        if [int(row[0]), int(row[2]), int(row[3])] == [0, 0, 0]:
                            continue
                        for i, x in enumerate(row):
                            l = Label(size_hint_y=None, halign='right', height=150, markup=True)
                            text = f'{str(x)}{f"({_inter_to_letters([x])[0]})" if int(x) > 9 and i == 3 else ""}'
                            text = f'[b]{text}[/b]' if i == 3 else text
                            l.text = text
                            l.bind(size=l.setter('text_size'))
                            gd_intg.add_widget(l)

                    bl.add_widget(label)
                    bl.add_widget(gd_intg)
                    if not conv_table.table_frct == []:
                        label_frct = Label(text=f'(fraction) {str(conv_table.numb)} -> {str(conv_table.result)}', markup=True, size_hint_y=None)
                        label_frct.bind(size=label_frct.setter('text_size'))

                        gd_frct = GridLayout(cols=4, size_hint_y=None)
                        gd_frct.bind(minimum_height=gd_frct.setter('height'))
                    
                        gd_frct.add_widget(Label(text='fraction', size_hint_y=None))
                        gd_frct.add_widget(Label(text='multiplier', size_hint_y=None))
                        gd_frct.add_widget(Label(text='product', size_hint_y=None))
                        gd_frct.add_widget(Label(text='integer', size_hint_y=None))

                        for row in conv_table.table_frct:
                            for x in row:
                                gd_frct.add_widget(Label(text=str(x), height=50, size_hint_y=None, halign='center'))

                        bl.add_widget(label_frct)
                        bl.add_widget(gd_frct)

                if i > 0:
                    self.root.add_widget(Label(height=50, text='––––––––––––––––––––––––––––––', size_hint_y=None))
                self.root.add_widget(bl)

class CommandExecutionModalView(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initial_build()
        self.commands = []

    def initial_build(self):
        self.size_hint = [0.8, 0.95]
        layout = BoxLayout(orientation='vertical')
        sv = ScrollView(size_hint=[0.95, 0.9])
        root = GridLayout(cols=1, size_hint_y=None)
        sv.add_widget(root)

        self.sv = sv
        root.bind(minimum_height=root.setter('height'))
        self.root = root

        btn_close_al = AnchorLayout(anchor_x='center', anchor_y='bottom', size_hint=[1, 0.05])
        btn_close = Button(text='Close')
        btn_close.on_release = self.dismiss
        
        sv_al = AnchorLayout(anchor_x='center', anchor_y='top')
        sv_al.add_widget(sv)
        layout.add_widget(sv_al)
        btn_close_al.add_widget(btn_close)
        layout.add_widget(btn_close_al)
        self.add_widget(layout)

    def set_commands(self, commands):
        self.commands = commands

    def fill(self):
       self.clear_widgets()
       self.initial_build()
       for i, command_execution in enumerate(self.commands):
            bl = BoxLayout(orientation='vertical', size_hint_y=None)
            bl.bind(minimum_height=bl.setter('height'))
            label = Label(text=f'{i+1}. {command_execution.left_operand} {command_execution.command} {command_execution.right_operand} = {command_execution.result}', markup=True, halign='center')
            label.bind(size=label.setter('text_size'))
            bl.add_widget(label)
            self.root.add_widget(bl)