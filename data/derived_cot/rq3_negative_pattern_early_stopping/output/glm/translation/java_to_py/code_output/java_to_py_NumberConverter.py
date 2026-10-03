import re

class NumberConverter:

    @staticmethod
    def decimalToBinary(decimalNum):
        return format(decimalNum & 0xFFFFFFFF, 'b')

    @staticmethod
    def binaryToDecimal(binaryNum):
        try:
            if not re.fullmatch(r'[+-]?[01]+', binaryNum):
                raise ValueError(f"For input string: \"{binaryNum}\"")
        except TypeError:
            raise ValueError("For input string: \"null\"")
        val = int(binaryNum, 2)
        if val > 2147483647 or val < -2147483648:
            raise ValueError(f"For input string: \"{binaryNum}\"")
        return val

    @staticmethod
    def decimalToOctal(decimalNum):
        return format(decimalNum & 0xFFFFFFFF, 'o')

    @staticmethod
    def octalToDecimal(octalNum):
        try:
            if not re.fullmatch(r'[+-]?[0-7]+', octalNum):
                raise ValueError(f"For input string: \"{octalNum}\"")
        except TypeError:
            raise ValueError("For input string: \"null\"")
        val = int(octalNum, 8)
        if val > 2147483647 or val < -2147483648:
            raise ValueError(f"For input string: \"{octalNum}\"")
        return val

    @staticmethod
    def decimalToHex(decimalNum):
        return format(decimalNum & 0xFFFFFFFF, 'x')

    @staticmethod
    def hexToDecimal(hexNum):
        try:
            if not re.fullmatch(r'[+-]?[0-9a-fA-F]+', hexNum):
                raise ValueError(f"For input string: \"{hexNum}\"")
        except TypeError:
            raise ValueError("For input string: \"null\"")
        val = int(hexNum, 16)
        if val > 2147483647 or val < -2147483648:
            raise ValueError(f"For input string: \"{hexNum}\"")
        return val