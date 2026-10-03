import re

class BinaryInfo:
    def __init__(self, zeroes: float, ones: float, bit_length: int):
        self._zeroes = zeroes
        self._ones = ones
        self._bit_length = bit_length

    def get_zeroes(self):
        return self._zeroes

    def get_ones(self):
        return self._ones

    def get_bit_length(self):
        return self._bit_length

    def __str__(self):
        return f"{{Zeroes: {self._zeroes:.3f}, Ones: {self._ones:.3f}, Bit length: {self._bit_length}}}"


class BinaryDataProcessor:
    def __init__(self, binary_string: str):
        self._binary_string = binary_string
        self._clean_non_binary_chars()

    def _clean_non_binary_chars(self):
        self._binary_string = re.sub(r'[^01]', '', self._binary_string)

    def calculate_binary_info(self):
        total_length = len(self._binary_string)
        zeroes_count = self._binary_string.count('0')
        ones_count = self._binary_string.count('1')
        zeroes_percentage = zeroes_count / total_length
        ones_percentage = ones_count / total_length
        return BinaryInfo(zeroes_percentage, ones_percentage, total_length)

    def _convert_to_text(self):
        result = []
        length = len(self._binary_string)
        for i in range(0, length, 8):
            if i + 8 > length:
                raise IndexError("String index out of range: binary string length is not a multiple of 8")
            byte_str = self._binary_string[i:i+8]
            decimal = int(byte_str, 2)
            result.append(chr(decimal))
        return ''.join(result)

    def convert_to_ascii(self):
        return self._convert_to_text()

    def convert_to_utf8(self):
        return self._convert_to_text()

    def get_binary_string(self):
        return self._binary_string


if __name__ == "__main__":
    bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
    print(bdp.get_binary_string())
    print(bdp.calculate_binary_info())
    print(bdp.convert_to_ascii())
    print(bdp.convert_to_utf8())