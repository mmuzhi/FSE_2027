class NumericEntityUnescaper:

    def replace(self, string):
        out = []
        pos = 0
        length = len(string)
        while pos < length - 2:
            if string[pos] == '&' and string[pos + 1] == '#':
                start = pos + 2
                is_hex = False
                if start == length:
                    return ''.join(out)
                first_char = string[start]
                if first_char == 'x' or first_char == 'X':
                    start += 1
                    is_hex = True
                    if start == length:
                        return ''.join(out)
                end = start
                while end < length and self.isHexChar(string[end]):
                    end += 1
                if end < length and string[end] == ';':
                    try:
                        entity_value = int(string[start:end], 16 if is_hex else 10)
                        out.append(chr(entity_value))
                        pos = end + 1
                        continue
                    except ValueError:
                        return ''.join(out)
            out.append(string[pos])
            pos += 1
        return ''.join(out)

    @staticmethod
    def isHexChar(c):
        return c.isdigit() or ('a' <= c.lower() <= 'f')