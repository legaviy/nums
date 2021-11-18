from numb import _numb, _nums
from cfg import COMMANDS_ALLOWED, BRACKETS, MAX_LOOP_ITERATION, WrongNumeralSystem, WrongSignForNumeralSystem, NotEnoughArgumentsException, MaxLoopIterations, SIGNS_COMMA_LIMIT

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

        self.is_conv = False if int(self.numb.nums) == int(self.result.nums) else True

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

def _new_sign_list(signs):
    arr = []
    for sign in signs:
        if type(sign).__name__ == '_numb':
            arr.append(_numb(sign))
        else:
            arr.append(sign)
    return arr

class _history_step:
    cursor = 0
    subcursor = 0
    numbcursor = 0
    is_frct = False # курсор находится на числе И курсор (numbcursor) находится в дробной части числа
    is_numb = True # курсор находится на числе
    signs = None # список знаков в строке
    prev_step = None
    next_step = None
    def __init__(self, interface, prev_step):
        self.prev_step = prev_step
        self.cursor = interface.cursor
        self.subcursor = interface.subcursor
        self.numbcursor = interface.numbcursor
        self.is_frct = interface.is_frct
        self.is_numb = interface.is_numb
        self.signs = _new_sign_list(interface.signs)
        if not prev_step == None:
            self.prev_step.next_step = self

class _command_execution: # выполнение команды, включающее в себя команда, два соответсвтующее ей операнда, и результат операции
    command = None
    left_operand = None
    right_operand = None
    result = None
    _str = None
    def __init__(self, command, left_operand, right_operand, result):
        self.command = command
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

    def __str__(self): # строковое представление команды и её результата
        return f'{self.command}({self.left_operand}, {self.right_operand}) -> {self.result}'

class _commander: # класс выполнения выражений и арифметических операций
    commands_history = [] # история выполнения команд
    _buffer = {} # буфер для хранения временных данных арифметических операций
    _expression_results = [] 
    _expressions = []
    def __init__(self):
        pass
    
    def _clear_history(self):
        self.commands_history = []

    def _execute(self, command, left_operand, right_operand, result_nums=10): # исполнение команды с возвращением её результата
        left_operand_dec = _nums._convert_to_dec(left_operand)
        right_operand_dec = _nums._convert_to_dec(right_operand)
        self._buffer['left_operand_dec'] = float(left_operand_dec._get_float())
        self._buffer['right_operand_dec'] = float(right_operand_dec._get_float())

        if command == '+':
            result_dec = self._addition()
        elif command == '-':
            result_dec = self._substruction()
        elif command == '*':
            result_dec = self._multiplication()
        elif command == '/':
            result_dec = self._division()
        elif command == '**':
            result_dec = self._exponentiation()
        else:
            raise(NotEnoughArgumentsException(f'command {command} does not exist'))

        _execution_result = _nums._convert_from_dec(_numb(result_dec), result_nums)
        self.commands_history.append(_command_execution(command, left_operand, right_operand, _execution_result))
        self._buffer.clear()
        return _execution_result

    def _addition(self): # сложение
        return self._buffer['left_operand_dec'] + self._buffer['right_operand_dec']

    def _substruction(self): # разница
        return self._buffer['left_operand_dec'] - self._buffer['right_operand_dec']

    def _multiplication(self): # умножение
        return self._buffer['left_operand_dec'] * self._buffer['right_operand_dec']

    def _division(self): # деление
        return self._buffer['left_operand_dec'] / self._buffer['right_operand_dec']

    def _exponentiation(self): # возведение в степень
        return self._buffer['left_operand_dec'] ** self._buffer['right_operand_dec']

    @staticmethod
    def _is_one_sign_in_arr(signs, arr): # находится ли хотя бы один элемент signs в arr
        for sign in signs:
            if sign in arr:
                return True
        return False

    def _execute_polynom_by_sign(self, signs, polynom): # выполнить команды из signs для многочлена polynom
        _iteration = 0
        while _commander._is_one_sign_in_arr(polynom, signs): # пока в многочлене есть команды из signs
            _iteration += 1
            if _iteration > MAX_LOOP_ITERATION:
                raise(MaxLoopIterations)
            for i, x in enumerate(polynom):
                if x in signs:
                    expression = _expression(polynom[i-1], polynom[i+1], x) # получить выражение с командой x и операндами по обе стороны от неё
                    self._expressions.append(expression) # добавить полученное выражение в список всех выражений
                    result = expression._execute(self) # получить результат выражения
                    for x in range(3): # удалить из выражение команду x и оба операнда
                        polynom.pop(i - 1)
                    polynom.insert(i - 1, result) # на место левого операнда вставить результат выражения
        return polynom # если в signs не входят сложение и разница, то вернётся оставшийся многочлен с выполненными действиями из signs; иначе вернётся массив с одним элементом - результатом изначального многочлена

    def _execute_polynom(self, polynom): # выполнить весь многочлен polynom
        """
        polynom = self._execute_polynom_by_sign(['**'], polynom)
        polynom = self._execute_polynom_by_sign(['*', '/'], polynom)
        result = self._execute_polynom_by_sign(['+', '-'], polynom)[0]
        return result[0]
         преобразовано в следующую строку
        """ 
        return self._execute_polynom_by_sign(['+', '-'], self._execute_polynom_by_sign(['*', '/'], self._execute_polynom_by_sign(['**'], polynom)))[0]

    @staticmethod
    def print_signs(expression): # служебная функция для выводы всех знаков в строчку
        s = ''
        for sign in expression:
            s = s + str(sign)
        print(s)
        return s

    def _execute_interface_expression(self, interface): # выполнить сложное выражение
        expression = list(interface.signs)
        _iteration = 0
        while '(' in expression: # пока в оставшемся выражении остаются скобки
            _iteration += 1
            if _iteration > MAX_LOOP_ITERATION:
                raise(MaxLoopIterations)
            open_bracket_index = 0 # индекс открывающей скобки в списке знаков
            close_bracket_index = 0 # индекс закрывающей скобки в списке знаков
            polynom = expression # выделяемый многочлен, обособленный скобками
            for i, x in enumerate(expression): # найти в выражении последнюю открывающую скобку и выделить от неё (невключительно) до конца выражение
                if x == '(':
                    open_bracket_index = i
                    polynom = expression[i+1:]
            for i, x in enumerate(polynom): # найти первую закрывающую скобку и обрезать часть выражения от неё (включительно) до конца выражения
                if x == ')':
                    close_bracket_index = i + open_bracket_index
                    polynom = polynom[:i]
                    break
            result = self._execute_polynom(polynom) # получить результат обособленного скобками многочлена
            for x in range(close_bracket_index - open_bracket_index + 2): # удалить из оставшегося выражения обособленный многочлен
                expression.pop(open_bracket_index)
            expression.insert(open_bracket_index, result) # вставить результат многочлена вместо него и скобок
        return self._execute_polynom(expression) # вернуть результат многочлена, получившегося после замены выражений, обособленных скобками, на их результаты

class _expression: # выражение, включающее в себя команду и два операнда
    left_operand = None
    right_operand = None
    command = None
    def __init__(self, left_operand, right_operand, command):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.command = command

    def _execute(self, _commander_):
        left_operand = None
        right_operand = None
        if type(self.left_operand).__name__ == 'str':
            left_operand = _commander_._expression_results[self.left_operand] 
        else:
            left_operand = self.left_operand
        if type(self.right_operand).__name__ == 'str':
            right_operand = _commander_._expression_results[self.right_operand] 
        else:
            right_operand = self.right_operand
        result = _commander_._execute(self.command, left_operand, right_operand)
        _commander_._expression_results.append(result)
        return result

class _interface: # класс ввода выражения
    """
        если cursor и subcursor равны, то курсор находится на конкретном знаке, который можно получить через self.signs[self.cursor];
        если subcursor больше cursor, то курсор находится между знаками (между signs[cursor] и signs[subcursor]) или в конце строки (если subcursor равен len(signs));
        если курсор находится на конкретном числе (типа _numb), то при смещении курсора меняется только значение numbcursor, который находится между цифрами (_numb_._part[numbcursor] и _numb_._part[numbcursor + 1];
            где _numb_ = self.signs[self.cursor], _part - целая/дробная часть числа (в зависимости от is_frct))
    """
    cursor = 0
    subcursor = 0
    numbcursor = 0
    is_frct = False # курсор находится на числе И курсор (numbcursor) находится в дробной части числа
    is_numb = True # курсор находится на числе
    signs = [] # список знаков в строке
    history_step = None

    def __init__(self):
        self._clear()
        self.history_step = _history_step(self, None)

    def _print_signs(self):
        s = ''
        for sign in self.signs:
            s = s + str(sign) + ' '
        print(s)
        return s[:-1]

    def _clear(self): # очистить строку
        self.signs = [_numb(0)]
        self.cursor = 0
        self.subcursor = 0
        self.numbcursor = 0
        self.is_frct = False
        self.is_numb = True

    def _offset(self, is_to_right=True): # сместить курсор: вправо (вперёд) при is_to_right=True, влево (назад) при is_to_right=False
        if self.is_numb:
            if self.is_frct:
                if is_to_right:
                    if self.numbcursor == len(self.signs[self.cursor].frct): # если курсор находится после последней цифры дробной части, то 
                        # выйти из дробной части в промежуток между текущим знаком и следующим знаком
                        self.numbcursor = 0
                        self.subcursor += 1
                        self.is_numb = False
                        self.is_frct = False
                    else:
                        self.numbcursor += 1 # сместить курсор вправо
                else:
                    if self.numbcursor == 0: # если курсор находится в начале дробной части
                        self.is_frct = False
                        self.numbcursor = len(self.signs[self.cursor].intg) # переместить курсор в конец дробной части
                    else:
                        self.numbcursor -= 1 # сместить курсор влево
            else:
                if is_to_right:
                    if self.numbcursor == len(self.signs[self.cursor].intg): # если курсор находится после последней цифры целой части, то
                        # перейти в начало дробной части
                        self.is_frct = True
                        self.numbcursor = 0
                    else:
                        # сместить курсор вправо
                        self.numbcursor += 1
                else:
                    if self.numbcursor == 0: # если курсор находится в начале целой части
                        # выйти из текущего числа в предудущий промежуток
                        self.is_numb = False
                        self.is_frct = False
                        self.cursor -= 1
                    else:
                        self.numbcursor -= 1 # сместить курсор влево
        else:
            if is_to_right and self.subcursor < len(self.signs): # если курсор находится не в конце строки (при смещении вправо)
                if self.cursor == self.subcursor: # если курсор находится на конкретном знаке
                    self.subcursor += 1 # сместить курсор в следующий промежуток между знаками
                elif self.cursor < self.subcursor: # если курсор находится между знаками
                    self.cursor += 1 # сместить курсор на следующий знак
            elif self.subcursor > 0 and not is_to_right: # если курсор находится не в начале (при смещении влево)
                if self.cursor == self.subcursor: # если курсор находится на конкретном знаке
                    self.cursor -= 1 # сместить курсор в предудущий промежуток между знаками
                elif self.cursor < self.subcursor: # если курсор находится между знаками
                    self.subcursor -= 1 # сместить курсор на предудущий знак
            elif self.subcursor == self.cursor == 0 and not is_to_right: # если курсор стоит на первом знаке (не число) и при смещении влево
                self.cursor -= 1 # сместить курсор в самое начало
            if self.cursor == self.subcursor and type(self.signs[self.subcursor]).__name__ == '_numb': # если курсор после смещения перешёл на число
                self.is_numb = True
                if is_to_right: # если смещение производилось направо, то
                    # то перенести курсор в начало целой части числа
                    self.numbcursor = 0
                    self.is_frct = False
                else:
                    # перенести курсор в конец дробной части числа
                    self.numbcursor = len(self.signs[self.subcursor].frct)
                    self.is_frct = True

    def _offset_left(self):
        self._offset(False)

    def _offset_to_begin(self):
        self.cursor = -1
        self.subcursor = 0
        self.numbcursor = 0
        self.is_numb = False
        self.is_frct = False

    def _offset_to_end(self):
        self.cursor = len(self.signs) - 1
        self.subcursor = len(self.signs)
        self.numbcursor = 0
        self.is_numb = False
        self.is_frct = False

    def _input(self, val): # добавить знак/цифру
        val = str(val).upper()
        if self.subcursor > self.cursor and val in BRACKETS + COMMANDS_ALLOWED: # если курсор находится между знаками (не для цифр)
            self.signs.insert(self.subcursor, val) # вставить val между self.signs[self.cursor] и self.signs[self.subcursor]
            self.subcursor += 1 # сдвинуть курсор между вставленным и следующем знаком
            self.cursor += 1
        elif self.subcursor == self.cursor: # если курсор находится на знаке
            if self.is_numb and not (val in BRACKETS + COMMANDS_ALLOWED): # если курсор находится на числе (для цифр)
                current_numb = self.signs[self.cursor]
                if not _nums._num_is_valid_for_nums(val, current_numb.nums) == True:
                    raise(WrongSignForNumeralSystem(val, current_numb.nums))
                if self.is_frct: # если курсор в дробной части числа
                    current_numb.frct.insert(self.numbcursor, val) # вставить в дробную часть текущего числа val на месте self.numbcursor
                else: # если курсор в целой части числа
                    if current_numb._get_intg_str() == '0': # если целая часть числа равна нулю
                        current_numb.intg[0] = val # заменить ноль в целой части на val
                        self.numbcursor = 0
                    else:
                        current_numb.intg.insert(self.numbcursor, val) # вставить в целую часть val на месте self.numbcursor
                self.numbcursor += 1 # переместить numbcursor после добавленной цифры
            else: # если курсор находится не на числе
                if val in COMMANDS_ALLOWED + BRACKETS: # не для цифр
                    self.signs[self.cursor] = val # заменить текущий знак на val
                    self.numbcursor = 0
                    self.is_numb = False
                    self.is_frct = False
                    # self.subcursor += 1 # сдвинуть курсор между вставленным и следующем знаком
                    # self.cursor += 1

    def _delete(self): # удалить знак/цифру
        if self.cursor > -1:
            if self.is_numb and self.numbcursor > 0: # если курсор на конкретном числе и не в начале его целой/дробной части
                current_numb = self.signs[self.cursor]
                if self.is_frct:
                    current_numb.frct.pop(self.numbcursor - 1) # удалить предыдущую цифру в части дробной
                else:
                    current_numb.intg.pop(self.numbcursor - 1) # удалить предыдущую цифру в части целой
                self.numbcursor -= 1 # сместить курсор влево
            else:
                if self.cursor == self.subcursor: # если курсор находится на конкретном знаке
                    self.signs.pop(self.cursor) # удалить знак из списка
                    if self.cursor == 0 and len(self.signs) == 0: # если курсор находится в начале строки
                        self._clear()
                    else:
                        self.cursor -= 1 # сместить курсор в предыдущий промежуток
                elif self.subcursor > self.cursor: # если курсор находится в промежутке
                    self.signs.pop(self.cursor) # удалить знак из списка
                    if self.cursor == 0 and len(self.signs) == 0: # если курсор находится в начале строки
                        self._clear()
                    else:
                        # сместить курсор в предыдущий промежуток
                        self.cursor -= 1
                        self.subcursor -= 1
                
    def _change_nums(self, nums): # сменить СС текущего числа ИЛИ добавить число в промежуток с nums-СС
        if 1 < nums < 37:
            if self.is_numb and _nums._num_is_valid_for_nums(self.signs[self.cursor], nums) == True: # если курсор находится (на знаке И на числе) И переводимое число подходит для nums-СС
                self.signs[self.cursor].nums = nums # сменить СС текущего числа
            elif self.subcursor > self.cursor: # если курсор находится между знаками
                numb = _numb(0)
                numb.nums = int(nums)
                self.signs.insert(self.subcursor, numb) # добавить numb между вставленным числом и следующем знаком
                self.cursor += 1 # переместить курсор на добавленное число
                self.is_numb = True
                self.is_frct = False
                self.numbcursor = 0
        else:
            raise(WrongNumeralSystem('2-36', nums))
    
    def _convert_nums(self, nums): # конвертировать экземпляр числа, на котором находится курсор, в nums-СС
        if 1 < nums < 37:
            if self.cursor == self.subcursor and self.is_numb:
                self.signs[self.cursor]._convert_to(nums)
                self.is_frct = False
                self.numbcursor = 0
        else:
            raise(WrongNumeralSystem('2-36', nums))

    def _save(self): # сохранить текущее выражение в историю изменений
        self.history_step = _history_step(self, self.history_step)

    def _offset_history_step(self, is_undo=True):
        history_step = self.history_step.prev_step if is_undo and not self.history_step.prev_step == None else (self.history_step.next_step if not self.history_step.next_step == None and not is_undo else None)
        if not history_step == None:
            self.cursor = history_step.cursor
            self.subcursor = history_step.subcursor
            self.numbcursor = history_step.numbcursor
            self.is_frct = history_step.is_frct
            self.is_numb = history_step.is_numb
            self.signs = _new_sign_list(history_step.signs)
            self.history_step = history_step

_commander_ = _commander()
_interface_ = _interface()