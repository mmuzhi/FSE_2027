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
        parts = key.split("_")
        # Java's String.split drops trailing empty strings; Python's does not.
        while parts and parts[-1] == "":
            parts.pop()
        camelCaseString = parts[0]
        for i in range(1, len(parts)):
            camelCaseString += parts[i][:1].upper() + parts[i][1:].lower()
        return camelCaseString

    def keySet(self):
        return self._data.keys()

    def size(self):
        return len(self._data)