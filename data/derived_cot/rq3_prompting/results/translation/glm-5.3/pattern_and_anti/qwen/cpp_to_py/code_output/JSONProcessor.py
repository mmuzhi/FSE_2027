import json


class JSONProcessor:

    def read_json(self, file_path, output):
        # Emulates the C++ out-parameter via a mutable container.
        # Returns: 0 if the file cannot be opened,
        #         -1 on parse error or 'null' content,
        #          1 on success (parsed value stored in output['value']).
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
        except OSError:
            return 0
        except UnicodeDecodeError:
            return -1

        try:
            parsed = json.loads(content)
        except ValueError:  # json.JSONDecodeError
            return -1

        if parsed is None:
            return -1

        output['value'] = parsed
        return 1

    def write_json(self, data, file_path):
        # nlohmann::json uses std::map (sorted keys) and dump(4) emits
        # 4-space indent with raw UTF-8 (ensure_ascii=False), no trailing newline.
        try:
            dumped = json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(dumped)
        except (OSError, TypeError, ValueError):
            return -1
        return 1

    def process_json(self, file_path, remove_key):
        output = {}
        result = self.read_json(file_path, output)

        if result != 1:
            return 0

        data = output['value']
        # nlohmann's contains() is true only for object types with the key present.
        if isinstance(data, dict) and remove_key in data:
            del data[remove_key]
            return self.write_json(data, file_path)
        else:
            return 0