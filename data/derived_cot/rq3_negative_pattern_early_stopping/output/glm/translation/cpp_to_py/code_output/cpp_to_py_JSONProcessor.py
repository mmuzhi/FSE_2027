import json


class JSONProcessor:

    def read_json(self, file_path, output):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, PermissionError, OSError):
            return 0
        except Exception:
            return -1

        if data is None:
            return -1

        output.append(data)
        return 1

    def write_json(self, data, file_path):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception:
            return -1

        return 1

    def process_json(self, file_path, remove_key):
        output = []
        result = self.read_json(file_path, output)

        if result != 1:
            return 0

        data = output[0]

        if isinstance(data, dict) and remove_key in data:
            del data[remove_key]
            return self.write_json(data, file_path)
        else:
            return 0