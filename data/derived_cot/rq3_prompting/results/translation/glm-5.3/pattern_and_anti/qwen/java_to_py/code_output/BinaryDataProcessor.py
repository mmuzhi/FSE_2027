from decimal import Decimal, ROUND_HALF_UP


class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        import re
        self.binary_string = re.sub("[^01]", "", self.binary_string)

    def calculate_binary_info(self):
        zeroes_count = self.binary_string.count("0")
        ones_count = self.binary_string.count("1")
        total_length = len(self.binary_string)

        # Java (double)/int yields NaN on 0/0; Python would raise ZeroDivisionError.
        if total_length == 0:
            zeroes_percentage = float("nan")
            ones_percentage = float("nan")
        else:
            zeroes_percentage = zeroes_count / total_length
            ones_percentage = ones_count / total_length

        return BinaryInfo(zeroes_percentage, ones_percentage, total_length)

    def convert_to_ascii(self):
        ascii_string = []
        for i in range(0, len(self.binary_string), 8):
            # Java substring(i, i+8) throws StringIndexOutOfBoundsException
            # when fewer than 8 chars remain; mirror that instead of slicing short.
            if i + 8 > len(self.binary_string):
                raise IndexError(
                    f"begin {i}, end {i + 8}, length {len(self.binary_string)}"
                )
            byte_string = self.binary_string[i : i + 8]
            decimal = int(byte_string, 2)
            ascii_string.append(chr(decimal))
        return "".join(ascii_string)

    def convert_to_utf8(self):
        utf8_string = []
        for i in range(0, len(self.binary_string), 8):
            if i + 8 > len(self.binary_string):
                raise IndexError(
                    f"begin {i}, end {i + 8}, length {len(self.binary_string)}"
                )
            byte_string = self.binary_string[i : i + 8]
            decimal = int(byte_string, 2)
            utf8_string.append(chr(decimal))
        return "".join(utf8_string)

    def get_binary_string(self):
        return self.binary_string


class BinaryInfo:
    def __init__(self, zeroes, ones, bit_length):
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
        return (
            f"{{Zeroes: {self._fmt(self._zeroes)}, "
            f"Ones: {self._fmt(self._ones)}, "
            f"Bit length: {self._bit_length}}}"
        )

    @staticmethod
    def _fmt(x):
        # Java's %.3f prints NaN as "NaN" and rounds HALF_UP on the exact double.
        if x != x:
            return "NaN"
        d = Decimal(x).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
        return format(d, "f")


if __name__ == "__main__":
    bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
    print(bdp.get_binary_string())
    print(bdp.calculate_binary_info())
    print(bdp.convert_to_ascii())
    print(bdp.convert_to_utf8())