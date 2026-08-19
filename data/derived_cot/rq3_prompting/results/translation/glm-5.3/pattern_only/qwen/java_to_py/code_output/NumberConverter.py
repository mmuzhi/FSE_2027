import re


class NumberConverter:

    _INT_MIN = -(1 << 31)
    _INT_MAX = (1 << 31) - 1

    @staticmethod
    def decimalToBinary(decimalNum):
        # Integer.toBinaryString treats the int as unsigned 32-bit.
        return format(decimalNum & 0xFFFFFFFF, 'b')

    @staticmethod
    def binaryToDecimal(binaryNum):
        return NumberConverter._parseInt(binaryNum, r'[+-]?[01]+', 2)

    @staticmethod
    def decimalToOctal(decimalNum):
        # Integer.toOctalString treats the int as unsigned 32-bit.
        return format(decimalNum & 0xFFFFFFFF, 'o')

    @staticmethod
    def octalToDecimal(octalNum):
        return NumberConverter._parseInt(octalNum, r'[+-]?[0-7]+', 8)

    @staticmethod
    def decimalToHex(decimalNum):
        # Integer.toHexString treats the int as unsigned 32-bit, lowercase.
        return format(decimalNum & 0xFFFFFFFF, 'x')

    @staticmethod
    def hexToDecimal(hexNum):
        return NumberConverter._parseInt(hexNum, r'[+-]?[0-9a-fA-F]+', 16)

    @staticmethod
    def _parseInt(s, pattern, radix):
        # Mirror Integer.parseInt(s, radix): optional sign, valid digits only,
        # no underscores/whitespace, and result must fit a signed 32-bit int.
        if not isinstance(s, str) or re.fullmatch(pattern, s) is None:
            raise ValueError(f'For input string: "{s}"')
        value = int(s, radix)
        if not (NumberConverter._INT_MIN <= value <= NumberConverter._INT_MAX):
            raise ValueError(f'For input string: "{s}"')
        return value