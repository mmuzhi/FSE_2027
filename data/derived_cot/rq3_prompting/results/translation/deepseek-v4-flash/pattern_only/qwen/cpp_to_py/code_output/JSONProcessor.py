import json


def _sort_json(obj):
    if isinstance(obj, dict):
        return {k: _sort_json(v) for k, v in sorted(obj.items())}
    if isinstance(obj, list):
        return [_sort_json(item) for item in obj]
    return obj


class JSON:
    def __init__(self, value=None):
        self.value = value

    def contains(self, key):
        return isinstance(self.value, dict) and key in self.value

    def erase(self, key):
        if isinstance(self.value, dict) and key in self.value:
            del self.value[key]

    def dump(self, indent=4):
        return json.dumps(self.value, indent=indent, ensure_ascii=False, sort_keys=True)


class JSONProcessor:
    def read_json(self, file_path, output):
        try:
            f = open(file_path, 'r', encoding='utf-8')
        except Exception:
            return 0

        try:
            with f:
                content = f.read()
            decoder = json.JSONDecoder()
            parsed, _ = decoder.raw_decode(content)
            output.value = _sort_json(parsed)
            if parsed is None:
                return -1
        except Exception:
            return -1

        return 1

    def write_json(self, data, file_path):
        try:
            if isinstance(data, JSON):
                serialized = data.dump(4)
            else:
                serialized = json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(serialized)
        except Exception:
            return -1

        return 1

    def process_json(self, file_path, remove_key):
        data = JSON()
        result = self.read_json(file_path, data)

        if result != 1:
            return 0

        if data.contains(remove_key):
            data.erase(remove_key)
            return self.write_json(data, file_path)
        else:
            return 0