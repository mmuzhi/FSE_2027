import json


class TextFileProcessor:
    def __init__(self, filename: str) -> None:
        self._filename = filename

    def read_file_as_json(self):
        with open(self._filename, 'rb') as f:
            return json.loads(f.read().decode('utf-8'))

    def read_file(self) -> str:
        # C++ reads raw bytes via rdbuf(); use surrogateescape to round-trip
        # arbitrary bytes losslessly through a str.
        with open(self._filename, 'rb') as f:
            return f.read().decode('utf-8', errors='surrogateescape')

    def write_file(self, content: str) -> None:
        # Binary mode matches ofstream's raw byte writes (no newline translation).
        with open(self._filename, 'wb') as f:
            f.write(content.encode('utf-8', errors='surrogateescape'))

    def process_file(self) -> str:
        content = self.read_file()
        result = ''.join(
            c for c in content if 'a' <= c <= 'z' or 'A' <= c <= 'Z'
        )
        self.write_file(result)
        return result