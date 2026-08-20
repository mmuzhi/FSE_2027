class BinaryDataProcessor:
    def __init__(self, binary_string: str):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self) -> None:
        # Equivalent of erase(remove_if(...)): keep only '0' and '1'.
        self.binary_string = ''.join(c for c in self.binary_string if c in '01')

    def calculate_binary_info(self):
        zeroes_count = self.binary_string.count('0')
        ones_count = len(self.binary_string) - zeroes_count
        total_length = len(self.binary_string)

        if total_length != 0:
            zeroes_percentage = zeroes_count / total_length
            ones_percentage = ones_count / total_length
        else:
            # C++ evaluates 0.0 / 0 here, which yields NaN (IEEE 754),
            # so mirror that instead of raising ZeroDivisionError.
            zeroes_percentage = float('nan')
            ones_percentage = float('nan')

        return {
            'Zeroes': zeroes_percentage,
            'Ones': ones_percentage,
            'Bit length': float(total_length),
        }

    def convert_to_ascii(self) -> str:
        pieces = []
        for i in range(0, len(self.binary_string), 8):
            chunk = self.binary_string[i:i + 8]
            # For a chunk of length <= 8 consisting of '0'/'1',
            # std::bitset<8>(chunk).to_ulong() == int(chunk, 2)
            # (the last character is the least significant bit,
            # and shorter chunks behave like left-padded values).
            pieces.append(chr(int(chunk, 2)))
        return ''.join(pieces)

    def convert_to_utf8(self) -> str:
        return self.convert_to_ascii()