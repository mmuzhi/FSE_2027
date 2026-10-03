class Tuple:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    def parse_arguments(self, command_string):
        args = command_string.split()
        for i in range(1, len(args)):
            arg = args[i]
            if arg.startswith('--'):
                key_value = arg[2:].split('=', 1)
                if len(key_value) == 2:
                    self.arguments[key_value[0]] = self.convert_type(key_value[0], key_value[1])
                else:
                    self.arguments[key_value[0]] = True
            elif arg.startswith('-'):
                key = arg[1:]
                if i + 1 < len(args) and not args[i + 1].startswith('-'):
                    self.arguments[key] = self.convert_type(key, args[i + 1])
                    i += 1
                else:
                    self.arguments[key] = True
        missing_args = set(self.required) - set(self.arguments.keys())
        if missing_args:
            return Tuple(False, missing_args)
        return Tuple(True, None)

    def get_argument(self, key):
        return self.arguments.get(key)

    def add_argument(self, arg, required, arg_type):
        if required:
            self.required.add(arg)
        self.types[arg] = arg_type

    def convert_type(self, arg, value):
        try:
            arg_type = self.types.get(arg)
            if arg_type is int:
                return int(value)
            elif arg_type is bool:
                return value.lower() == 'true'
            elif arg_type is str:
                return value
        except Exception:
            return value
        return value

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('arg1', True, int)
    parser.add_argument('arg2', False, str)
    parser.add_argument('option1', False, bool)
    parser.add_argument('option2', False, bool)

    result = parser.parse_arguments('python script.py --arg1=123 -arg2 value2 --option1 -option2')
    print(result.x)
    print(result.y)
    print(parser.arguments)