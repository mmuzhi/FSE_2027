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
                        entity_value = int(string[start:end], 16 if is_hex else 10)
                    except ValueError:
                        return ''.join(out)
                    # Java Integer.parseInt throws NumberFormatException on int overflow
                    if entity_value > 2147483647:
                        return ''.join(out)
                    # Java (char) cast truncates to the low 16 bits
                    out.append(chr(entity_value & 0xFFFF))
                    pos = end + 1
                    continue

            out.append(string[pos])
            pos += 1

        return ''.join(out)

    @staticmethod
    def is_hex_char(c):
        # Character.isDigit == Nd category -> str.isdecimal (NOT str.isdigit,
        # which also matches superscripts); lowercase mapping into 'a'..'f'
        # only occurs for ASCII 'A'-'F'/'a'-'f' in both languages.
        return c.isdecimal() or ('a' <= c.lower() <= 'f')