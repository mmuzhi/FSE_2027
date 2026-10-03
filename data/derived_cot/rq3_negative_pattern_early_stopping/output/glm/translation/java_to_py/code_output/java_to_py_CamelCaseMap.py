class CamelCaseMap:
    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data.get(self._convert_key(key))

    def put(self, key, value):
        self._data[self._convert_key(key)] = value

    def remove(self, key):
        self._data.pop(self._convert_key(key), None)

    def _convert_key(self, key):
        if key is None:
            return None
        return self._to_camel_case(key)

    @staticmethod
    def _to_camel_case(key):
        parts = key.split("_")
        while parts and parts[-1] == '':
            parts.pop()
        camel_case_string = parts[0]
        for i in range(1, len(parts)):
            camel_case_string += parts[i][0].upper() + parts[i][1:].lower()
        return camel_case_string

    def key_set(self):
        return self._data.keys()

    def size(self):
        return len(self._data)