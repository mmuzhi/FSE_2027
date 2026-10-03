class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        # Remove any character that is not '0' or '1'
        self.binary_string = ''.join(filter(lambda c: c == '0' or c == '1', self.binary_string))

    def calculate_binary_info(self):
        total_length = len(self.binary_string)
        zeroes_count = self.binary_string.count('0')
        ones_count = total_length - zeroes_count

        zeroes_percentage = zeroes_count / total_length
        ones_percentage = ones_count / total_length

        return {
            "Zeroes": zeroes_percentage,
            "Ones": ones_percentage,
            "Bit length": total_length
        }

    def convert_to_ascii(self):
        # Convert the binary string to ASCII by processing 8 bits at a time
        # Note: This might not match the C++ behavior for bytes above 127 if the system's char is signed.
        output_chars = []
        for i in range(0, len(self.binary_string), 8):
            # Take up to 8 bits
            byte_str = self.binary_string[i:i+8]
            if len(byte_str) < 8:
                # Pad with zeros if necessary? The C++ code doesn't pad, but the input is cleaned and might be shorter.
                # But the C++ code uses substr(i,8) which might go beyond the string. It uses substr(i,8) and if the string is shorter, it will have fewer than 8 bits.
                # We'll just use what's there.
                pass
            # Convert the 8-bit binary string to an integer
            byte_value = int(byte_str, 2) if byte_str else 0
            # Convert to character using chr
            output_chars.append(chr(byte_value))
        return ''.join(output_chars)

    def convert_to_utf8(self):
        return self.convert_to_ascii()