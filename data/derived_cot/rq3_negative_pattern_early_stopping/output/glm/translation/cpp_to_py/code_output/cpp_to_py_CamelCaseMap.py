class CamelCaseMap:
    def __init__(self):
        self.data: dict[str, str] = {}
        self.insertion_order: list[str] = []

    @staticmethod
    def to_camel_case(key: str) -> str:
        camel_case_key = []
        capitalize = False
        for c in key:
            if c == '_':
                capitalize = True
            else:
                if capitalize:
                    camel_case_key.append(c.upper())
                else:
                    camel_case_key.append(c)
                capitalize = False
        return "".join(camel_case_key)

    def convert_key(self, key: str) -> str:
        return CamelCaseMap.to_camel_case(key)

    def set_item(self, key: str, value: str) -> None:
        camel_key = self.convert_key(key)
        if camel_key not in self.data:
            self.insertion_order.append(camel_key)
        self.data[camel_key] = value

    def get_item(self, key: str) -> str:
        return self.data[self.convert_key(key)]

    def del_item(self, key: str) -> None:
        camel_key = self.convert_key(key)
        self.data.pop(camel_key, None)
        self.insertion_order = [k for k in self.insertion_order if k != camel_key]

    def len(self) -> int:
        return len(self.data)

    def __len__(self) -> int:
        return self.len()

    def __iter__(self):
        return iter(self.insertion_order)