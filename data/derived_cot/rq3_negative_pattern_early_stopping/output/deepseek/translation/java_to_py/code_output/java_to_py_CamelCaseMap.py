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
        parts = key.split('_')
        camel_case = parts[0]
        for part in parts[1:]:
            camel_case += part[0].upper() + part[1:].lower()
        return camel_case

    def key_set(self):
        return set(self._data.keys())

    def size(self):
        return len(self._data)