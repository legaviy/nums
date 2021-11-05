from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy_markuptextinput import MarkupTextInput
from kivy_modalview import ModalView

from cfg import LATIN_ALPHABET, logging, CURSOR_SIGN_FORMATTED, KEYBOARD_KEYS, KEYS_IS_DEFAULT_EXCEPTIONS, get_command_analogue
from numb import _nums, _numb

class KeyboardButton(Button):
    """
        is_default = <bool>: True, если это обычная кнопка и служит для ввода цифр/команд/скобок в строку математического выражения;
                False, если у кнопки есть отдельное предназначение;
        action = <str>: название действия, за которое отвечается действие, при is_default = False; 
    """
    def __init__(self, text, is_default=True, action=None):
        super().__init__(text=str(text),
            background_color=(3, 3, 3),
            color=(0.05, 0.05, 0.05),
            font_size='20sp')
        self.is_default = is_default
        self.action = action

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
        super().__init__(size_hint=[1, 0.75],
            font_size='35sp')

class MainApp(App):
    def build(self):
        self.build_interface()

        from interface import _interface_, _commander_
        self._interface_ = _interface_
        self._commander_ = _commander_

        self.cursor_offset_left_btn.on_release = self.offset_left
        self.cursor_offset_right_btn.on_release = self.offset_right
        self.backspace_btn.on_release = self.backspace
        self.convertion_mv.btn_ok.on_release = self.convert_nums
        self.changing_mv.btn_ok.on_release = self.change_nums

        self.cursor_offset_to_begin_btn.on_release = self.offset_to_begin
        self.clear_signs_btn.on_release = self.clear_signs
        self.cursor_offset_ot_end_btn.on_release = self.offset_to_end

        self.answer_nums = 10

        self.output()

        return self.main_layout

    def build_interface(self):
        self.convertion_mv = ModalviewIntInput()
        self.convertion_mv_ti = self.convertion_mv.ti
        self.convertion_mv_btn_ok = self.convertion_mv.btn_ok

        self.changing_mv = ModalviewIntInput()
        self.changing_mv_ti = self.changing_mv.ti
        self.changing_mv_btn_ok = self.changing_mv.btn_ok

        settings_menu_al = AnchorLayout(size_hint=[1, 0.05])
        settings_menu_btn = Button(text='...')
        settings_menu_al.add_widget(settings_menu_btn)


        convertions_menu_al = AnchorLayout(size_hint=[0.05, 1], anchor_x='left', anchor_y='center')
        convertions_menu_btn = Button(text='...')
        convertions_menu_al.add_widget(convertions_menu_btn)


        line_al = AnchorLayout(size_hint=[0.90, 1], anchor_x='center', anchor_y='center')
        line_bl = BoxLayout(orientation='vertical',)
        expression_bl = BoxLayout(size_hint=[1, 0.85])
        expression_ti = MarkupTextInput(font_size='20sp', readonly=True, background_color=(3, 3, 3))
        expression_bl.add_widget(expression_ti)

        answer_bl = BoxLayout(orientation='horizontal', size_hint=[1, 0.15])
        answer_ti = TextInput(font_size='10sp', readonly=True, background_color=(3, 3, 3), size_hint=[0.8,1])
        answer_nums_ti = NumsTextInput(font_size='30sp', background_color=(1,1,1), size_hint=[0.2,1], text='10')
        answer_bl.add_widget(answer_ti)
        answer_bl.add_widget(answer_nums_ti)
        answer_nums_ti.bind(text=self.on_answer_nums)

        line_bl.add_widget(expression_bl)
        line_bl.add_widget(answer_bl)
        line_al.add_widget(line_bl)
        self.expression_ti = expression_ti
        self.answer_ti = answer_ti


        commands_executions_menu_al = AnchorLayout(size_hint=[0.05, 1], anchor_x='right', anchor_y='center')
        commands_executions_menu_btn = Button(text='...')
        commands_executions_menu_al.add_widget(commands_executions_menu_btn)


        middle_hb = BoxLayout(orientation='horizontal', size_hint=[1, 0.45])
        middle_hb.add_widget(convertions_menu_al)
        middle_hb.add_widget(line_al)
        middle_hb.add_widget(commands_executions_menu_al)


        functional_tab_hb = BoxLayout(orientation='horizontal', size_hint=[1, 0.1])

        cursor_offset_left_btn = FunctionalButton('<-')
        cursor_offset_left_btn.size_hint = [0.2, 1]
        convert_btn = FunctionalButton('conv')
        convert_btn.on_release = self.convertion_mv.open
        change_btn = FunctionalButton('change')
        change_btn.on_release = self.changing_mv.open
        backspace_btn = FunctionalButton('backspace')
        cursor_offset_right_btn = FunctionalButton('->')
        cursor_offset_right_btn.size_hint = [0.2, 1]
        cursor_offset_to_begin_btn = FunctionalButton('home')
        cursor_offset_ot_end_btn = FunctionalButton('end')
        clear_signs_btn = FunctionalButton('clear')

        functional_tab_hb.add_widget(cursor_offset_left_btn)

        functional_tab_middle_hb = BoxLayout(orientation='vertical', size_hint=[0.6, 1])

        functional_tab_middle_upper_hb = BoxLayout(orientation='horizontal', size_hint=[1, 0.75])
        functional_tab_middle_upper_hb.add_widget(convert_btn)
        functional_tab_middle_upper_hb.add_widget(change_btn)
        functional_tab_middle_upper_hb.add_widget(backspace_btn)
        functional_tab_middle_hb.add_widget(functional_tab_middle_upper_hb)

        functional_tab_middle_lower_hb = BoxLayout(orientation='horizontal', size_hint=[1, 0.25])
        functional_tab_middle_lower_hb.add_widget(cursor_offset_to_begin_btn)
        functional_tab_middle_lower_hb.add_widget(clear_signs_btn)
        functional_tab_middle_lower_hb.add_widget(cursor_offset_ot_end_btn)
        functional_tab_middle_hb.add_widget(functional_tab_middle_lower_hb)

        functional_tab_hb.add_widget(functional_tab_middle_hb)
        functional_tab_hb.add_widget(cursor_offset_right_btn)

        self.cursor_offset_left_btn = cursor_offset_left_btn
        self.convert_btn = convert_btn
        self.change_btn = change_btn
        self.backspace_btn = backspace_btn
        self.cursor_offset_right_btn = cursor_offset_right_btn
        self.cursor_offset_to_begin_btn = cursor_offset_to_begin_btn
        self.clear_signs_btn = clear_signs_btn
        self.cursor_offset_ot_end_btn = cursor_offset_ot_end_btn

        keyboard_al = AnchorLayout(size_hint=[1, 0.4])
        keyboard_gl = GridLayout(cols=8, spacing=1)
        keyboard_al.add_widget(keyboard_gl)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(settings_menu_al)
        main_layout.add_widget(middle_hb)
        main_layout.add_widget(keyboard_al)
        main_layout.add_widget(functional_tab_hb)


        self.keyboard_gl = keyboard_gl
        self.fill_keyboard()

        self.main_layout = main_layout

    def fill_keyboard(self):
        for key in KEYBOARD_KEYS:
            if key == ' ':
                self.keyboard_gl.add_widget(Button(background_color=(3,3,3)))
            else:
                btn = KeyboardButton(str(key))
                btn.bind(on_release=self.on_keyboard_btn_press)

                if key in KEYS_IS_DEFAULT_EXCEPTIONS: # обработка кнопки на наличие исключения из обычных кнопок
                    btn.is_default = False
                    btn.action = KEYS_IS_DEFAULT_EXCEPTIONS[key] # присваивание экземпляру названия действия, за которое отвечает данный экземляр

                self.keyboard_gl.add_widget(btn)

    def on_keyboard_btn_press(self, instance):
        if instance.is_default: # обработчик стандартной кнопки
            value = instance.text
            if value in LATIN_ALPHABET + [str(x) for x in range(10)] and self._interface_.is_numb:
                if not _nums._num_is_valid_for_nums(value, self._interface_.signs[self._interface_.cursor].nums) == True:
                    return
            self._interface_._input(get_command_analogue(value, False))
            self.output()
        elif instance.action == 'changing_pos': # обработчики нестандартных кнопок
            self.change_positive_of_numb()

    def offset_left(self):
        self._interface_._offset(False)
        self.output()

    def offset_right(self):
        self._interface_._offset()
        self.output()

    def offset_to_begin(self):
        self._interface_._offset_to_begin()
        self.output()

    def offset_to_end(self):
        self._interface_._offset_to_end()
        self.output()

    def clear_signs(self):
        self._interface_._clear()
        self.output()

    def backspace(self):
        self._interface_._delete()
        self.output()

    def change_nums(self):
        nums = self.changing_mv_ti.saved_value
        if nums == '':
            return
        nums = int(nums)
        if 1 < nums < 37:
            self._interface_._change_nums(nums)
            self.changing_mv.dismiss_mv()
            self.changing_mv_ti.saved_value = '10'
            self.output()

    def convert_nums(self):
        nums = self.convertion_mv_ti.saved_value
        if nums == '':
            return
        nums = int(nums)
        if 1 < nums < 37 and self._interface_.is_numb:
            self._interface_._convert_nums(nums)
            self.convertion_mv.dismiss_mv()
            self.convertion_mv_ti.saved_value = '10'
            self.output()

    def change_positive_of_numb(self):
        if self._interface_.is_numb:
            self._interface_.signs[self._interface_.cursor]._change_pos()
            self.output()

    def on_answer_nums(self, instance, value):
        if not value == '':
            value = int(value)
            if 1 < value < 37:
                self.answer_nums = value
                self.output()

    def output(self):
        self.expression_ti.text = ''
        CS = CURSOR_SIGN_FORMATTED
        cursor = self._interface_.cursor
        subcursor = self._interface_.subcursor
        numbcursor = self._interface_.numbcursor
        signs = self._interface_.signs
        is_numb = self._interface_.is_numb
        is_frct = self._interface_.is_frct
        answer_nums = self.answer_nums
        answer_text = '...'
        is_cursor_inserted = False
        # заполнение выражения
        text = ''
        for i, sign in enumerate(signs):
            sign = get_command_analogue(sign, True)
            if subcursor > cursor and subcursor == i and not is_cursor_inserted:
                text = text if text[-2:] == CS + ' '  else f'{text} {CS} '
            if cursor == subcursor == i:
                if is_numb:
                    text = f'{text} {sign._get_pos_str()}'
                    if is_frct:
                        text = f'{text}{sign._get_intg_str()},'
                        frct = sign.frct
                        if frct == []:
                            text = f'{text}{CS}'
                        else:
                            for i in range(len(frct)):
                                if numbcursor == i:
                                    text = f'{text}{CS}'
                                text = f'{text}{str(frct[i])}'
                            if numbcursor == len(frct):
                                text = f'{text}{CS}'
                    else:
                        intg = sign.intg
                        for i in range(len(intg)):
                            if numbcursor == i:
                                text = f'{text}{CS}'
                            text = f'{text}{str(intg[i])}'
                        if numbcursor == len(intg):
                            text = f'{text}{CS}'
                        text = f'{text}{"0" if sign._get_frct_str() == "" else "," + sign._get_frct_str()}'
                        
                    text = f'{text}({str(sign.nums)}) '
                else:
                    text = f'{text} {sign}{CS} '
            else:
                text = f'{text} {sign}'
            if subcursor > cursor and cursor == i:
                is_cursor_inserted = True
                text = f'{text} {CS} '

        self.expression_ti.text = text

        # заполнение ответа
        try:
            answer = _numb(0)
            answer._apply_numb_properties_to_self(self._commander_._execute_interface_expression(self._interface_))
            answer._convert_to(answer_nums)
            answer_text = str(answer)
        except Exception as exc:
            logging.critical('MainApp.output cought exception:')
            logging.critical(exc)

        self.answer_ti.text = str(answer_text)

        return text, answer_text

if __name__ == '__main__':
    MainApp().run()