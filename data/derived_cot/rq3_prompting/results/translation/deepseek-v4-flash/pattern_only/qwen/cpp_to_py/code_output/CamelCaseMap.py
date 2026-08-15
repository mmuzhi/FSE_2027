class CamelCaseMap:
    def __init__(self):
        self.data = {}
        self.insertion_order = []

    @staticmethod
    def to_camel_case(key):
        result = []
        capitalize = False
        for c in key:
            if c == '_':
                capitalize = True
            else:
                if capitalize and 'a' <= c <= 'z':
                    result.append(chr(ord(c) - 32))
                else:
                    result.append(c)
                capitalize = False
        return ''.join(result)

    def convert_key(self, key):
        return self.to_camel_case(key)

    def set_item(self, key, value):
        camel_key = self.convert_key(key)
        if camel_key not in self.data:
            self.insertion_order.append(camel_key)
        self.data[camel_key] = value

    def get_item(self, key):
        return self.data[self.convert_key(key)]

    def del_item(self, key):
        camel_key = self.convert_key(key)
        self.data.pop(camel_key, None)
        self.insertion_order[:] = [k for k in self.insertion_order if k != camel_key]

    def len(self):
        return len(self.data)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.insertion_order)

    def begin(self):
        return iter(self.insertion_order)

    def end(self):
        return iter([])