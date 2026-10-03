class BinaryDataProcessor:
    def __init__(self, binary_string: str):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        self.binary_string = ''.join(ch for ch in self.binary_string if ch in ('0', '1'))

    def calculate_binary_info(self):
        zeroes_count = self.binary_string.count('0')
        ones_count = len(self.binary_string) - zeroes_count
        total_length = len(self.binary_string)
        if total_length == 0:
            import math
            zeroes_percentage = math.nan
            ones_percentage = math.nan
        else:
            zeroes_percentage = zeroes_count / total_length
            ones_percentage = ones_count / total_length
        return {
            "Zeroes": zeroes_percentage,
            "Ones": ones_percentage,
            "Bit length": float(total_length)
        }

    def convert_to_ascii(self):
        result = []
        for i in range(0, len(self.binary_string), 8):
            chunk = self.binary_string[i:i+8]
            if len(chunk) < 8:
                chunk = chunk.zfill(8)
            value = int(chunk, 2)
            result.append(chr(value))
        return ''.join(result)

    def convert_to_utf8(self):
        return self.convert_to_ascii()