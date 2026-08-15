class NumberConverter:
    @staticmethod
    def _stoi(s, base):
        # Mimic std::stoi(s, nullptr, base): parse a prefix, allow leading
        # whitespace and an optional sign, then consume valid base digits.
        i = 0
        n = len(s)

        # ASCII whitespace only, matching the C locale used by std::isspace.
        while i < n and s[i] in ' \t\n\v\f\r':
            i += 1

        sign = 1
        if i < n and (s[i] == '+' or s[i] == '-'):
            if s[i] == '-':
                sign = -1
            i += 1

        if base == 2:
            valid = set('01')
        elif base == 8:
            valid = set('01234567')
        elif base == 16:
            valid = set('0123456789abcdefABCDEF')
        else:
            raise ValueError("unsupported base")

        start = i
        while i < n and s[i] in valid:
            i += 1

        if i == start:
            raise ValueError(f"invalid literal for int() with base {base}: {s!r}")

        value = int(s[start:i], base) * sign

        # std::stoi returns int; assume 32-bit signed int range.
        if value < -2147483648 or value > 2147483647:
            raise OverflowError("int out of range")

        return value

    @staticmethod
    def decimal_to_binary(decimal_num):
        if decimal_num >= 0:
            return "0" if decimal_num == 0 else bin(decimal_num)[2:]
        # 32-bit two's complement, matching std::bitset<32>(decimal_num)
        return format((1 << 32) + decimal_num, '032b')

    @staticmethod
    def binary_to_decimal(binary_num):
        return NumberConverter._stoi(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num):
        return format(decimal_num, 'o')

    @staticmethod
    def octal_to_decimal(octal_num):
        return NumberConverter._stoi(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num):
        return format(decimal_num, 'x')

    @staticmethod
    def hex_to_decimal(hex_num):
        return NumberConverter._stoi(hex_num, 16)