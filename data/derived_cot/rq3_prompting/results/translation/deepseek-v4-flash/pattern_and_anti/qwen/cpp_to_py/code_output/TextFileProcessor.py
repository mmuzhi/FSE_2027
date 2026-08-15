import json

class TextFileProcessor:
    def __init__(self, filename):
        self.filename_ = filename

    def read_file_as_json(self):
        try:
            with open(self.filename_, 'rb') as f:
                data = f.read()
        except OSError:
            data = b""
        return json.loads(data.decode('utf-8-sig'))

    def read_file(self):
        try:
            with open(self.filename_, 'rb') as f:
                data = f.read()
        except OSError:
            return ""
        return data.decode('utf-8', errors='surrogateescape')

    def write_file(self, content):
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='surrogateescape')
        try:
            with open(self.filename_, 'wb') as f:
                f.write(content.encode('utf-8', errors='surrogateescape'))
        except OSError:
            pass

    def process_file(self):
        content = self.read_file()
        result = ''.join(c for c in content if ('A' <= c <= 'Z') or ('a' <= c <= 'z'))
        self.write_file(result)
        return result