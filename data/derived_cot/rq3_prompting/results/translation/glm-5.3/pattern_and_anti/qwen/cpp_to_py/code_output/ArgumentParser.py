import re

# Whitespace characters recognized by std::istream extraction in the default C locale.
_CPP_WS = " \t\n\v\f\r"

# Emulates the prefix std::strtol (base 10) would parse for std::stoi.
_STOI_RE = re.compile(r"[ \t\n\v\f\r]*[+-]?[0-9]+")


class ArgumentParser:
    def __init__(self):
        self.arguments = {}    # std::map<std::string, std::string>
        self.required = set()  # std::set<std::string>
        self.types = {}        # std::map<std::string, std::string>
        self.type_converters = {}  # std::map<std::string, std::function<...>>
        self.initialize_converters()

    def parse_arguments(self, command_string):
        s = command_string
        n = len(s)

        # std::getline(iss, word, ' ') consumes the first space-delimited
        # field (the command name, using ' ' as the only delimiter); discarded.
        first_space = s.find(' ')
        i = n if first_space == -1 else first_space + 1

        def skip_ws(pos):
            while pos < n and s[pos] in _CPP_WS:
                pos += 1
            return pos

        def read_token(pos):
            pos = skip_ws(pos)
            start = pos
            while pos < n and s[pos] not in _CPP_WS:
                pos += 1
            return s[start:pos], pos

        while True:
            j = skip_ws(i)
            if j >= n:
                break
            word, i = read_token(j)  # iss >> word

            if word.startswith("--"):
                key_value = word[2:]
                pos = key_value.find('=')
                if pos == -1:
                    key, value = key_value, ""
                else:
                    key, value = key_value[:pos], key_value[pos + 1:]
                self.arguments[key] = self.convert_type(key, "1" if value == "" else value)
            elif word.startswith("-"):
                key = word[1:]
                # iss.peek() looks at the character immediately after the token
                # (it does NOT skip whitespace).
                if i < n and s[i] != '-':
                    value, i = read_token(i)  # iss >> value; "" if extraction fails
                    self.arguments[key] = self.convert_type(key, value)
                else:
                    self.arguments[key] = self.convert_type(key, "1")

        missing_args = {req for req in self.required if req not in self.arguments}
        return (len(missing_args) == 0, missing_args)

    def get_argument(self, key):
        return self.arguments.get(key, "")

    def add_argument(self, arg, required=False, type="string"):
        if required:
            self.required.add(arg)
        self.types[arg] = type

    def convert_type(self, arg, value):
        if arg in self.types:
            converter = self.type_converters.get(self.types[arg])
            if converter is not None:
                return converter(value)
        return value

    def initialize_converters(self):
        def to_int(value):
            # std::to_string(std::stoi(value)); on invalid_argument or
            # out_of_range the original value is returned unchanged.
            m = _STOI_RE.match(value)
            if m is None:
                return value
            number = int(m.group(0))
            if number < -2147483648 or number > 2147483647:
                return value  # std::out_of_range (32-bit int assumed)
            return str(number)

        def to_bool(value):
            if value == "True":
                return "1"
            if value == "False":
                return "0"
            return value

        self.type_converters["int"] = to_int
        self.type_converters["bool"] = to_bool