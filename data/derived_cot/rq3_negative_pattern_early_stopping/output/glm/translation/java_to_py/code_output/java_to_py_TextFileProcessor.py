import json
import re

class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file_as_json(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except ValueError as e:
            raise OSError(str(e)) from e

    def read_file(self):
        with open(self.file_path, 'r') as f:
            return f.read()

    def write_file(self, content):
        with open(self.file_path, 'w') as f:
            f.write(content)

    def process_file(self):
        content = self.read_file()
        processed_content = re.sub(r'[^a-zA-Z]', '', content)
        self.write_file(processed_content)
        return processed_content