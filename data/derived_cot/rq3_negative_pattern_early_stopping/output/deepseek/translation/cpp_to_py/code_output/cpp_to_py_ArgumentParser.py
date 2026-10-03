class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}
        self.type_converters = {}
        self.initialize_converters()

    def initialize_converters(self):
        def int_converter(value: str) -> str:
            try:
                return str(int(value))
            except (ValueError, TypeError):
                return value

        def bool_converter(value: str) -> str:
            if value == "True":
                return "1"
            elif value == "False":
                return "0"
            else:
                return value

        self.type_converters["int"] = int_converter
        self.type_converters["bool"] = bool_converter

    def convert_type(self, arg: str, value: str) -> str:
        if arg not in self.types:
            return value
        type_name = self.types[arg]
        converter = self.type_converters.get(type_name)
        if converter is None:
            return value
        return converter(value)

    def parse_arguments(self, command_string: str):
        parts = command_string.split(' ', 1)
        rest = parts[1] if len(parts) == 2 else ''
        tokens = rest.split()  # split on any whitespace, discarding empty strings

        i = 0
        while i < len(tokens):
            word = tokens[i]
            if word.startswith('--'):
                key_value = word[2:]  # remove leading '--'
                if '=' in key_value:
                    key, value = key_value.split('=', 1)
                    if value == '':
                        value = '1'
                else:
                    key = key_value
                    value = '1'
                self.arguments[key] = self.convert_type(key, value)
                i += 1
            elif word.startswith('-'):
                key = word[1:]  # remove leading '-'
                if (i + 1 < len(tokens)) and not tokens[i + 1].startswith('-'):
                    value = tokens[i + 1]
                    i += 2
                else:
                    value = '1'
                    i += 1
                self.arguments[key] = self.convert_type(key, value)
            else:
                i += 1

        missing_args = set()
        for req in self.required:
            if req not in self.arguments:
                missing_args.add(req)

        return (len(missing_args) == 0, missing_args)

    def get_argument(self, key: str) -> str:
        return self.arguments.get(key, "")

    def add_argument(self, arg: str, required: bool = False, type: str = "string"):
        if required:
            self.required.add(arg)
        self.types[arg] = type