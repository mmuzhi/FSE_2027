import re

class CamelCaseMap:
    def __init__(self):
        self.data = {}
        self.insertion_order = []

    @staticmethod
    def to_camel_case(key):
        components = re.split(r'_+', key)
        camel_case = components[0]
        for comp in components[1:]:
            if comp:  # Ensure non-empty components
                camel_case += comp.capitalize()
        return camel_case

    def set_item(self, key, value):
        camel_key = self.to_camel_case(key)
        if camel_key not in self.data:
            self.insertion_order.append(camel_key)
        self.data[camel_key] = value

    def get_item(self, key):
        camel_key = self.to_camel_case(key)
        return self.data[camel_key]

    def del_item(self, key):
        camel_key = self.to_camel_case(key)
        if camel_key in self.data:
            del self.data[camel_key]
            self.insertion_order.remove(camel_key)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.insertion_order)

    def begin(self):
        return iter(self.insertion_order)

    def end(self):
        return iter()

# Example usage:
# cm = CamelCaseMap()
# cm.set_item("hello_world", "world")
# print(cm.get_item("hello_world"))  # Output: world
# print(len(cm))  # Output: 1