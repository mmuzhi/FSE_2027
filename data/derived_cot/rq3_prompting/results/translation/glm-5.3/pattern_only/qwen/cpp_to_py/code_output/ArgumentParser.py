import re

# Classic-locale whitespace (exactly what istringstream's operator>> skips).
_WS = ' \t\n\v\f\r'
# Emulates std::stoi parsing: optional leading whitespace, optional sign, digits.
_STOI_RE = re.compile(r'[ \t\n\v\f\r]*([+-]?[0-9]+)')
_INT_MIN = -2147483648
_INT_MAX = 2147483647


class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}
        self.type_converters = {}
        self.initialize_converters()

    def parse_arguments(self, command_string):
        s = command_string
        n = len(s)

        # std::getline(iss, word, ' ') discards everything up to and including
        # the first ' ' (or the whole string when no space is present).
        first_space = s.find(' ')
        pos = n if first_space == -1 else first_space + 1

        def read_token():
            # operator>>(std::string): skip whitespace, then read a token.
            # None means extraction failed (eof/fail), like a failed >>.
            nonlocal pos
            while pos < n and s[pos] in _WS:
                pos += 1
            if pos >= n:
                return None
            start = pos
            while pos < n and s[pos] not in _WS:
                pos += 1
            return s[start:pos]

        while True:
            word = read_token()
            if word is None:
                break

            if word.startswith("--"):
                key_value = word[2:]
                eq = key_value.find('=')
                key = key_value if eq == -1 else key_value[:eq]
                value = "" if eq == -1 else key_value[eq + 1:]
                self.arguments[key] = self.convert_type(key, value if value != "" else "1")
            elif word.startswith("-"):
                key = word[1:]
                # char nxt = iss.peek(); if (!iss.eof() && iss.peek() != '-')
                if pos < n and s[pos] != '-':
                    value = read_token()
                    if value is None:
                        # Failed extraction leaves value empty; the failbit also
                        # terminates the enclosing loop on the next iteration.
                        self.arguments[key] = self.convert_type(key, "")
                        break
                    self.arguments[key] = self.convert_type(key, value)
                else:
                    self.arguments[key] = self.convert_type(key, "1")

        missing_args = {req for req in self.required if req not in self.arguments}
        return (not missing_args, missing_args)

    def get_argument(self, key):
        if key in self.arguments:
            return self.arguments[key]
        return ""

    def add_argument(self, arg, required=False, type="string"):
        if required:
            self.required.add(arg)
        self.types[arg] = type

    def convert_type(self, arg, value):
        if arg not in self.types:
            return value
        converter = self.type_converters.get(self.types[arg])
        if converter is not None:
            return converter(value)
        return value

    def initialize_converters(self):
        def int_converter(value):
            # std::to_string(std::stoi(value)), falling back to the original
            # value on any parse error (invalid_argument / out_of_range).
            try:
                match = _STOI_RE.match(value)
                if match is None:
                    raise ValueError("stoi: no conversion")
                number = int(match.group(1))
                if number < _INT_MIN or number > _INT_MAX:
                    raise ValueError("stoi: out of range")
                return str(number)
            except Exception:
                return value

        def bool_converter(value):
            tmp = value
            if tmp == "True":
                tmp = "1"
            if tmp == "False":
                tmp = "0"
            return tmp

        self.type_converters["int"] = int_converter
        self.type_converters["bool"] = bool_converter