import re


class Tuple:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    @staticmethod
    def _java_split(s, pattern):
        # Emulates Java's String.split(regex) with limit 0:
        # no match -> [input]; otherwise trailing empty strings are dropped.
        parts = re.split(pattern, s, flags=re.ASCII)
        if len(parts) == 1:
            return parts
        while parts and parts[-1] == '':
            parts.pop()
        return parts

    def parseArguments(self, commandString):
        args = self._java_split(commandString, r'\s+')
        i = 1
        while i < len(args):
            arg = args[i]
            if arg.startswith('--'):
                keyValue = self._java_split(arg[2:], '=')
                if len(keyValue) == 2:
                    self.arguments[keyValue[0]] = self.convertType(keyValue[0], keyValue[1])
                else:
                    self.arguments[keyValue[0]] = True
            elif arg.startswith('-'):
                key = arg[1:]
                if i + 1 < len(args) and not args[i + 1].startswith('-'):
                    self.arguments[key] = self.convertType(key, args[i + 1])
                    i += 1
                else:
                    self.arguments[key] = True
            i += 1
        missingArgs = set(self.required)
        missingArgs -= self.arguments.keys()
        if missingArgs:
            return Tuple(False, missingArgs)
        return Tuple(True, None)

    def getArgument(self, key):
        return self.arguments.get(key)

    def addArgument(self, arg, required, argType):
        if required:
            self.required.add(arg)
        self.types[arg] = argType

    def convertType(self, arg, value):
        try:
            argType = self.types.get(arg)
            if argType is int:
                return int(value)
            elif argType is bool:
                return value.lower() == 'true'
            elif argType is str:
                return value
        except Exception:
            return value
        return value


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.addArgument("arg1", True, int)
    parser.addArgument("arg2", False, str)
    parser.addArgument("option1", False, bool)
    parser.addArgument("option2", False, bool)

    result = parser.parseArguments("python script.py --arg1=123 -arg2 value2 --option1 -option2")
    print(result.x)
    print(result.y)
    print(parser.arguments)