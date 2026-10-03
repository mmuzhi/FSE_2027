import json

class TextFileProcessor:
    def __init__(self, filename: str):
        self.filename = filename

    def read_file_as_json(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def read_file(self) -> str:
        with open(self.filename, 'r') as f:
            return f.read()

    def write_file(self, content: str) -> None:
        with open(self.filename, 'w') as f:
            f.write(content)

    def process_file(self) -> str:
        content = self.read_file()
        result = ''.join(c for c in content if c.isalpha())
        self.write_file(result)
        return result