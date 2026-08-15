class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}
        self.type_converters = {}
        self.initialize_converters()

    def parse_arguments(self, command_string):
        # Replicate getline(iss, word, ' ')
        if ' ' in command_string:
            first, rest = command_string.split(' ', 1)
        else:
            first = command_string
            rest = ''
        # first is discarded

        # Tokenize using C++ whitespace: space, tab, newline, CR, VT, FF
        tokens = []
        i = 0
        n = len(rest)
        while i < n:
            while i < n and rest[i] in ' \t\n\r\v\f':
                i += 1
            if i >= n:
                break
            start = i
            while i < n and rest[i] not in ' \t\n\r\v\f':
                i += 1
            tokens.append(rest[start:i])

        has_trailing_ws = bool(rest) and rest[-1] in ' \t\n\r\v\f'

        i = 0
        while i < len(tokens):
            word = tokens[i]
            i += 1

            if word.startswith('--'):
                key_value = word[2:]
                if '=' in key_value:
                    pos = key_value.index('=')
                    key = key_value[:pos]
                    value = key_value[pos + 1:]
                else:
                    key = key_value
                    value = ''
                if value == '':
                    value = '1'
                self.arguments[key] = self.convert_type(key, value)

            elif word.startswith('-'):
                key = word[1:]
                if i < len(tokens):
                    value = tokens[i]
                    i += 1
                else:
                    if has_trailing_ws:
                        value = ''
                    else:
                        value = '1'
                self.arguments[key] = self.convert_type(key, value)

            # Words not starting with '-' are ignored

        missing_args = set()
        for req in self.required:
            if req not in self.arguments:
                missing_args.add(req)

        return (len(missing_args) == 0, missing_args)

    def get_argument(self, key):
        return self.arguments.get(key, '')

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
            try:
                i = 0
                n = len(value)
                while i < n and value[i] in ' \t\n\r\v\f':
                    i += 1
                if i >= n:
                    raise ValueError

                sign = 1
                if value[i] == '+':
                    i += 1
                elif value[i] == '-':
                    sign = -1
                    i += 1

                if i >= n:
                    raise ValueError

                start = i
                while i < n and '0' <= value[i] <= '9':
                    i += 1

                if i == start:
                    raise ValueError

                num = int(value[start:i]) * sign
                if num < -2147483648 or num > 2147483647:
                    raise OverflowError

                return str(num)
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