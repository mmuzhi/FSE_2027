import json

class TextFileProcessor:
    def __init__(self, filename):
        self.filename = filename

    def read_file_as_json(self):
        with open(self.filename, 'r', encoding='utf-8-sig') as f:
            return json.load(f)

    def read_file(self):
        try:
            with open(self.filename, 'rb') as f:
                return f.read()
        except OSError:
            return b''

    def write_file(self, content):
        try:
            with open(self.filename, 'wb') as f:
                f.write(content)
        except OSError:
            pass

    def process_file(self):
        content = self.read_file()
        result = bytearray()
        for c in content:
            if (65 <= c <= 90) or (97 <= c <= 122):
                result.append(c)
        result = bytes(result)
        self.write_file(result)
        return result