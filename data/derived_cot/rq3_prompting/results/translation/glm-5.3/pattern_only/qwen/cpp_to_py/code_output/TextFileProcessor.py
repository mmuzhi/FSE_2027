import json


class TextFileProcessor:
    def __init__(self, filename):
        self._filename = filename

    def read_file_as_json(self):
        with open(self._filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def read_file(self):
        # surrogateescape keeps arbitrary bytes round-trippable, like rdbuf()
        with open(self._filename, 'r', encoding='utf-8', errors='surrogateescape') as file:
            return file.read()

    def write_file(self, content):
        # truncates/overwrites like ofstream
        with open(self._filename, 'w', encoding='utf-8', errors='surrogateescape') as file:
            file.write(content)

    def process_file(self):
        content = self.read_file()
        # isascii() + isalpha() matches C-locale isalpha() on chars (only [A-Za-z])
        result = ''.join(c for c in content if c.isascii() and c.isalpha())
        self.write_file(result)
        return result