from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy_elements import KeyboardButton, FunctionalButton, NumsModalview, NumsTextInput

from cfg import CURSOR_SIGN_FORMATTED, LATIN_ALPHABET, logging, CURSOR_SIGN_FORMATTED, KEYBOARD_KEYS, KEYS_IS_DEFAULT_EXCEPTIONS, get_command_analogue, STYLES, NotEnoughArgumentsException, SIGNS_COMMA_LIMIT
from numb import _nums, _numb

class ConvertionTable:
    mode = None
    result = None
    table = []
    table_frct = []

    def __init__(self, from_nums, to_nums, numb):
        from_nums = int(from_nums)
        to_nums = int(to_nums)
        self.from_nums = from_nums
        self.to_nums = to_nums
        self.numb = numb
        self.mode = 'from_dec' if from_nums == 10 else ('to_dec' if to_nums == 10 else None)
        if self.mode == None:
            raise(NotEnoughArgumentsException)

        if self.mode == 'to_dec':
            self.table = self.to_dec(self.from_nums, self.numb, is_fract=False)
            self.table_frct = self.to_dec(self.from_nums, self.numb, is_fract=True)
            self.result = _nums._convert_to_dec(self.numb, self.from_nums)
        else:
            self.table = self.from_dec(self.to_nums, self.numb)
            self.table_frct = self.from_dec_fract(self.to_nums, self.numb)
            self.result = _nums._convert_from_dec(self.numb, self.to_nums)

    def from_dec(self, nums, numb=None, intg=None) -> list():
        dig = None
        if intg == None and not numb == None:
            dig = int(''.join([str(elt) for elt in numb.intg]))
        elif numb == None and not intg == None:
            dig = intg
        else:
            raise(NotEnoughArgumentsException)
        table = []
        arr = [] # список переведённых чисел в систему с основанием num
        mod = dig % nums # остаток деления
        div = dig // nums # целое от частного
        table.append([dig, nums, div, mod])
        arr.append(mod)
        while div > 0: # пока частное (предыдущее частное, поделённое на основание системы счисления) остаётся больше нуля, добавлять остаток от деления
            mod = div % nums # остаток от деления
            table.append([div, nums])
            div //= nums # целая часть от деления
            table[-1] = table[-1] + [div, mod]
            arr.append(mod)
            if div < nums: # если частное меньше основания системы, то оно сразу добавляется в список, и цикл преывается
                table.append([div, nums, div, div])
                arr.append(div)
                break
        print(table)
        return table

    def from_dec_fract(self, nums, numb=None, frcts=None) -> list():
        frct = None
        if frcts == None and not numb == None:
            frct = (''.join([str(elt) for elt in numb.frct]))
        elif numb == None and not frcts == None:
            frct = frcts
        else:
            raise(NotEnoughArgumentsException)
        table = []
        arr = []  # список переведённых чисел в систему с основанием num
        mul = float('0.' + ''.join([elt for elt in str(frct)])) # число типа float через объединения строк: '0.' и объеденённый в строку список дробной части
        n = 0 # счётчик, не позволяющий добавить в дробную часть больше знаков, чем SIGNS_COMMA_LIMIT (см. cfg.py)
        while n <= SIGNS_COMMA_LIMIT and mul > 0:
            table.append([mul])
            mul *= nums # умножение дробной части на основание системы
            table[-1] = table[-1] + [nums, mul, int(mul)]
            arr.append(int(mul)) # добавить целую часть от умножения в список
            mul = float('0.' + ''.join([str(elt) for elt in _nums._get_frct(mul)]))
            n += 1

        return table

    def to_dec(self, nums=None, numb=None, intg=None, is_fract=False):
        mode = -1 if is_fract else 1 # множитель степени
        intgs = None # строковое значение целой/дробной части
        if numb == None and not intg == None and not nums == None:
            intgs = str(intg)
            nums = int(nums)
        elif intg == None and not numb == None:
            arr = numb.frct if is_fract else numb.intg
            intgs = str(''.join([str(elt) for elt in arr]))
            nums = numb.nums
        else:
            raise NotEnoughArgumentsException()

        table = []

        intgs = ''.join([char for char in intgs])
        intgs = intgs if is_fract else intgs[::-1]
        num = 0 # переведённое значение в nums-СС
        grade = 1 if is_fract else 0 # степень возведения для каждого знака
        for char in intgs:
            num += int(_nums._inter_sign_to_num(char)) * nums ** (mode * grade)
            table.append([char, nums, (mode * grade)])
            grade += 1
        if 'e' in str(num) and is_fract:
            num = _nums._get_frct(num)
        else:
            num = str(''.join(_nums._get_frct(num)) if is_fract else num)

        return table

class MainApp(App):
    answer = None
    answer_nums = 10
    conv_tables = []
    ans_conv_table = []

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
        
        self.convertion_mv.nums_2_btn.bind(on_release=self.on_converion_nums_btn_pressed)
        self.convertion_mv.nums_8_btn.bind(on_release=self.on_converion_nums_btn_pressed)
        self.convertion_mv.nums_10_btn.bind(on_release=self.on_converion_nums_btn_pressed)
        self.convertion_mv.nums_16_btn.bind(on_release=self.on_converion_nums_btn_pressed)

        self.changing_mv.nums_2_btn.bind(on_release=self.on_changing_nums_btn_pressed)
        self.changing_mv.nums_8_btn.bind(on_release=self.on_changing_nums_btn_pressed)
        self.changing_mv.nums_10_btn.bind(on_release=self.on_changing_nums_btn_pressed)
        self.changing_mv.nums_16_btn.bind(on_release=self.on_changing_nums_btn_pressed)

        self.expression_ti.bind(size=self.expression_ti.setter('text_size'))
        self.answer_ti.bind(size=self.answer_ti.setter('text_size'))

        self.answer_nums = 10
        self.answer = _numb(0)

        self.output()

        return self.main_layout

    def build_interface(self):
        self.convertion_mv = NumsModalview()
        self.convertion_mv_ti = self.convertion_mv.ti
        self.convertion_mv_btn_ok = self.convertion_mv.btn_ok

        self.changing_mv = NumsModalview()
        self.changing_mv_ti = self.changing_mv.ti
        self.changing_mv_btn_ok = self.changing_mv.btn_ok

        settings_menu_al = AnchorLayout(size_hint=STYLES['settings_menu_al']['sh'])
        settings_menu_btn = Button(text='...')
        settings_menu_al.add_widget(settings_menu_btn)


        convertions_menu_al = AnchorLayout(size_hint=STYLES['convertions_menu_al']['sh'], anchor_x='left', anchor_y='center')
        convertions_menu_btn = Button(text='...')
        convertions_menu_al.add_widget(convertions_menu_btn)


        line_al = AnchorLayout(size_hint=STYLES['line_al']['sh'], anchor_x='center', anchor_y='center')
        line_bl = BoxLayout(orientation='vertical')
        expression_bl = BoxLayout(size_hint=STYLES['expression_bl']['sh'])
        expression_ti = Label(font_size=STYLES['expression_ti']['fz'], halign='left', valign='top', markup=True)
        expression_bl.add_widget(expression_ti)

        answer_bl = BoxLayout(orientation='horizontal', size_hint=STYLES['answer_bl']['sh'])
        answer_ti = Label(font_size=STYLES['answer_ti']['fz'], size_hint=STYLES['answer_ti']['sh'], halign='left', valign='top', markup=True)
        answer_nums_ti = NumsTextInput(font_size=STYLES['answer_nums_ti']['fz'], background_color=STYLES['answer_nums_ti']['bgc'], size_hint=STYLES['answer_nums_ti']['sh'], text='10')
        answer_bl.add_widget(answer_ti)
        answer_bl.add_widget(answer_nums_ti)
        answer_nums_ti.bind(text=self.on_answer_nums)

        line_bl.add_widget(expression_bl)
        line_bl.add_widget(answer_bl)
        line_al.add_widget(line_bl)
        self.expression_ti = expression_ti
        self.answer_ti = answer_ti


        commands_executions_menu_al = AnchorLayout(size_hint=STYLES['commands_executions_menu_al']['sh'], anchor_x='right', anchor_y='center')
        commands_executions_menu_btn = Button(text='...')
        commands_executions_menu_al.add_widget(commands_executions_menu_btn)


        middle_hb = BoxLayout(orientation='horizontal', size_hint=STYLES['middle_hb']['sh'])
        middle_hb.add_widget(convertions_menu_al)
        middle_hb.add_widget(line_al)
        middle_hb.add_widget(commands_executions_menu_al)


        functional_tab_hb = BoxLayout(orientation='horizontal', size_hint=STYLES['functional_tab_hb']['sh'])

        cursor_offset_left_btn = FunctionalButton('<-')
        cursor_offset_left_btn.size_hint = STYLES['cursor_offset_left_btn']['sh']
        convert_btn = FunctionalButton('conv')
        convert_btn.on_release = self.convertion_mv.open
        change_btn = FunctionalButton('change')
        change_btn.on_release = self.changing_mv.open
        backspace_btn = FunctionalButton('backspace')
        cursor_offset_right_btn = FunctionalButton('->')
        cursor_offset_right_btn.size_hint = STYLES['cursor_offset_right_btn']['sh']
        cursor_offset_to_begin_btn = FunctionalButton('home')
        cursor_offset_ot_end_btn = FunctionalButton('end')
        clear_signs_btn = FunctionalButton('clear')

        functional_tab_hb.add_widget(cursor_offset_left_btn)

        functional_tab_middle_hb = BoxLayout(orientation='vertical', size_hint=STYLES['functional_tab_middle_hb']['sh'])

        functional_tab_middle_upper_hb = BoxLayout(orientation='horizontal', size_hint=STYLES['functional_tab_middle_upper_hb']['sh'])
        functional_tab_middle_upper_hb.add_widget(convert_btn)
        functional_tab_middle_upper_hb.add_widget(change_btn)
        functional_tab_middle_upper_hb.add_widget(backspace_btn)
        functional_tab_middle_hb.add_widget(functional_tab_middle_upper_hb)

        functional_tab_middle_lower_hb = BoxLayout(orientation='horizontal', size_hint=STYLES['functional_tab_middle_lower_hb']['sh'])
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

        keyboard_al = AnchorLayout(size_hint=STYLES['keyboard_al']['sh'])
        keyboard_gl = GridLayout(cols=8, spacing=STYLES['keyboard_gl']['spacing'])
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
        elif instance.action == 'applying_answer':
            self.apply_answer()

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

    def apply_answer(self):
        if not self.answer == None:
            self._interface_._clear()
            self._interface_.signs = [self.answer]
            self.offset_to_end()
            self.output()

    def on_answer_nums(self, instance, value):
        if not value == '':
            value = int(value)
            if 1 < value < 37:
                self.answer_nums = value
                self.output()

    def on_converion_nums_btn_pressed(self, instance):
        self.convertion_mv_ti.text = str(instance.nums)
        self.convert_nums()

    def on_changing_nums_btn_pressed(self, instance):
        self.changing_mv_ti.text = str(instance.nums)
        self.change_nums()

    def fill_conv_table(self):
        self.conv_tables = []
        for sign in self._interface_.signs:
            if type(sign).__name__ == '_numb':
                if not sign.nums == 10:
                    self.conv_tables.append(ConvertionTable(sign.nums, 10, sign))

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
                        
                    text = f'{text}{sign._get_nums_subscriber()} '
                else:
                    text = f'{text} {sign}{CS} '
            else:
                text = f'{text} {sign}'
            if subcursor > cursor and cursor == i:
                is_cursor_inserted = True
                text = f'{text} {CS} '

        self.expression_ti.text = text

        # заполнение ответа
        self.fill_conv_table()
        self.ans_conv_table = []
        try:
            answer = _numb(0)
            answer._apply_numb_properties_to_self(self._commander_._execute_interface_expression(self._interface_))
            self.answer = answer

            if answer.nums != self.answer_nums:
                _answer = answer
                if answer.nums != 10:
                    self.ans_conv_table.append(ConvertionTable(answer.nums, 10, answer))
                    _answer._apply_numb_properties_to_self(_nums._convert_to_dec(_answer))
                if self.answer_nums != 10:
                    self.ans_conv_table.append(ConvertionTable(10, self.answer_nums, _answer))

            print('**************')
            answer.info()
            if answer.nums != answer_nums:
                answer._convert_to(answer_nums)
            # answer.info()
            answer_text = str(answer)
        except Exception as exc:
            logging.critical('MainApp.output cought exception:')
            logging.critical(exc)
            self.answer = None
            self.ans_conv_table = []

        self.answer_ti.text = str(answer_text)

        print('======================================================================================================')

        for convtable in self.conv_tables:
            print(convtable.table)
            print(convtable.table_frct)
            print(convtable.result)
            print('-----------------')
        if self.ans_conv_table != None:
            print('-ans-')
            for anstable in self.ans_conv_table:
                print(anstable.table)
                print(anstable.table_frct)
                print(anstable.result)
                print('-----------------')

        return text, answer_text

if __name__ == '__main__':
    MainApp().run()