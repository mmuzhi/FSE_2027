class NumberConverter:
    _DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'
    _SPACES = ' \t\n\v\f\r'  # C-locale whitespace skipped by std::stoi

    @staticmethod
    def decimal_to_binary(decimal_num):
        # std::bitset<32>(n).to_string() == 32-bit two's complement view
        binary_num = format(decimal_num & 0xFFFFFFFF, '032b').lstrip('0')
        return binary_num if binary_num else "0"

    @staticmethod
    def binary_to_decimal(binary_num):
        return NumberConverter._stoi(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num):
        # std::oct prints '-' + magnitude, no prefix; format(n, 'o') matches
        return format(decimal_num, 'o')

    @staticmethod
    def octal_to_decimal(octal_num):
        return NumberConverter._stoi(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num):
        # std::hex prints lowercase, no "0x" prefix; format(n, 'x') matches
        return format(decimal_num, 'x')

    @staticmethod
    def hex_to_decimal(hex_num):
        return NumberConverter._stoi(hex_num, 16)

    @staticmethod
    def _stoi(s, base):
        # Mimics std::stoi(str, nullptr, base):
        # skip leading whitespace, optional sign, optional 0x/0X prefix when
        # base == 16 (strtol semantics), parse longest valid prefix,
        # throw on no digits, and range-check against 32-bit int.
        i, n = 0, len(s)
        while i < n and s[i] in NumberConverter._SPACES:
            i += 1
        sign = 1
        if i < n and s[i] in '+-':
            if s[i] == '-':
                sign = -1
            i += 1
        if (base == 16 and i + 1 < n and s[i] == '0'
                and s[i + 1] in 'xX'
                and i + 2 < n and s[i + 2].lower() in NumberConverter._DIGITS[:16]):
            i += 2  # consume "0x"/"0X" only if a hex digit follows
        digits = NumberConverter._DIGITS[:base]
        value, start = 0, i
        while i < n and s[i].lower() in digits:
            value = value * base + digits.index(s[i].lower())
            i += 1
        if i == start:
            raise ValueError("stoi: no conversion")  # std::invalid_argument
        result = sign * value
        if result < -2147483648 or result > 2147483647:
            raise OverflowError("stoi: out of range")  # std::out_of_range
        return result