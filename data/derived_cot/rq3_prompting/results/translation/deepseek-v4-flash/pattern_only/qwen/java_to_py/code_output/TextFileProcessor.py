import json
import re
import locale


class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file_as_json(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def read_file(self):
        encoding = locale.getpreferredencoding(False)
        with open(self.file_path, 'rb') as f:
            return f.read().decode(encoding, errors='replace')

    def write_file(self, content):
        encoding = locale.getpreferredencoding(False)
        with open(self.file_path, 'wb') as f:
            f.write(content.encode(encoding, errors='replace'))

    def process_file(self):
        content = self.read_file()
        processed_content = re.sub(r'[^a-zA-Z]', '', content)
        self.write_file(processed_content)
        return processed_content