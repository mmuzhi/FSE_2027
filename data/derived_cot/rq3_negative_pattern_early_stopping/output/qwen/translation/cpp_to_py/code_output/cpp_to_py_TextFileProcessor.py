import json
import os

class TextFileProcessor:
    def __init__(self, filename):
        self.filename = filename

    def read_file_as_json(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
            return json.loads(content)
        except FileNotFoundError:
            return json.loads('{}')  # Return an empty JSON object if file not found

    def read_file(self):
        try:
            with open(self.filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return ''

    def write_file(self, content):
        with open(self.filename, 'w') as file:
            file.write(content)

    def process_file(self):
        content = self.read_file()
        result = ''.join(filter(str.isalpha, content))
        self.write_file(result)
        return result