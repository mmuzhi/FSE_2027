class NumberConverter:
    @staticmethod
    def decimal_to_binary(decimal_num: int) -> str:
        if decimal_num >= 0:
            binary = bin(decimal_num)[2:]
            return binary if binary else "0"
        else:
            val = (1 << 32) + decimal_num
            binary = bin(val)[2:]
            return binary.zfill(32)

    @staticmethod
    def binary_to_decimal(binary_num: str) -> int:
        return int(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num: int) -> str:
        return oct(decimal_num)[2:] if decimal_num >= 0 else oct(decimal_num)[2:]  # oct for negative gives '-0o...' so handle
        if decimal_num >= 0:
            return oct(decimal_num)[2:]
        else:
            val = (1 << 32) + decimal_num
            return oct(val)[2:]

    @staticmethod
    def octal_to_decimal(octal_num: str) -> int:
        return int(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num: int) -> str:
        if decimal_num >= 0:
            return hex(decimal_num)[2:]
        else:
            val = (1 << 32) + decimal_num
            return hex(val)[2:]

    @staticmethod
    def hex_to_decimal(hex_num: str) -> int:
        return int(hex_num, 16)