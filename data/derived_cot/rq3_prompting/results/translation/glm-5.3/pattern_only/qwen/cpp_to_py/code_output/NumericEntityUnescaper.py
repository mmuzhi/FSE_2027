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
                    return "".join(out)

                end = start
                while end < length and NumericEntityUnescaper.is_hex_char(input[end]):
                    end += 1

                if end < length and input[end] == ';':
                    try:
                        number_str = input[start:end]
                        entity_value = NumericEntityUnescaper._parse_int_stream(number_str, is_hex)
                        if entity_value is None:
                            # ss.fail() -> abort with accumulated output
                            return "".join(out)
                        # static_cast<char>(value): truncate to low 8 bits
                        out.append(chr(entity_value & 0xFF))
                        pos = end + 1
                        continue
                    except Exception:
                        return "".join(out)

            out.append(input[pos])
            pos += 1

        return "".join(out)

    @staticmethod
    def is_hex_char(c):
        # ASCII-exact equivalent of std::isdigit || (tolower in 'a'..'f')
        return ('0' <= c <= '9') or ('a' <= c <= 'f') or ('A' <= c <= 'F')

    @staticmethod
    def _parse_int_stream(number_str, is_hex):
        # Mimics `std::stringstream >> int` (with std::hex when is_hex):
        # greedy prefix extraction; failure only when nothing was extracted,
        # or when the value overflows a 32-bit int (failbit since C++11).
        valid = "0123456789abcdefABCDEF" if is_hex else "0123456789"
        i = 0
        while i < len(number_str) and number_str[i] in valid:
            i += 1
        if i == 0:
            return None  # extraction failed -> ss.fail()
        base = 16 if is_hex else 10
        value = int(number_str[:i], base)
        if value > 2147483647:  # int overflow -> failbit
            return None
        return value