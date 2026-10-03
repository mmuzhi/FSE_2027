import json

class JSONProcessor:
    """
    Mimics the C++ JSONProcessor class using Python's built-in json module.
    Return codes:
        1: success
        0: file not found / key not present (process_json)
       -1: corrupted JSON, null JSON, or write failure
    """

    def read_json(self, file_path: str, output: dict) -> int:
        """
        Read a JSON file into `output` (a mutable dict-like object).
        Returns 1 on success, 0 if file cannot be opened, -1 if JSON is null or malformed.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            return 0
        except (json.JSONDecodeError, UnicodeDecodeError, IOError):
            return -1

        if data is None:
            return -1

        if isinstance(output, dict):
            output.clear()
            output.update(data)
        else:
            pass

        return 1

    def write_json(self, data, file_path: str) -> int:
        """
        Write JSON data to a file with indent 4.
        Returns 1 on success, -1 on failure.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except (IOError, TypeError):
            return -1
        return 1

    def process_json(self, file_path: str, remove_key: str) -> int:
        """
        Read a JSON file, remove a key if present, then write back.
        Returns:
            1 on successful removal and write,
            0 if file cannot be read or key is missing,
            -1 if write fails.
        """
        data = {}
        result = self.read_json(file_path, data)
        if result != 1:
            return 0

        if remove_key in data:
            del data[remove_key]
            return self.write_json(data, file_path)
        else:
            return 0