from cfg import WrongSignForNumeralSystem
from numb import _numb, _nums
from interface import _interface_, _commander_

def conv_dec_to(dec, nums):
    if type(dec).__name__ == '_numb':
        return dec if nums == 10 else _nums._convert_from_dec(dec, nums)
    return _numb(dec=dec) if nums == 10 else _nums._convert_from_dec(_numb(dec=dec), nums)

def conv_to_dec(numb):
    return _nums._convert_to_dec(numb)

def get_numb(num, nums=10):
    num = str(num).upper()
    nums = int(nums)
    resp = _nums._num_is_valid_for_nums(num, nums)
    if resp == True:
        num = num.replace(',', '.').replace('+', '')
        frct = None
        if not '.' in num:
            num = num + '.'
            frct = ''
        else:
            frct=num.split('.')[1]
        return _numb(dec=None, pos=not '-' in num, intg=num.replace('-', '').split('.')[0], frct=frct, nums=int(nums))
    else:
        raise(WrongSignForNumeralSystem(resp, nums))

def conv_to(num, nums1, nums2):
    return conv_dec_to(conv_to_dec(get_numb(num, nums1)), nums2)

i = _interface_
i._offset(False)
i._input('+')
# print('-----------------')
i._print_signs()
# print(' =', _commander_._execute_interface_expression(_interface_))