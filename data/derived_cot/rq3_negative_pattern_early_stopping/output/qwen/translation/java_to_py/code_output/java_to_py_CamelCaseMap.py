from collections import OrderedDict

class CamelCaseMap:
    def __init__(self):
        self.data = OrderedDict()

    def get(self, key):
        return self.data.get(self._to_camel_case(key))

    def put(self, key, value):
        camel_key = self._to_camel_case(key)
        self.data[camel_key] = value

    def remove(self, key):
        camel_key = self._to_camel_case(key)
        if camel_key in self.data:
            del self.data[camel_key]

    def keySet(self):
        return set(self.data.keys())

    def size(self):
        return len(self.data)

    @staticmethod
    def _to_camel_case(key):
        if key is None:
            return None
        parts = key.split('_')
        if len(parts) == 1:
            return parts[0]
        camel_case = parts[0]
        for part in parts[1:]:
            if part:
                camel_case += part[0].upper() + part[1:].lower()
            else:
                camel_case += part  # Handle empty parts
        return camel_case