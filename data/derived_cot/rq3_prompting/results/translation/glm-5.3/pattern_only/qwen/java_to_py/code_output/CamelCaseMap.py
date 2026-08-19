class CamelCaseMap:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(self._convert_key(key))

    def put(self, key, value):
        self.data[self._convert_key(key)] = value

    def remove(self, key):
        # Java's Map.remove is a no-op for absent keys (no exception)
        self.data.pop(self._convert_key(key), None)

    def _convert_key(self, key):
        if key is None:
            return None
        return self._to_camel_case(key)

    @staticmethod
    def _to_camel_case(key):
        parts = key.split("_")
        # Java's String.split(regex) drops trailing empty strings
        while parts and parts[-1] == "":
            parts.pop()
        # parts[0] raises IndexError on empty list, mirroring Java's AIOOBE
        camel_case_string = parts[0]
        for part in parts[1:]:
            # part[0] raises IndexError for empty parts, mirroring substring(0, 1)
            camel_case_string += part[0].upper() + part[1:].lower()
        return camel_case_string

    def key_set(self):
        return self.data.keys()

    def size(self):
        return len(self.data)