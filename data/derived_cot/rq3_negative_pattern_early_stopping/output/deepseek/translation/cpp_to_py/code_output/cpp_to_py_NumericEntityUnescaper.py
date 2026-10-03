class NumericEntityUnescaper:
    @staticmethod
    def is_hex_char(c: str) -> bool:
        return ('0' <= c <= '9') or ('a' <= c.lower() <= 'f')

    def replace(self, input_str: str) -> str:
        out = []
        length = len(input_str)
        pos = 0
        if length == 0:
            return ""
        while pos < length - 2:
            if input_str[pos] == '&' and input_str[pos + 1] == '#':
                start = pos + 2
                is_hex = False
                if start < length and (input_str[start] == 'x' or input_str[start] == 'X'):
                    start += 1
                    is_hex = True
                if start == length:
                    return ''.join(out)
                end = start
                while end < length and self.is_hex_char(input_str[end]):
                    end += 1
                if end < length and input_str[end] == ';':
                    number_str = input_str[start:end]
                    try:
                        if is_hex:
                            entity_value = int(number_str, 16)
                        else:
                            entity_value = int(number_str, 10)
                    except ValueError:
                        return ''.join(out)
                    out.append(chr(entity_value & 0xFF))
                    pos = end + 1
                    continue
            out.append(input_str[pos])
            pos += 1
        return ''.join(out)