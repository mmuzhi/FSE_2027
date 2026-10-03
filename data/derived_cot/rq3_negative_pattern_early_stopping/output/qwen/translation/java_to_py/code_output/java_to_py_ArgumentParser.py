import sys
from typing import Dict, Set, Optional, Tuple

class ArgumentParser:
    def __init__(self) -> None:
        self.arguments: Dict[str, object] = {}
        self.required: Set[str] = set()
        self.types: Dict[str, type] = {}

    def parse_arguments(self, command_string: str) -> Tuple[bool, Optional[Set[str]]]:
        args = command_string.split()
        # We start from index 1 because the first token might be the script name
        for i in range(1, len(args)):
            arg_str = args[i]
            if arg_str.startswith('--'):
                # Handle --key=value or --key
                # Split the string after '--' and then split by '='
                key_value = arg_str[2:].split('=', 1)
                key = key_value[0].strip()
                if len(key_value) == 2 and key_value[1].strip():
                    # There's a value part
                    self.arguments[key] = self.convert_type(key, key_value[1].strip())
                else:
                    # No value part, so just set to True
                    self.arguments[key] = True
            elif arg_str.startswith('-') and len(arg_str) > 1:
                # Handle -k or -k value
                key = arg_str[1:].strip()
                if i + 1 < len(args) and not args[i+1].startswith('-'):
                    # There is a value and it's not an option
                    self.arguments[key] = self.convert_type(key, args[i+1])
                    i += 1  # Skip the next argument
                else:
                    self.arguments[key] = True

        # Check for missing required arguments
        missing_args = self.required - set(self.arguments.keys())
        if missing_args:
            return (False, missing_args)
        return (True, None)

    def get_argument(self, key: str) -> Optional[object]:
        return self.arguments.get(key)

    def add_argument(self, arg: str, required: bool, arg_type: type) -> None:
        if required:
            self.required.add(arg)
        self.types[arg] = arg_type

    def convert_type(self, arg: str, value: str) -> object:
        arg_type = self.types.get(arg)
        if arg_type is None:
            return value

        try:
            if arg_type == int:
                return int(value)
            elif arg_type == bool:
                # Convert to boolean. Note: Java's Boolean.parseBoolean returns true for "true", false for "false", and ignores case.
                # We'll do the same.
                return value.lower() in ('true', 'yes', '1')
            elif arg_type == str:
                return value
        except Exception:
            # If conversion fails, return the original value (as in Java)
            pass
        return value

# Example usage in main (if needed)
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("arg1", True, int)
    parser.add_argument("arg2", False, str)
    parser.add_argument("option1", False, bool)
    parser.add_argument("option2", False, bool)

    # Note: The example command string in Java is: "python script.py --arg1=123 -arg2 value2 --option1 -option2"
    # We are only parsing the arguments after the script name, so we need to adjust the command string.
    # Let's assume we are calling the script as: "python script.py" and then the arguments are passed as separate tokens.
    # But note: the example command string in Java includes the script name. In Python, we might get the command line arguments differently.
    # However, the problem says to translate the code, so we'll keep the same interface.

    # We'll adjust the command string to be just the arguments part, but note that the original Java code splits the entire string.
    # Let's change the example to use the same format but without the script name.

    # Since we are in a script, we might use sys.argv, but the problem doesn't specify. We'll just use the same string as in Java but without the script name.
    # Alternatively, we can use the same string but note that the first token is the script name. We'll adjust the example.

    # Let's change the example command string to: "--arg1=123 -arg2 value2 --option1 -option2"
    result = parser.parse_arguments("--arg1=123 -arg2 value2 --option1 -option2")
    print(result[0])
    if result[1] is not None:
        print(result[1])
    print(parser.arguments)