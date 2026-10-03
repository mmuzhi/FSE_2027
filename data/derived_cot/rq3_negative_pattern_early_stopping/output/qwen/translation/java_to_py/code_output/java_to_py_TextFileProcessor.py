import json
import os
import errno
import locale

class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file_as_json(self):
        encoding = locale.getpreferredencoding()
        try:
            with open(self.file_path, 'r', encoding=encoding) as f:
                return json.load(f)
        except FileNotFoundError as e:
            raise e
        except OSError as e:
            raise OSError from e
        except json.JSONDecodeError as e:
            import errno
            raise OSError(errno.EIO, f"JSON decode error: {e.msg}", self.file_path) from e

    def read_file(self):
        encoding = locale.getpreferredencoding()
        try:
            with open(self.file_path, 'r', encoding=encoding) as f:
                return f.read()
        except FileNotFoundError as e:
            raise e
        except OSError as e:
            raise OSError from e
        except UnicodeDecodeError as e:
            import errno
            raise OSError(errno.EIO, f"Decoding error: {e.reason}", self.file_path) from e

    def write_file(self, content):
        encoding = locale.getpreferredencoding()
        try:
            with open(self.file_path, 'w', encoding=encoding) as f:
                f.write(content)
        except OSError as e:
            raise OSError from e
        except UnicodeEncodeError as e:
            import errno
            raise OSError(errno.EIO, f"Encoding error: {e.reason}", self.file_path) from e

    def process_file(self):
        content = self.read_file()
        processed_content = ''.join(filter(str.isalpha, content))
        self.write_file(processed_content)
        return processed_content