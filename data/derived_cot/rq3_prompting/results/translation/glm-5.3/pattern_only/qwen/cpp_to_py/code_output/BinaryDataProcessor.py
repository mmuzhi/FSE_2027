import math


class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        self.binary_string = ''.join(c for c in self.binary_string if c == '0' or c == '1')

    def calculate_binary_info(self):
        zeroes_count = self.binary_string.count('0')
        ones_count = len(self.binary_string) - zeroes_count
        total_length = len(self.binary_string)

        if total_length:
            zeroes_percentage = zeroes_count / total_length
            ones_percentage = ones_count / total_length
        else:
            # C++ produces NaN (0.0/0) for an empty string; mirror that
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
            # std::bitset<8> treats the first char as the MSB and zero-fills
            # the low bits for short chunks: left-align the chunk.
            value = int(chunk, 2) << (8 - len(chunk))
            parts.append(chr(value))
        return ''.join(parts)

    def convert_to_utf8(self):
        return self.convert_to_ascii()