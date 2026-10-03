class NumericEntityUnescaper:

    def replace(self, string):
        if not string:
            return string

        out_list = []
        pos = 0
        length = len(string)

        while pos < length - 2:
            if string[pos] == '&' and string[pos+1] == '#':
                start = pos + 2
                is_hex = False
                first_char = string[start]

                if first_char == 'x' or first_char == 'X':
                    start += 1
                    is_hex = True

                if start >= length:
                    # We've reached the end, so break out of the loop and return the built string.
                    break

                end = start
                while end < length and self.is_hex_char(string[end]):
                    end += 1

                if end < length and string[end] == ';':
                    try:
                        # Parse the substring from `start` to `end` (exclusive of `end`) as an integer.
                        entity_value = int(string[start:end], 16 if is_hex else 10)
                        out_list.append(chr(entity_value))
                        pos = end + 1  # Move the position past the semicolon
                        continue  # Skip the rest of the loop and go to the next iteration
                    except ValueError:
                        # If there's a parsing error, break out and return what we have.
                        break
                else:
                    # If we didn't find a semicolon, we just append the current character and continue.
                    out_list.append(string[pos])
                    pos += 1
                    continue

            # If we didn't find an entity, just append the current character and move on.
            out_list.append(string[pos])
            pos += 1

        return ''.join(out_list)

    @staticmethod
    def is_hex_char(c):
        # Check if the character is a hex digit (0-9, a-f, A-F)
        c_lower = c.lower()
        return c.isdigit() or ('a' <= c_lower <= 'f')