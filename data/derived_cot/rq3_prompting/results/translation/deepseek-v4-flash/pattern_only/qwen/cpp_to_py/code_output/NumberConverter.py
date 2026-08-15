def _is_digit(ch, base):
    if base == 2:
        return ch == '0' or ch == '1'
    if base == 8:
        return '0' <= ch <= '7'
    if base == 16:
        return ch in '0123456789abcdefABCDEF'
    return False


def _digit_value(ch):
    if '0' <= ch <= '9':
        return ord(ch) - ord('0')
    if 'a' <= ch <= 'f':
        return ord(ch) - ord('a') + 10
    if 'A' <= ch <= 'F':
        return ord(ch) - ord('A') + 10
    raise ValueError("invalid digit")


def _stoi(s, base):
    i = 0
    n = len(s)

    while i < n and s[i] in ' \t\n\v\f\r':
        i += 1

    if i >= n:
        raise ValueError("invalid_argument")

    sign = 1
    if s[i] == '+':
        i += 1
    elif s[i] == '-':
        sign = -1
        i += 1

    if base == 16 and i + 1 < n and s[i] == '0' and s[i + 1] in 'xX':
        if i + 2 < n and _is_digit(s[i + 2], 16):
            i += 2

    digits_start = i
    while i < n and _is_digit(s[i], base):
        i += 1

    if i == digits_start:
        raise ValueError("invalid_argument")

    digit_str = s[digits_start:i]
    value = 0
    for ch in digit_str:
        value = value * base + _digit_value(ch)

    value *= sign

    if value < -2147483648 or value > 2147483647:
        raise OverflowError("out_of_range")

    return value


class NumberConverter:
    @staticmethod
    def decimal_to_binary(decimal_num):
        binary_num = format(decimal_num & 0xFFFFFFFF, '032b').lstrip('0')
        return binary_num if binary_num else "0"

    @staticmethod
    def binary_to_decimal(binary_num):
        return _stoi(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num):
        return format(decimal_num, 'o')

    @staticmethod
    def octal_to_decimal(octal_num):
        return _stoi(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num):
        return format(decimal_num, 'x')

    @staticmethod
    def hex_to_decimal(hex_num):
        return _stoi(hex_num, 16)