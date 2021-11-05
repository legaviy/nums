"""
обозначения в комментариях:
    - X-СС: система счисления с основанием X;
    - промежуток (в _interface.signs): положение курсора между знаками
    - ГПИ: графический пользовательский интерфейс;
    - команда: программное строковое представление арифметического действия;
"""

from exceptions import *

LATIN_ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

SIGN_ALPHABET = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35']

COMMANDS_ALLOWED = ['+', '-', '*', '/', '**'] # команды, использующиеся в программе, в качестве реализованных

BRACKETS = ['(', ')']

SIGNS_COMMA_LIMIT = 19 # максимальное количество знаков в дробной части

MAX_LOOP_ITERATION = 999 # максимальное количество итераций для циклов, которые могут быть бесконечными при неверных параметров

CURSOR_SIGN = 'I' # обозначение курсора в строке

CURSOR_SIGN_FORMATTED = f'[u][b]{CURSOR_SIGN}[/b][/u]' # форматированное обозначение курсора в строке

KEYBOARD_KEYS = ['1', '2', '3', 'A', 'B', 'C', 'D', 'E',
                 '4', '5', '6', 'F', 'G', 'H', 'I', 'J',
                 '7', '8', '9', 'K', 'L', 'M', 'N', 'O',
                 '(', '0', ')', 'P', 'Q', 'R', 'S', 'T',
                 '+', '-', '×', 'U', 'V', 'W', 'X', 'Y',
                 '/', '^', '±', 'Z', ' ', ' ', ' ', ' ',] # надписи кнопок основной клавиатуры

KEYS_IS_DEFAULT_EXCEPTIONS = {
    '±': 'changing_pos',
} # словарь надписей нестандартных кнопок и соответствующие им названия их действий;
  # <<key:str>, <action:str>>
  # key: надпись кнопки; action: название действия, которой соответствует кнопка с надписью key

KEYS_ANALOGUES = {
    '**': '^',
    '*': '×',
} # словарь команд и соответствующие им аналогичные представления в графическом интерфейсе
  # <<command:str>, <gui_analogue>>
  # command: программное представление команды; gui_analogue: представление команды в ГПИ


def _get_command_analogue(value, is_gui_analogue=True): # is_gui_analogue = <bool>: True при получение ГПИ-представление команды; False при получение программного представления
    return KEYS_ANALOGUES[value] if is_gui_analogue else list(KEYS_ANALOGUES.keys())[[val for val in list(KEYS_ANALOGUES.values())].index(value)]

def get_command_analogue(value, is_gui_analogue=True):
    if is_gui_analogue:
        return KEYS_ANALOGUES[value] if value in KEYS_ANALOGUES else value
    if value in list(KEYS_ANALOGUES.values()):
        for key, val in KEYS_ANALOGUES.items():
            if val == value:
                return key
    return value