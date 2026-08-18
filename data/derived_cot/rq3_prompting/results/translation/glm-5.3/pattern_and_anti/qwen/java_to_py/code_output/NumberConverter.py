import re


class NumberConverter:

    _DIGITS = {2: '01', 8: '01234567', 16: '0123456789abcdefABCDEF'}
    _INT_MIN = -2 ** 31
    _INT_MAX = 2 ** 31 - 1

    @staticmethod
    def _parse_int(s, base):
        # Mirror Integer.parseInt: optional single sign, then only valid digits
        # (no whitespace, underscores, or "0x"/"0b" prefixes), result must fit
        # in a signed 32-bit int.
        digits = NumberConverter._DIGITS[base]
        if not re.fullmatch(r'[+-]?[' + digits + r']+', s):
            raise ValueError('For input string: "' + str(s) + '"')
        value = int(s, base)
        if value < NumberConverter._INT_MIN or value > NumberConverter._INT_MAX:
            raise ValueError('For input string: "' + s + '"')
        return value

    @staticmethod
    def decimal_to_binary(decimal_num):
        # Java's toBinaryString treats the int as unsigned 32-bit (no prefix,
        # no leading zeros); masking reproduces that for negatives.
        return format(decimal_num & 0xFFFFFFFF, 'b')

    @staticmethod
    def binary_to_decimal(binary_num):
        return NumberConverter._parse_int(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num):
        return format(decimal_num & 0xFFFFFFFF, 'o')

    @staticmethod
    def octal_to_decimal(octal_num):
        return NumberConverter._parse_int(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num):
        return format(decimal_num & 0xFFFFFFFF, 'x')

    @staticmethod
    def hex_to_decimal(hex_num):
        return NumberConverter._parse_int(hex_num, 16)