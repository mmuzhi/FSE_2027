class CamelCaseMap:
    def __init__(self):
        self.data = {}
        self.insertion_order = []

    @staticmethod
    def to_camel_case(key):
        camel_case_key = []
        capitalize = False
        for c in key:
            if c == '_':
                capitalize = True
            else:
                camel_case_key.append(c.upper() if capitalize else c)
                capitalize = False
        return ''.join(camel_case_key)

    def convert_key(self, key):
        return self.to_camel_case(key)

    def set_item(self, key, value):
        camel_key = self.convert_key(key)
        if camel_key not in self.data:
            self.insertion_order.append(camel_key)
        self.data[camel_key] = value

    def get_item(self, key):
        # data.at() throws on missing key -> KeyError
        return self.data[self.convert_key(key)]

    def del_item(self, key):
        camel_key = self.convert_key(key)
        # data.erase() is a no-op on missing key
        self.data.pop(camel_key, None)
        # erase-remove idiom removes ALL occurrences of camel_key
        self.insertion_order = [k for k in self.insertion_order if k != camel_key]

    def len(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.insertion_order)

    __setitem__ = set_item
    __getitem__ = get_item
    __delitem__ = del_item
    __len__ = len