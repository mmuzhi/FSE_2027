import json
import os


class JSONProcessor:

    def read_json(self, file_path):
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r") as reader:
                # Gson deserializes JSON numbers into Double; parse_int=float mirrors that.
                # Gson throws (JsonSyntaxException) for a non-object root, so a non-dict
                # result must be treated as a parse failure.
                data = json.load(reader, parse_int=float)
                if not isinstance(data, dict):
                    raise ValueError("Expected a JSON object at root")
                return data
        except Exception:
            return None

    def write_json(self, data, file_path):
        try:
            with open(file_path, "w") as writer:
                json.dump(data, writer, separators=(",", ":"), ensure_ascii=False)
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