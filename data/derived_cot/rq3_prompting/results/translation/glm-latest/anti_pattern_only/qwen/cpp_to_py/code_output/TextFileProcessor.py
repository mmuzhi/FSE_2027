import json
from typing import Any


class TextFileProcessor:
    def __init__(self, filename: str) -> None:
        self._filename = filename

    def read_file_as_json(self) -> Any:
        with open(self._filename, encoding="utf-8") as file:
            return json.load(file)

    def read_file(self) -> str:
        with open(self._filename, encoding="utf-8") as file:
            return file.read()

    def write_file(self, content: str) -> None:
        with open(self._filename, "w", encoding="utf-8") as file:
            file.write(content)

    def process_file(self) -> str:
        content = self.read_file()
        # std::isalpha in the default "C" locale: ASCII letters only
        result = "".join(c for c in content if "a" <= c <= "z" or "A" <= c <= "Z")
        self.write_file(result)
        return result