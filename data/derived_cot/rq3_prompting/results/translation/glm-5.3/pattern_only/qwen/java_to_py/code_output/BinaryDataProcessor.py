import math
import re
from decimal import Decimal, ROUND_HALF_UP


def _java_div(numerator, denominator):
    # Java double division: division by zero yields NaN/Infinity, never an exception.
    if denominator == 0:
        return float('nan') if numerator == 0 else float('inf')
    return numerator / denominator


def _java_f3(value):
    # Java String.format("%.3f", ...): NaN/Infinity spellings + HALF_UP rounding.
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "Infinity" if value > 0 else "-Infinity"
    return str(Decimal(value).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


class BinaryInfo:
    def __init__(self, zeroes, ones, bit_length):
        self.zeroes = zeroes
        self.ones = ones
        self.bit_length = bit_length

    def get_zeroes(self):
        return self.zeroes

    def get_ones(self):
        return self.ones

    def get_bit_length(self):
        return self.bit_length

    def __str__(self):
        return "{Zeroes: %s, Ones: %s, Bit length: %d}" % (
            _java_f3(self.zeroes), _java_f3(self.ones), self.bit_length)


class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        self.binary_string = re.sub(r"[^01]", "", self.binary_string)

    def calculate_binary_info(self):
        zeroes_count = len(self.binary_string) - len(self.binary_string.replace("0", ""))
        ones_count = len(self.binary_string) - len(self.binary_string.replace("1", ""))
        total_length = len(self.binary_string)

        zeroes_percentage = _java_div(zeroes_count, total_length)
        ones_percentage = _java_div(ones_count, total_length)

        return BinaryInfo(zeroes_percentage, ones_percentage, total_length)

    def _convert(self):
        parts = []
        s = self.binary_string
        for i in range(0, len(s), 8):
            if i + 8 > len(s):
                # Java substring(i, i + 8) throws StringIndexOutOfBoundsException on a partial chunk.
                raise IndexError("begin %d, end %d, length %d" % (i, i + 8, len(s)))
            parts.append(chr(int(s[i:i + 8], 2)))
        return "".join(parts)

    def convert_to_ascii(self):
        return self._convert()

    def convert_to_utf8(self):
        return self._convert()

    def get_binary_string(self):
        return self.binary_string


if __name__ == "__main__":
    bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
    print(bdp.get_binary_string())
    print(bdp.calculate_binary_info())
    print(bdp.convert_to_ascii())
    print(bdp.convert_to_utf8())