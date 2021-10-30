class NotEnoughArgumentsException(Exception): # исключения неверного заполнения параметров функции
    def __init__(self, msg='not enough arhuments'):
        super().__init__(msg)

class WrongNumeralSystem(Exception): # исключение неверной системы счисления, где nums_req ошибочно подменено на nums
    def __init__(self, nums_req=None, nums=None, msg='wrong numeral system'):
        if not nums_req == None:
            msg = msg + f' ({str(nums_req)} required'
            if not nums == None:
                msg = msg + f' not {str(nums)}'
            msg = msg + ')'
        super().__init__(msg)

class WrongType(Exception): # исключения неверного типа аргумента, где type_req ошибочно подменено на _type
    def __init__(self, type_req=None, _type=None, msg='wrong argument\'s type'):
        if not type_req == None:
            msg = msg + f' ({type_req} required'
            if not type(_type).__name__ == None:
                msg = msg + f' not {str(type(_type).__name__)}'
            msg = msg + ')'
        super().__init__(msg)

class WrongSignForNumeralSystem(Exception): # исключения неверного знака sign, не входящего в алфавит nums-ой системы
    def __init__(self, sign=None, nums=None, msg='wrong sign for alphabet'):
        if not sign == None and not nums == None:
            msg = msg + f' ({str(sign)} not member of {str(nums)}-numerical system)'
        super().__init__(msg)