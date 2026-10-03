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

    def parseArguments(self, commandString):
        args = re.split(r'\s+', commandString)
        i = 1
        while i < len(args):
            arg = args[i]
            if arg.startswith("--"):
                keyValue = arg[2:].split("=")
                if len(keyValue) == 2:
                    self.arguments[keyValue[0]] = self.convertType(keyValue[0], keyValue[1])
                else:
                    self.arguments[keyValue[0]] = True
            elif arg.startswith("-"):
                key = arg[1:]
                if i + 1 < len(args) and not args[i + 1].startswith("-"):
                    self.arguments[key] = self.convertType(key, args[i + 1])
                    i += 1
                else:
                    self.arguments[key] = True
            i += 1
            
        missingArgs = self.required - set(self.arguments.keys())
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
            type_ = self.types.get(arg)
            if type_ == int:
                return int(value)
            elif type_ == bool:
                return value.lower() == 'true'
            elif type_ == str:
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