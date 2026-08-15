class NumberFormatException(ValueError):
    pass


class NumberConverter:
    @staticmethod
    def decimalToBinary(decimalNum):
        return bin(decimalNum & 0xffffffff)[2:]

    @staticmethod
    def binaryToDecimal(binaryNum):
        return NumberConverter._parseInt(binaryNum, 2)

    @staticmethod
    def decimalToOctal(decimalNum):
        return oct(decimalNum & 0xffffffff)[2:]

    @staticmethod
    def octalToDecimal(octalNum):
        return NumberConverter._parseInt(octalNum, 8)

    @staticmethod
    def decimalToHex(decimalNum):
        return hex(decimalNum & 0xffffffff)[2:]

    @staticmethod
    def hexToDecimal(hexNum):
        return NumberConverter._parseInt(hexNum, 16)

    @staticmethod
    def _parseInt(s, radix):
        if s is None:
            raise NumberFormatException("null")
        if s != s.strip():
            raise NumberFormatException('For input string: "' + s + '"')
        if len(s) == 0:
            raise NumberFormatException('For input string: "' + s + '"')

        sign = 1
        index = 0
        if s[0] == '-':
            sign = -1
            index = 1
        elif s[0] == '+':
            index = 1

        if index >= len(s):
            raise NumberFormatException('For input string: "' + s + '"')

        digits = s[index:]

        # Reject Python int() prefixes that Java's parseInt does not accept.
        if radix == 16 and (digits.startswith('0x') or digits.startswith('0X')):
            raise NumberFormatException('For input string: "' + s + '"')
        if radix == 2 and (digits.startswith('0b') or digits.startswith('0B')):
            raise NumberFormatException('For input string: "' + s + '"')
        if radix == 8 and (digits.startswith('0o') or digits.startswith('0O')):
            raise NumberFormatException('For input string: "' + s + '"')

        try:
            value = int(digits, radix)
        except ValueError:
            raise NumberFormatException('For input string: "' + s + '"')

        if sign == -1:
            value = -value

        if value > 2147483647 or value < -2147483648:
            raise NumberFormatException('For input string: "' + s + '"')

        return value