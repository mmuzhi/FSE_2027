class AvgPartition:
    def __init__(self, lst, limit):
        self.lst = lst
        self.limit = limit

    def set_num(self):
        size = len(self.lst) // self.limit
        remainder = len(self.lst) % self.limit
        return (size, remainder)

    def get(self, index):
        size, rem = self.set_num()
        start = index * size + min(index, rem)
        end = start + size
        if index < rem:
            end += 1
        return self.lst[start:end]