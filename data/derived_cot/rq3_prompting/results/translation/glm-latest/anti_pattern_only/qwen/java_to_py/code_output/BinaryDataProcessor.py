import math
import re


class BinaryInfo:
    def __init__(self, zeroes: float, ones: float, bit_length: int):
        self._zeroes = zeroes
        self._ones = ones
        self._bit_length = bit_length

    @property
    def zeroes(self) -> float:
        return self._zeroes

    @property
    def ones(self) -> float:
        return self._ones

    @property
    def bit_length(self) -> int:
        return self._bit_length

    def __str__(self) -> str:
        return "{Zeroes: %s, Ones: %s, Bit length: %d}" % (
            self._format_double(self._zeroes),
            self._format_double(self._ones),
            self._bit_length,
        )

    __repr__ = __str__

    @staticmethod
    def _format_double(value: float) -> str:
        # Java's String.format("%.3f", NaN) renders as "NaN"; Python's as "nan".
        if math.isnan(value):
            return "NaN"
        return "%.3f" % value


class BinaryDataProcessor:
    def __init__(self, binary_string: str):
        self._binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self) -> None:
        self._binary_string = re.sub("[^01]", "", self._binary_string)

    def calculate_binary_info(self) -> BinaryInfo:
        total_length = len(self._binary_string)
        zeroes_count = self._binary_string.count("0")
        ones_count = self._binary_string.count("1")

        if total_length:
            zeroes_percentage = zeroes_count / total_length
            ones_percentage = ones_count / total_length
        else:
            # Java evaluates (double) 0 / 0 as NaN rather than raising.
            zeroes_percentage = float("nan")
            ones_percentage = float("nan")

        return BinaryInfo(zeroes_percentage, ones_percentage, total_length)

    def convert_to_ascii(self) -> str:
        chars = []
        binary_string = self._binary_string
        for i in range(0, len(binary_string), 8):
            if i + 8 > len(binary_string):
                # Java's substring(i, i + 8) throws StringIndexOutOfBoundsException
                # when the remaining bits do not form a full byte.
                raise IndexError(
                    "begin %d, end %d, length %d" % (i, i + 8, len(binary_string))
                )
            byte_string = binary_string[i:i + 8]
            decimal = int(byte_string, 2)
            chars.append(chr(decimal))
        return "".join(chars)

    def convert_to_utf8(self) -> str:
        chars = []
        binary_string = self._binary_string
        for i in range(0, len(binary_string), 8):
            if i + 8 > len(binary_string):
                raise IndexError(
                    "begin %d, end %d, length %d" % (i, i + 8, len(binary_string))
                )
            byte_string = binary_string[i:i + 8]
            decimal = int(byte_string, 2)
            chars.append(chr(decimal))
        return "".join(chars)

    def get_binary_string(self) -> str:
        return self._binary_string


def main() -> None:
    bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
    print(bdp.get_binary_string())
    print(bdp.calculate_binary_info())
    print(bdp.convert_to_ascii())
    print(bdp.convert_to_utf8())


if __name__ == "__main__":
    main()