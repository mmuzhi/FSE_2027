import json


class JSONProcessor:

    def read_json(self, file_path):
        """Read JSON from file_path.

        Returns a (status, data) tuple:
            status 0  -> file could not be opened (data is None)
            status -1 -> parse error or JSON null (data is None)
            status 1  -> success (data holds the parsed JSON)
        """
        try:
            file = open(file_path, 'r')
        except Exception:
            return 0, None

        with file:
            try:
                output = json.load(file)
                if output is None:
                    return -1, None
            except Exception:
                return -1, None

        return 1, output

    def write_json(self, data, file_path):
        try:
            file = open(file_path, 'w')
        except Exception:
            return -1

        with file:
            try:
                # indent=4 mirrors dump(4); sort_keys mirrors std::map key ordering
                json.dump(data, file, indent=4, sort_keys=True)
            except Exception:
                return -1

        return 1

    def process_json(self, file_path, remove_key):
        result, data = self.read_json(file_path)

        if result != 1:
            return 0

        if isinstance(data, dict) and remove_key in data:
            del data[remove_key]
            return self.write_json(data, file_path)
        else:
            return 0