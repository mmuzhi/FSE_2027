class CamelCaseMap:
    """A mapping that stores keys in camelCase but accepts snake_case keys for modification."""

    def __init__(self):
        self.data = {}
        self.insertion_order = []

    @staticmethod
    def to_camel_case(key: str) -> str:
        """Convert a snake_case string to camelCase (first letter lowercase)."""
        result = []
        capitalize = False
        for c in key:
            if c == '_':
                capitalize = True
            else:
                result.append(c.upper() if capitalize else c)
                capitalize = False
        return ''.join(result)

    def convert_key(self, key: str) -> str:
        """Return the camelCase version of *key*."""
        return self.to_camel_case(key)

    def set_item(self, key: str, value: str) -> None:
        """Insert or update *value* under the camelCase version of *key*."""
        camel_key = self.convert_key(key)
        if camel_key not in self.data:
            self.insertion_order.append(camel_key)
        self.data[camel_key] = value

    def get_item(self, key: str) -> str:
        """Return the value stored under the camelCase version of *key*.
        Raises KeyError if the key does not exist."""
        camel_key = self.convert_key(key)
        return self.data[camel_key]

    def del_item(self, key: str) -> None:
        """Remove the entry for *key* if it exists; otherwise do nothing."""
        camel_key = self.convert_key(key)
        if camel_key in self.data:
            del self.data[camel_key]
        try:
            self.insertion_order.remove(camel_key)
        except ValueError:
            pass

    def len(self) -> int:
        """Return the number of stored items."""
        return len(self.data)

    def __len__(self) -> int:
        return self.len()

    def __iter__(self):
        """Iterate over the keys in insertion order."""
        return iter(self.insertion_order)