import re
from typing import Dict, Set, Tuple, Optional


class ArgumentParser:
    def __init__(self):
        self.initialize_converters()
        self.arguments: Dict[str, str] = {}
        self.required: Set[str] = set()
        self.types: Dict[str, str] = {}
        self.type_converters: Dict[str, callable] = {}

    def parse_arguments(self, command_string: str) -> Tuple[bool, Set[str]]:
        words = iter(command_string.split())
        missing_args = set()

        for word in words:
            if word.startswith('--'):
                key_value = word[2:]
                if '=' in key_value:
                    key, _, value = key_value.partition('=')
                    value_str = value if value else "1"
                else:
                    key = key_value
                    value_str = "1"
                try:
                    self.arguments[key] = self.convert_type(key, value_str)
                except Exception:
                    # Preserve C++ behavior by keeping original value on conversion error
                    self.arguments[key] = value_str
            elif word.startswith('-'):
                key = word[1:]
                try:
                    if not next(words, None):
                        value_str = "1"
                    else:
                        value_str = next(words)
                    self.arguments[key] = self.convert_type(key, value_str)
                except Exception:
                    # Preserve C++ behavior by keeping original value on conversion error
                    self.arguments[key] = value_str

        for req in self.required:
            if req not in self.arguments:
                missing_args.add(req)

        return (len(missing_args) == 0, missing_args)

    def get_argument(self, key: str) -> str:
        return self.arguments.get(key, "")

    def add_argument(self, arg: str, required: bool = False, typ: str = "string"):
        if required:
            self.required.add(arg)
        self.types[arg] = typ

    def convert_type(self, arg: str, value: str) -> str:
        if arg not in self.types:
            return value
        converter = self.type_converters.get(self.types[arg])
        if converter:
            try:
                return converter(value)
            except Exception:
                return value
        return value

    def initialize_converters(self):
        self.type_converters["int"] = lambda v: str(int(v)) if v.isdigit() else v
        self.type_converters["bool"] = lambda v: "1" if v.lower() == "true" else "0"