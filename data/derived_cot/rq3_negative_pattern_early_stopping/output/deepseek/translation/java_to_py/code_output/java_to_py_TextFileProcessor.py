import json
import re
from pathlib import Path

class TextFileProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file_as_json(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def read_file(self) -> str:
        return Path(self.file_path).read_text(encoding='utf-8')

    def write_file(self, content: str) -> None:
        Path(self.file_path).write_text(content, encoding='utf-8')

    def process_file(self) -> str:
        content = self.read_file()
        processed_content = re.sub(r'[^a-zA-Z]', '', content)
        self.write_file(processed_content)
        return processed_content