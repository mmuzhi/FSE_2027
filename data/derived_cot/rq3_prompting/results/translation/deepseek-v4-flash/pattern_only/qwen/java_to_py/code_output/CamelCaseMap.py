def _java_split_underscore(s):
    if s == '':
        return ['']
    parts = s.split('_')
    while parts and parts[-1] == '':
        parts.pop()
    return parts


class CamelCaseMap:
    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data.get(self._convertKey(key))

    def put(self, key, value):
        self._data[self._convertKey(key)] = value

    def remove(self, key):
        self._data.pop(self._convertKey(key), None)

    def _convertKey(self, key):
        if key is None:
            return None
        return CamelCaseMap._toCamelCase(key)

    @staticmethod
    def _toCamelCase(key):
        parts = _java_split_underscore(key)
        camel_case_string = parts[0]
        for part in parts[1:]:
            camel_case_string += part[0].upper() + part[1:].lower()
        return camel_case_string

    def keySet(self):
        return self._data.keys()

    def size(self):
        return len(self._data)