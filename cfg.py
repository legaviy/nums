"""
обозначения в комментариях и условные обозначения перменных/ключей:
    - X-СС: система счисления с основанием X;
    - промежуток (в _interface.signs): положение курсора между знаками
    - ГПИ: графический пользовательский интерфейс;
    - команда: программное строковое представление арифметического действия;
    - bgc: background_color;
    - fz: font_size;
    - sh: size_hint;
"""
import logging

class NotEnoughArgumentsException(Exception): # исключения неверного заполнения параметров функции
    def __init__(self, msg='not enough arhuments'):
        logging.critical(msg)
        super().__init__(msg)

class WrongNumeralSystem(Exception): # исключение неверной системы счисления, где nums_req ошибочно подменено на nums
    def __init__(self, nums_req=None, nums=None, msg='wrong numeral system'):
        if not nums_req == None:
            msg = msg + f' ({str(nums_req)} required'
            if not nums == None:
                msg = msg + f' not {str(nums)}'
            msg = msg + ')'
        logging.critical(msg)
        super().__init__(msg)

class WrongType(Exception): # исключения неверного типа аргумента, где type_req ошибочно подменено на _type
    def __init__(self, type_req=None, _type=None, msg='wrong argument\'s type'):
        if not type_req == None:
            msg = msg + f' ({type_req} required'
            if not type(_type).__name__ == None:
                msg = msg + f' not {str(type(_type).__name__)}'
            msg = msg + ')'
        logging.critical(msg)
        super().__init__(msg)

class WrongSignForNumeralSystem(Exception): # исключения неверного знака sign, не входящего в алфавит nums-ой системы
    def __init__(self, sign=None, nums=None, msg='wrong sign for alphabet'):
        if not sign == None and not nums == None:
            msg = msg + f' ({str(sign)} not member of {str(nums)}-numerical system)'
        logging.critical(msg)
        super().__init__(msg)

class MaxLoopIterations(Exception):
    def __init__(self, msg = 'maximum iterations for one loop (check cfg.py)'):
        logging.critical(msg)
        super().__init__(msg)

LATIN_ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

SIGN_ALPHABET = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35']

COMMANDS_ALLOWED = ['+', '-', '*', '/', '**'] # команды, использующиеся в программе, в качестве реализованных

BRACKETS = ['(', ')']

SIGNS_COMMA_LIMIT = 19 # максимальное количество знаков в дробной части

MAX_LOOP_ITERATION = 999 # максимальное количество итераций для циклов, которые могут быть бесконечными при неверных параметров

CURSOR_SIGN = 'I' # обозначение курсора в строке

CURSOR_SIGN_FORMATTED = f'[u][b][color=#ee0000]{CURSOR_SIGN}[/color][/b][/u]' # форматированное обозначение курсора в строке

KEYBOARD_KEYS = ['1', '2', '3', 'A', 'B', 'C', 'D', 'E',
                 '4', '5', '6', 'F', 'G', 'H', 'I', 'J',
                 '7', '8', '9', 'K', 'L', 'M', 'N', 'O',
                 '(', '0', ')', 'P', 'Q', 'R', 'S', 'T',
                 '+', '-', '×', 'U', 'V', 'W', 'X', 'Y',
                 '/', '^', '±', 'Z', '=', ' ', ' ', ' ',] # надписи кнопок основной клавиатуры

KEYS_IS_DEFAULT_EXCEPTIONS = {
    '±': 'changing_pos',
    '=': 'applying_answer',
} # словарь надписей нестандартных кнопок и соответствующие им названия их действий (см. gui.py:MyApp:on_keyboard_btn_pressed); 
  # <<key:str>, <action:str>>
  # key: надпись кнопки; action: название действия, которой соответствует кнопка с надписью key

KEYS_ANALOGUES = {
    '**': '^',
    '*': '×',
} # словарь команд и соответствующие им аналогичные представления в графическом интерфейсе
  # <<command:str>, <gui_analogue>>
  # command: программное представление команды; gui_analogue: представление команды в ГПИ

STYLES = {
    'nums_size': 20,
    'keyboard_btn':
        {
            'fz': '20sp',
            'bgc': (3, 3, 3),
            'color': (0.05, 0.05, 0.05)
        },

    'functional_btn':
        {
            'fz': '15sp',
            'bgc': (2.4, 2.4, 2.4),
            'color': (0.05, 0.05, 0.05)
        },

    'nums_btn':
        {
            'fz': '15sp',
            'bgc': (2.4, 2.4, 2.4),
            'color': (0.05, 0.05, 0.05)
        },

    'nums_mv':
        {
            'sh': [0.75, 0.25],
            'main_bl': {
                'padding': 20,
                'spacing': 5
            },
            'buttons_hb': { 'spacing': 15 },
            'nums_hb': {
                'spacing': 15,
                'padding': 5
            },
        },

    'modalview_btn':
        {
            'bgc': (1.4, 1.4, 1.4),
            'color': (0.05, 0.05, 0.05),
            'sh': [1, 0.8],
            'fz': '15sp',
        },
    
    'modalview_int_textinput':
        {
            'sh': [1, 0.75],
            'fz': '35sp'
        },

    'history_menu_al':
        {
            'sh': [1, 0.05]
        },

    'convertions_menu_al':
        {
            'sh': [0.05, 1]
        },

    'line_al':
        {
            'sh': [0.90, 1]
        },

    'expression_bl':
        {
            'sh': [1, 0.85]
        },

    'expression_ti':
        {
            'fz': '20sp',
            'bgc': (3, 3, 3)
        },

    'answer_bl':
        {
            'sh': [1, 0.15]
        },

    'answer_ti':
        {
            'bgc': (3, 3, 3),
            'sh': [0.8, 1],
            'fz': '15sp',
        },
    
    'answer_nums_ti':
        {
            'bgc': (1, 1, 1),
            'sh': [0.2, 1],
            'fz': '30sp',
        },

    'commands_executions_menu_al':
        { 'sh': [0.05, 1] },

    'middle_hb':
        { 'sh': [1, 0.45] },
        
    'functional_tab_hb':
        { 'sh': [1, 0.1] },
        
    'cursor_offset_left_btn':
        { 'sh': [0.2, 1] },
        
    'cursor_offset_right_btn':
        { 'sh': [0.2, 1] },
        
    'functional_tab_middle_hb':
        { 'sh': [0.6, 1] },
        
    'functional_tab_middle_upper_hb':
        { 'sh': [1, 0.75] },
        
    'functional_tab_middle_lower_hb':
        { 'sh': [1, 0.25] },
        
    'keyboard_al':
        { 'sh': [1, 0.4] },
        
    'keyboard_gl':
        { 'spacing': 1 },
} # словарь стилей элементов ГПИ

def get_command_analogue(value, is_gui_analogue=True): # is_gui_analogue = <bool>: True при получение ГПИ-представление команды; False при получение программного представления
    if is_gui_analogue:
        return KEYS_ANALOGUES[value] if value in KEYS_ANALOGUES else value
    if value in list(KEYS_ANALOGUES.values()):
        for key, val in KEYS_ANALOGUES.items():
            if val == value:
                return key
    return value


def _get_elt_by_i(arr, i): # получить элемент в arr по индексу i
    i = int(abs(i))
    if len(arr) > i:
        return arr[i]
    return None

def _inter_to_letters(arr): # сменить числа больше 9 на буквенный эквивалент в списке arr
    _arr = []
    for x in arr:
        if x > 9:
            _arr.append(_get_elt_by_i(LATIN_ALPHABET, x - 10))
            continue
        _arr.append(x)
    return _arr

def _inter_sign_to_num(sign): # сменить буквенный эквивалент десятичного числа на само число для sign
    if sign in LATIN_ALPHABET:
        return str(SIGN_ALPHABET[LATIN_ALPHABET.index(sign)])
    return str(sign)