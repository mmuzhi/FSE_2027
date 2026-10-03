class NumberConverter:
    @staticmethod
    def decimal_to_binary(decimal_num):
        # Handle negative numbers by converting to two's complement 32-bit representation
        if decimal_num < 0:
            # Use bitwise AND with 0xFFFFFFFF to get the two's complement representation
            n_unsigned = decimal_num & 0xFFFFFFFF
            s = bin(n_unsigned)[2:]
        else:
            s = bin(decimal_num)[2:]
        # Remove leading zeros, but if the string is empty then return "0"
        if s == '':
            return "0"
        return s

    @staticmethod
    def binary_to_decimal(binary_num):
        # The input binary_num is a string of 0s and 1s (without any sign)
        return int(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num):
        return oct(decimal_num)[2:]

    @staticmethod
    def octal_to_decimal(octal_num):
        return int(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num):
        return hex(decimal_num)[2:]

    @staticmethod
    def hex_to_decimal(hex_num):
        return int(hex_num, 16)