import json


class JSONProcessor:
    def read_json(self, file_path):
        try:
            f = open(file_path, 'r', encoding='utf-8')
        except IsADirectoryError:
            return -1, None
        except Exception:
            return 0, None

        try:
            try:
                content = f.read()
            except Exception:
                return -1, None
        finally:
            try:
                f.close()
            except Exception:
                pass

        try:
            decoder = json.JSONDecoder()
            idx = 0
            while idx < len(content) and content[idx] in ' \t\n\r':
                idx += 1
            data, _ = decoder.raw_decode(content, idx)
        except Exception:
            return -1, None

        if data is None:
            return -1, None

        return 1, data

    def write_json(self, data, file_path):
        try:
            f = open(file_path, 'w', encoding='utf-8')
        except Exception:
            return -1

        try:
            try:
                dumped = json.dumps(data, indent=4, ensure_ascii=False)
            except Exception:
                return -1

            try:
                f.write(dumped)
            except Exception:
                pass
            finally:
                try:
                    f.close()
                except Exception:
                    pass

            return 1
        except Exception:
            return -1

    def process_json(self, file_path, remove_key):
        result, data = self.read_json(file_path)
        if result != 1:
            return 0

        if isinstance(data, dict) and remove_key in data:
            del data[remove_key]
            return self.write_json(data, file_path)

        return 0