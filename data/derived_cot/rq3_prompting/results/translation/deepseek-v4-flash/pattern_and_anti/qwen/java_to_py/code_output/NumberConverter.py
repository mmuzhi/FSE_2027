class NumberFormatException(ValueError):
    pass


class NumberConverter:
    @staticmethod
    def _digit(ch, radix):
        try:
            return int(ch, radix)
        except ValueError:
            return -1

    @staticmethod
    def _parse_int(s, radix):
        if s is None:
            raise NumberFormatException("null")
        if radix < 2 or radix > 36:
            raise NumberFormatException("radix " + str(radix) + " out of range")

        result = 0
        negative = False
        i = 0
        length = len(s)

        if length > 0:
            first_char = s[0]
            if first_char < '0':
                if first_char == '-':
                    negative = True
                    limit = -2147483648
                elif first_char != '+':
                    raise NumberFormatException('For input string: "' + s + '"')
                else:
                    limit = -2147483647

                if length == 1:
                    raise NumberFormatException('For input string: "' + s + '"')
                i += 1
            else:
                limit = -2147483647

            multmin = -((-limit) // radix)

            while i < length:
                digit = NumberConverter._digit(s[i], radix)
                if digit < 0:
                    raise NumberFormatException('For input string: "' + s + '"')
                if result < multmin:
                    raise NumberFormatException('For input string: "' + s + '"')
                result *= radix
                if result < limit + digit:
                    raise NumberFormatException('For input string: "' + s + '"')
                result -= digit
                i += 1
        else:
            raise NumberFormatException('For input string: "' + s + '"')

        return -result if negative else result

    @staticmethod
    def decimalToBinary(decimalNum):
        if decimalNum < 0:
            return bin(decimalNum & 0xFFFFFFFF)[2:]
        return bin(decimalNum)[2:]

    @staticmethod
    def binaryToDecimal(binaryNum):
        return NumberConverter._parse_int(binaryNum, 2)

    @staticmethod
    def decimalToOctal(decimalNum):
        if decimalNum < 0:
            return oct(decimalNum & 0xFFFFFFFF)[2:]
        return oct(decimalNum)[2:]

    @staticmethod
    def octalToDecimal(octalNum):
        return NumberConverter._parse_int(octalNum, 8)

    @staticmethod
    def decimalToHex(decimalNum):
        if decimalNum < 0:
            return hex(decimalNum & 0xFFFFFFFF)[2:]
        return hex(decimalNum)[2:]

    @staticmethod
    def hexToDecimal(hexNum):
        return NumberConverter._parse_int(hexNum, 16)