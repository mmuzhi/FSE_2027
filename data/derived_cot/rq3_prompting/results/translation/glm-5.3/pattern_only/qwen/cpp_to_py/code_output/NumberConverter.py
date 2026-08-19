class NumberConverter:
    @staticmethod
    def decimal_to_binary(decimal_num: int) -> str:
        # std::bitset<32>(...).to_string(): 32-bit two's complement representation
        binary_num = format(decimal_num & 0xFFFFFFFF, '032b')
        stripped = binary_num.lstrip('0')
        return stripped if stripped else "0"

    @staticmethod
    def binary_to_decimal(binary_num: str) -> int:
        return NumberConverter._stoi(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num: int) -> str:
        # std::oct on a negative value prints the unsigned bit pattern
        return format(decimal_num & 0xFFFFFFFF, 'o')

    @staticmethod
    def octal_to_decimal(octal_num: str) -> int:
        return NumberConverter._stoi(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num: int) -> str:
        # std::hex: lowercase, unsigned reinterpretation for negatives
        return format(decimal_num & 0xFFFFFFFF, 'x')

    @staticmethod
    def hex_to_decimal(hex_num: str) -> int:
        return NumberConverter._stoi(hex_num, 16)

    @staticmethod
    def _digit_val(c: str) -> int:
        if '0' <= c <= '9':
            return ord(c) - ord('0')
        if 'a' <= c <= 'z':
            return ord(c) - ord('a') + 10
        if 'A' <= c <= 'Z':
            return ord(c) - ord('A') + 10
        return -1

    @staticmethod
    def _stoi(s: str, base: int) -> int:
        # Emulates std::stoi(s, nullptr, base): skips leading whitespace,
        # optional sign, optional 0x/0X prefix only for base 16, parses valid
        # digits and stops at the first invalid character; raises ValueError
        # for no-conversion (invalid_argument) and out-of-range cases.
        i, n = 0, len(s)
        while i < n and s[i] in ' \t\n\v\f\r':
            i += 1
        neg = False
        if i < n and s[i] in '+-':
            neg = s[i] == '-'
            i += 1
        if (base == 16 and s[i:i + 2] in ('0x', '0X')
                and i + 2 < n and 0 <= NumberConverter._digit_val(s[i + 2]) < 16):
            i += 2
        start = i
        val = 0
        while i < n:
            d = NumberConverter._digit_val(s[i])
            if d < 0 or d >= base:
                break
            val = val * base + d
            i += 1
        if i == start:
            raise ValueError("stoi: no conversion")
        if neg:
            val = -val
        if not -0x80000000 <= val <= 0x7FFFFFFF:
            raise ValueError("stoi: result out of range")
        return val