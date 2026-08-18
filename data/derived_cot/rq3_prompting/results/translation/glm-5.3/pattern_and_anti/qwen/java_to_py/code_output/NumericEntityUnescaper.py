import unicodedata


class NumericEntityUnescaper:

    def replace(self, string):
        out = []
        pos = 0
        length = len(string)

        while pos < length - 2:
            if string[pos] == '&' and string[pos + 1] == '#':
                start = pos + 2
                is_hex = False
                first_char = string[start]

                if first_char == 'x' or first_char == 'X':
                    start += 1
                    is_hex = True

                if start == length:
                    return ''.join(out)

                end = start
                while end < length and NumericEntityUnescaper.is_hex_char(string[end]):
                    end += 1

                if end < length and string[end] == ';':
                    try:
                        entity_value = self._parse_int(
                            string[start:end], 16 if is_hex else 10)
                        out.append(chr(entity_value & 0xFFFF))
                        pos = end + 1
                        continue
                    except ValueError:
                        return ''.join(out)
            out.append(string[pos])
            pos += 1

        return ''.join(out)

    @staticmethod
    def _parse_int(s, radix):
        # Mirrors Java's Integer.parseInt(s, radix): raises ValueError for
        # empty/invalid digit strings and for values overflowing a 32-bit int.
        value = int(s, radix)
        if value > 0x7FFFFFFF:
            raise ValueError('Value out of range for a 32-bit int')
        return value

    @staticmethod
    def is_hex_char(c):
        # Character.isDigit(c) == Unicode general category Nd
        return (unicodedata.category(c) == 'Nd'
                or 'a' <= c.lower() <= 'f')