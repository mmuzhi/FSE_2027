class NumericEntityUnescaper:

    def replace(self, input):
        out = []
        pos = 0
        length = len(input)
        if length == 0:
            return ""
        while pos < length - 2:
            if input[pos] == '&' and input[pos + 1] == '#':
                start = pos + 2
                is_hex = False

                if start < length and input[start] in ('x', 'X'):
                    start += 1
                    is_hex = True

                if start == length:
                    return ''.join(out)

                end = start
                while end < length and NumericEntityUnescaper.is_hex_char(input[end]):
                    end += 1

                if end < length and input[end] == ';':
                    number_str = input[start:end]
                    try:
                        entity_value = int(number_str, 16) if is_hex else int(number_str)
                    except ValueError:
                        return ''.join(out)
                    if entity_value > 0x7FFFFFFF:
                        # mirrors std::stringstream failbit on int overflow
                        return ''.join(out)
                    out.append(chr(entity_value & 0xFF))  # static_cast<char> truncation
                    pos = end + 1
                    continue

            out.append(input[pos])
            pos += 1

        return ''.join(out)

    @staticmethod
    def is_hex_char(c):
        return ('0' <= c <= '9') or ('a' <= c.lower() <= 'f')