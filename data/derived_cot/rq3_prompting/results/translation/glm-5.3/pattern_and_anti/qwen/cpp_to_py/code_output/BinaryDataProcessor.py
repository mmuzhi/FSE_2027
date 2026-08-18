import math


class BinaryDataProcessor:
    def __init__(self, binary_string: str):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        self.binary_string = ''.join(c for c in self.binary_string if c in ('0', '1'))

    def calculate_binary_info(self):
        zeroes_count = self.binary_string.count('0')
        ones_count = len(self.binary_string) - zeroes_count
        total_length = len(self.binary_string)

        # C++ double division yields NaN for 0/0; preserve that instead of raising
        if total_length:
            zeroes_percentage = zeroes_count / total_length
            ones_percentage = ones_count / total_length
        else:
            zeroes_percentage = math.nan
            ones_percentage = math.nan

        return {
            'Zeroes': zeroes_percentage,
            'Ones': ones_percentage,
            'Bit length': float(total_length)
        }

    def convert_to_ascii(self):
        parts = []
        for i in range(0, len(self.binary_string), 8):
            chunk = self.binary_string[i:i + 8]
            parts.append(chr(int(chunk, 2)))
        return ''.join(parts)

    def convert_to_utf8(self):
        return self.convert_to_ascii()