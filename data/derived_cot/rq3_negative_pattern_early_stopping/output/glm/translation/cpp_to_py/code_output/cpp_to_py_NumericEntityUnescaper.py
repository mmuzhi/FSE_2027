class NumericEntityUnescaper:
    def replace(self, input_str):
        out = []
        pos = 0
        length = len(input_str)
        if not input_str:
            return ""
        while pos < length - 2:
            if input_str[pos] == '&' and input_str[pos + 1] == '#':
                start = pos + 2
                is_hex = False
                if start < length and (input_str[start] == 'x' or input_str[start] == 'X'):
                    start += 1
                    is_hex = True
                if start == length:
                    return "".join(out)
                end = start
                while end < length and NumericEntityUnescaper.is_hex_char(input_str[end]):
                    end += 1
                if end < length and input_str[end] == ';':
                    try:
                        number_str = input_str[start:end]
                        if is_hex:
                            entity_value = int(number_str, 16)
                        else:
                            entity_value = int(number_str)
                        out.append(chr(entity_value))
                        pos = end + 1
                        continue
                    except (ValueError, OverflowError):
                        return "".join(out)
            out.append(input_str[pos])
            pos += 1
        return "".join(out)

    @staticmethod
    def is_hex_char(c):
        return c.isdigit() or (c.lower() >= 'a' and c.lower() <= 'f')