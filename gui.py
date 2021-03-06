from kivy.app import App
from kivy_elements import (CommandExecutionModalView, ConvertionModalview, KeyboardButton, FunctionalButton, NumsModalview, NumsTextInput,
                            AnchorLayout, Label, GridLayout, Button, BoxLayout)
from cfg import CURSOR_SIGN_FORMATTED, LATIN_ALPHABET, logging, CURSOR_SIGN_FORMATTED, KEYBOARD_KEYS, KEYS_IS_DEFAULT_EXCEPTIONS, get_command_analogue, STYLES
from interface import ConvertionTable
from numb import _nums, _numb
from kivy.graphics import Color, Rectangle

class MainApp(App):
    answer = None
    answer_nums = 10
    conv_tables = []
    ans_conv_table = []
    buffer = None

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

        self.convertions_menu_btn.on_release = self.open_conv_mv
        self.commands_executions_menu_btn.on_release = self.open_command_mv

        self.undo_btn.on_release = self.undo
        self.redo_btn.on_release = self.redo

        self.answer_nums = 10
        self.answer = _numb(0)

        self.output()
        self._interface_._save()

        return self.main_layout

    def build_interface(self):
        self.convertion_mv = NumsModalview()
        self.convertion_mv_ti = self.convertion_mv.ti
        self.convertion_mv_btn_ok = self.convertion_mv.btn_ok

        self.changing_mv = NumsModalview()
        self.changing_mv_ti = self.changing_mv.ti
        self.changing_mv_btn_ok = self.changing_mv.btn_ok

        history_menu_al = AnchorLayout(size_hint=STYLES['history_menu_al']['sh'])
        history_menu_bl = BoxLayout(orientation='horizontal')
        undo_btn = Button(text='undo')
        redo_btn = Button(text='redo')
        history_menu_bl.add_widget(undo_btn)
        history_menu_bl.add_widget(redo_btn)
        history_menu_al.add_widget(history_menu_bl)
        self.undo_btn = undo_btn
        self.redo_btn = redo_btn


        convertions_menu_al = AnchorLayout(size_hint=STYLES['convertions_menu_al']['sh'], anchor_x='left', anchor_y='center')
        convertions_menu_btn = Button(text='...')
        convertions_menu_al.add_widget(convertions_menu_btn)
        self.convertions_menu_btn = convertions_menu_btn
        self.conv_mv = ConvertionModalview()


        line_al = AnchorLayout(size_hint=STYLES['line_al']['sh'], anchor_x='center', anchor_y='center')
        line_bl = BoxLayout(orientation='vertical')
        expression_bl = BoxLayout(size_hint=STYLES['expression_bl']['sh'])
        expression_ti = Label(font_size=STYLES['expression_ti']['fz'], halign='left', valign='top', markup=True)
        expression_bl.add_widget(expression_ti)

        answer_bl = BoxLayout(orientation='horizontal', size_hint=STYLES['answer_bl']['sh'])
        answer_ti = Label(font_size=STYLES['answer_ti']['fz'], size_hint=STYLES['answer_ti']['sh'], halign='left', valign='top', markup=True)
        answer_nums_ti = NumsTextInput(font_size=STYLES['answer_nums_ti']['fz'], background_color=STYLES['answer_nums_ti']['bgc'], size_hint=STYLES['answer_nums_ti']['sh'], text='10', foreground_color=(3,3,3))
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
        self.command_execution_mv = CommandExecutionModalView()
        self.commands_executions_menu_btn = commands_executions_menu_btn


        middle_hb = BoxLayout(orientation='horizontal', size_hint=STYLES['middle_hb']['sh'])
        middle_hb.add_widget(convertions_menu_al)
        middle_hb.add_widget(line_al)
        middle_hb.add_widget(commands_executions_menu_al)


        functional_tab_hb = BoxLayout(orientation='horizontal', size_hint=STYLES['functional_tab_hb']['sh'])

        cursor_offset_left_btn = FunctionalButton('<-')
        cursor_offset_left_btn.size_hint = STYLES['cursor_offset_left_btn']['sh']
        convert_btn = FunctionalButton('convert')
        convert_btn.on_release = self.convertion_mv.open
        change_btn = FunctionalButton('change/add')
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
        main_layout.add_widget(history_menu_al)
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

                if key in KEYS_IS_DEFAULT_EXCEPTIONS: # ?????????????????? ???????????? ???? ?????????????? ???????????????????? ???? ?????????????? ????????????
                    btn.is_default = False
                    btn.action = KEYS_IS_DEFAULT_EXCEPTIONS[key] # ???????????????????????? ???????????????????? ???????????????? ????????????????, ???? ?????????????? ???????????????? ???????????? ????????????????

                self.keyboard_gl.add_widget(btn)

    def on_keyboard_btn_press(self, instance):
        if instance.is_default: # ???????????????????? ?????????????????????? ????????????
            value = instance.text
            if value in LATIN_ALPHABET + [str(x) for x in range(10)] and self._interface_.is_numb:
                if not _nums._num_is_valid_for_nums(value, self._interface_.signs[self._interface_.cursor].nums) == True:
                    return
            self._interface_._input(get_command_analogue(value, False))
            self.output()
            self._interface_._save()
        elif instance.action == 'changing_pos': # ?????????????????????? ?????????????????????????? ????????????
            self.change_positive_of_numb()
            self._interface_._save()
        elif instance.action == 'applying_answer':
            self.apply_answer()
            self._interface_._save()
        elif instance.action == 'cut':
            self.cut()
        elif instance.action == 'copy':
            self.copy()
        elif instance.action == 'paste':
            self.paste()

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
        self._interface_._save()

    def backspace(self):
        self._interface_._delete()
        self.output()
        self._interface_._save()

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
            self._interface_._save()

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
            self._interface_._save()

    def change_positive_of_numb(self):
        if self._interface_.is_numb:
            self._interface_.signs[self._interface_.cursor]._change_pos()
            self.output()

    def apply_answer(self):
        if not self.answer == None:
            self._interface_._save()
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
                    numb = _numb(sign)
                    self.conv_tables.append(ConvertionTable(sign.nums, 10, numb))

    def open_conv_mv(self):
        self.conv_mv.set_conv_tables(self.conv_tables + self.ans_conv_table)
        self.conv_mv.fill()
        self.conv_mv.open()

    def open_command_mv(self):
        self.command_execution_mv.set_commands(self._commander_.commands_history)
        self.command_execution_mv.fill()
        self.command_execution_mv.open()

    def undo(self):
        self._interface_._offset_history_step(True)
        self.output()

    def redo(self):
        self._interface_._offset_history_step(False)
        self.output()

    def copy(self):
        if self._interface_.is_numb and self._interface_.cursor == self._interface_.subcursor:
            self.buffer = _numb(self._interface_.signs[self._interface_.cursor])
    
    def cut(self):
        if self._interface_.cursor == self._interface_.subcursor and self._interface_.is_numb:
            self.copy()
            self._interface_.signs.pop(self._interface_.cursor) # ?????????????? ???????? ???? ????????????
            if self._interface_.cursor == 0 and len(self._interface_.signs) == 0: # ???????? ???????????? ?????????????????? ?? ???????????? ????????????
                self._interface_._clear()
            else:
                self._interface_.cursor -= 1 # ???????????????? ???????????? ?? ???????????????????? ????????????????????
            if not (self._interface_.cursor == self._interface_.subcursor):
                self._interface_.is_numb = False
                self._interface_.is_frct = False
                self._interface_.numbcursor = 0
            self.output()
            self._interface_._save()

    def paste(self):
        if (not self._interface_.cursor == self._interface_.subcursor) and not self._interface_.is_numb:
            self._interface_._change_nums(10)
            self._interface_.signs[self._interface_.cursor]._apply_numb_properties_to_self(self.buffer)
            self.output()
            self._interface_._save()

    def output(self):
        self.expression_ti.text = ''
        self._commander_._clear_history()
        CS = CURSOR_SIGN_FORMATTED
        cursor = self._interface_.cursor
        subcursor = self._interface_.subcursor
        numbcursor = self._interface_.numbcursor
        signs = self._interface_.signs
        is_numb = self._interface_.is_numb
        is_frct = self._interface_.is_frct
        is_cursor_inserted = False
        # ???????????????????? ??????????????????
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
        self.fill_answer()

    def fill_answer(self):
        self.fill_conv_table()
        self.ans_conv_table = []
        answer_text = '...'
        try:
            answer = _numb(self._commander_._execute_interface_expression(self._interface_))
            self.answer = answer
            if answer.nums != self.answer_nums:
                _answer = _numb(answer)
                if answer.nums != 10:
                    self.ans_conv_table.append(ConvertionTable(answer.nums, 10, _answer))
                    _answer._apply_numb_properties_to_self(_nums._convert_to_dec(_answer))
                if self.answer_nums != 10:
                    answer_ = _numb(_answer)
                    self.ans_conv_table.append(ConvertionTable(10, self.answer_nums, answer_))
            if answer.nums != self.answer_nums:
                answer._convert_to(self.answer_nums)
            answer_text = str(answer)
        except Exception as exc:
            logging.critical('MainApp.output cought exception:')
            logging.critical(exc)
            self.answer = None
            self.ans_conv_table = []
        self.answer_ti.text = str(answer_text)

        return answer_text

if __name__ == '__main__':
    MainApp().run()