from cfg import WrongType, LATIN_ALPHABET, SIGN_ALPHABET, NotEnoughArgumentsException, SIGNS_COMMA_LIMIT, WrongNumeralSystem

class _nums: # класс статических методов для перевода чисел и вспомогательных статических методов
    @staticmethod        
    def _get_frct(numb): # вернуть список знаков дробной части числа numb
        if type(numb).__name__ in ['str', 'int', 'float']:
            numb = float(numb)
            if numb % 1 == 0:
                return []
            return _nums._get_rid_of_e(numb).split('.')[1] if 'e' in str(numb) else [char for char in str(numb).split('.')[1]]
        else:
            raise WrongType('number-supporting', numb)
    
    @staticmethod
    def _inter_to_letters(arr): # сменить числа больше 9 на буквенный эквивалент в списке arr
        _arr = []
        for x in arr:
            if x > 9:
                _arr.append(_nums._get_elt_by_i(LATIN_ALPHABET, x - 10))
                continue
            _arr.append(x)
        return _arr

    @staticmethod
    def _inter_to_num(arr): # сменить буквенный эквивалент десятичного числа на само число в списке arr
        _arr = []
        for x in arr:
            if x in LATIN_ALPHABET:
                _arr.append(SIGN_ALPHABET[LATIN_ALPHABET.index(x)])
                continue
            _arr.append(x)
        return _arr

    @staticmethod
    def _inter_sign_to_num(sign): # сменить буквенный эквивалент десятичного числа на само число для sign
        if sign in LATIN_ALPHABET:
            return str(SIGN_ALPHABET[LATIN_ALPHABET.index(sign)])
        return str(sign)
    
    @staticmethod
    def _get_elt_by_i(arr, i): # получить элемент в arr по индексу i
        i = int(abs(i))
        if len(arr) > i:
            return arr[i]
        return None
    
    @staticmethod
    def _rem_nulls(arr): # удалить нули в начале списка 
        if _nums._get_elt_by_i(arr, 0) == 0 and len(arr) > 1:
            arr.remove(0)
            return _nums._rem_nulls(arr)
        return arr

    @staticmethod
    def _rem_nulls_reverse(arr): # удалить нули в конце списка 
        arr_ = arr
        arr_.reverse()
        arr_ = _nums._rem_nulls(arr_)
        arr_.reverse()
        return arr_
    
    @staticmethod
    def _reverse_arr(arr): # вернуть перевёрнутый список
        arr.reverse()
        return arr

    @staticmethod
    def _from_dec(nums, numb=None, intg=None) -> list(): # перевести число dig в систему счисления с основанием num
        dig = None
        if intg == None and not numb == None:
            dig = int(''.join([str(elt) for elt in numb.intg]))
        elif numb == None and not intg == None:
            dig = intg
        else:
            raise(NotEnoughArgumentsException)
        arr = [] # список переведённых чисел в систему с основанием num
        mod = dig % nums # остаток деления
        div = dig // nums # целое от частного
        arr.append(mod)
        while div > 0: # пока частное (предыдущее частное, поделённое на основание системы счисления) остаётся больше нуля, добавлять остаток от деления
            mod = div % nums # остаток от деления
            div //= nums # целая часть от деления
            arr.append(mod)
            if div < nums: # если частное меньше основания системы, то оно сразу добавляется в список, и цикл преывается
                arr.append(div)
                break
        return _nums._inter_to_letters(_nums._rem_nulls(_nums._reverse_arr(arr)))

    @staticmethod
    def _from_dec_fract(nums, numb=None, frcts=None) -> list(): # перевести дробную часть fract в
        frct = None
        if frcts == None and not numb == None:
            frct = (''.join([str(elt) for elt in numb.frct]))
        elif numb == None and not frcts == None:
            frct = frcts
        else:
            raise(NotEnoughArgumentsException)
        arr = []  # список переведённых чисел в систему с основанием num
        mul = float('0.' + ''.join([elt for elt in str(frct)])) # число типа float через объединения строк: '0.' и объеденённый в строку список дробной части
        n = 0 # счётчик, не позволяющий добавить в дробную часть больше знаков, чем SIGNS_COMMA_LIMIT
        while n <= SIGNS_COMMA_LIMIT: 
            mul *= nums # умножение дробной части на основание системы
            arr.append(int(mul)) # добавить целую часть от умножения в список
            mul = float('0.' + ''.join([str(elt) for elt in _nums._get_frct(mul)]))
            n += 1
        return _nums._inter_to_letters(_nums._rem_nulls_reverse(arr))

    @staticmethod
    def _convert_from_dec(numb, nums): # вернуть конвертированное число из 10-СС в nums-СС
        nums = int(nums)
        if numb.nums == 10:
            intg = _nums._from_dec(nums, numb=numb) # список знаков целой части
            frct = _nums._from_dec_fract(nums, numb=numb) # список знаков дробной части
            frct = [] if frct == [0] else frct
            numb._set_frct_empty_arr()
            return _numb(dec=None, pos=numb.pos, intg=intg, frct=frct, nums=nums)
        else:
            raise(WrongNumeralSystem(10, numb.nums))

    @staticmethod
    def _get_rid_of_e(num): # избавиться от представления числа в стандартном виде
        _num = num
        num = str(num).lower()
        if 'e' in num:
            grade = num.split('e')[1]
            if '-' in grade:
                grade = grade.replace('-', '')
                grade = -1 * int(''.join(_nums._rem_nulls([char for char in grade])))
            else:
                grade = int(''.join(_nums._rem_nulls([char for char in num])))
            _num = '{:.19f}'.format(float(num.split('e')[0]) * (10 ** grade))
        return _num

    @staticmethod
    def _to_dec(nums=None, numb=None, intg=None, is_fract=False): # вернуть конвертированное число из nums-СС в 10-СС; numb:_numb; intg линейное значение числа; is_fract перевод для дробной части
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
        intgs = ''.join([char for char in intgs])
        intgs = intgs if is_fract else intgs[::-1]
        num = 0 # переведённое значение в систему с основанием nums
        grade = 1 if is_fract else 0 # степень возведения для каждого знака
        for char in intgs:
            num += int(_nums._inter_sign_to_num(char)) * nums ** (mode * grade)
            grade += 1
        if 'e' in str(num) and is_fract:
            num = _nums._get_frct(num)
        else:
            num = str(''.join(_nums._get_frct(num)) if is_fract else num)
        return [str(char) for char in num]

    @staticmethod
    def _convert_to_dec(numb, nums=None): # вернуть конвертированное число из nums-СС в 10-СС
        nums = int(nums if not nums == None else numb.nums)
        intg = _nums._to_dec(nums, numb=numb)
        frct = _nums._to_dec(nums, numb=numb, is_fract=True)
        frct = [] if frct == [0] else frct
        numb._set_frct_empty_arr()
        return _numb(dec=None, pos=numb.pos, intg=intg, frct=frct, nums=10)

    @staticmethod
    def _get_nums_alphabet(nums): # получить список всех знаков в nums-СС
        nums = int(nums)
        if nums < 37 and nums > 1:
            return ([str(x) for x in range(10)] + LATIN_ALPHABET)[:nums]
        else:
            raise WrongNumeralSystem('2-36', nums)

    @staticmethod
    def _num_is_valid_for_nums(numb, nums): # входят ли знаки числа num в алфавит nums-СС
        num = (numb._get_intg_str() + numb._get_frct_str()) if type(numb).__name__ == '_numb' else str(numb).replace('-', '').replace(',', '.').replace('.', '').upper()
        if len(num) == 0:
            return False 
        alphabet = _nums._get_nums_alphabet(nums)
        for char in num:
            if char in alphabet:
                continue
            return char
        return True

class _numb: # число в nums'ной системе счисления
    pos = True # положительно ли число
    intg = None # список знаков целой части числа
    frct = None # список знаков дробной части числа
    nums = 10 # значение основания системы счисления числа
    def __init__(self, dec=None, pos=True, intg=None, frct=None, nums=10):
        if dec == None and not None in [pos, intg, frct, nums]: # если введены свойства, описывающие экземляр, то присвоить ему эти свойства
            self.pos = pos 
            self.intg = intg
            self.frct = frct
            self.nums = nums
        elif not dec == None and (type(dec).__name__ in ['str', 'int', 'float']): # если введено десятичное число типа float/int, то получить необходимые свойства и присвоить их экземпляру
            dec = float(dec)
            self.pos = dec >= 0
            self.intg = [ch for ch in str(abs(int(dec)))]
            self.frct = _nums._get_frct(dec)
            self.nums = 10
        else:
            raise(NotEnoughArgumentsException)

    def _set_frct_empty_arr(self): # нет слов
        self.frct = [] if (self.frct if not type(self.frct).__name__ == 'str' else self.frct.replace(' ', '')) in [None, [], ''] else self.frct

    def _get_intg_str(self): # строковое представление целой части числа
        return ''.join([str(char) for char in self.intg])

    def _get_frct_str(self): # строковое представление дробной части числа
        return '0' if self.frct == [] else ''.join([str(char) for char in self.frct])

    def _get_pos_str(self):
        return '' if self.pos else '-'

    def _get_nums_subscriber(self):
        return f'[size=10]{self.nums}[/size]'

    def __str__(self): # строковое представление числа
        return f'{self._get_pos_str()}{self._get_intg_str()},{self._get_frct_str()}{self._get_nums_subscriber()}'

    def _apply_numb_properties_to_self(self, numb): # применить к данному экземпляру свойства экземпляра numb
        self.pos = numb.pos
        self.intg = numb.intg
        self.frct = numb.frct
        self.nums = numb.nums

    def _convert_to_dec(self): # конвертировать данный экземпляр в 10-СС
        self._apply_numb_properties_to_self(_nums._convert_to_dec(self))

    def _convert_from_dec(self, nums): # конвертировать данный экземпляр из 10-СС в nums-СС
        self._apply_numb_properties_to_self(_nums._convert_from_dec(self, nums))

    def _convert_to(self, nums): # конвертировать данный экземпляр из текущей-СС в nums-СС
        self._convert_to_dec()
        self._convert_from_dec(int(nums))

    def _get_float(self): # получить числовое представление данного экземлпяра
        return float(f'{self._get_pos_str()}{self._get_intg_str()}.{self._get_frct_str()}')

    def _change_pos(self, pos=None): # сменить знак числа на противоположный
        self.pos = pos if not pos == None else not self.pos

    def info(self): # служебная функция для вывода свойств данного экземпляра
        print('self.pos', self.pos, f'({"+" if self.pos else "-"})')
        print('self.intg', self.intg)
        print('self.frct', self.frct)
        print('self.nums', self.nums)