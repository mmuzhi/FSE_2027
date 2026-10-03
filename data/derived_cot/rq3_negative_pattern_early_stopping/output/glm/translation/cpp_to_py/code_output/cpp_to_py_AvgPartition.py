class AvgPartition:
    def __init__(self, lst, limit):
        self.lst = list(lst)
        self.limit = limit

    def set_num(self):
        size = len(self.lst) // self.limit
        remainder = len(self.lst) % self.limit
        return size, remainder

    def get(self, index):
        size, remainder = self.set_num()
        start = index * size + min(index, remainder)
        end = start + size
        if index + 1 <= remainder:
            end += 1
        return self.lst[start:end]