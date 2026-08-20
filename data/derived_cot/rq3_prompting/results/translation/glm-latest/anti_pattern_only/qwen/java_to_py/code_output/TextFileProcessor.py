import json
import re


class TextFileProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file_as_json(self):
        # Jackson's ObjectMapper.readValue(File, Object.class):
        # reads the file and parses JSON, returning dict/list/str/int/float/bool/None.
        # Parse failures surface as exceptions (json.JSONDecodeError) instead of
        # Java's IOException subclasses.
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def read_file(self) -> str:
        # Equivalent of new String(Files.readAllBytes(...)): decodes raw bytes
        # using the default encoding, with no newline translation (newline="").
        with open(self.file_path, "r", newline="") as f:
            return f.read()

    def write_file(self, content: str) -> None:
        # Equivalent of Files.write(...): creates or truncates the file and
        # encodes using the default encoding, no newline translation.
        with open(self.file_path, "w", newline="") as f:
            f.write(content)

    def process_file(self) -> str:
        content = self.read_file()
        processed_content = re.sub(r"[^a-zA-Z]", "", content)
        self.write_file(processed_content)
        return processed_content