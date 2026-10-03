import json
import os

class JSONProcessor:
    def read_json(self, file_path):
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception:
            return None

    def write_json(self, data, file_path):
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            return True
        except Exception:
            return False

    def process_json(self, file_path, remove_key):
        data = self.read_json(file_path)
        if data is None:
            return False
        if remove_key in data:
            del data[remove_key]
            return self.write_json(data, file_path)
        else:
            return False