import json
import re
import locale


class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def _default_encoding(self):
        return locale.getpreferredencoding(False)

    def read_file_as_json(self):
        with open(self.file_path, 'rb') as f:
            data = f.read()
        return json.loads(data.decode('utf-8-sig'))

    def read_file(self):
        with open(self.file_path, 'rb') as f:
            data = f.read()
        return data.decode(self._default_encoding(), errors='replace')

    def write_file(self, content):
        data = content.encode(self._default_encoding(), errors='replace')
        with open(self.file_path, 'wb') as f:
            f.write(data)

    def process_file(self):
        content = self.read_file()
        processed_content = re.sub(r'[^a-zA-Z]', '', content)
        self.write_file(processed_content)
        return processed_content