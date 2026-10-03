class AvgPartition:
    def __init__(self, lst, limit):
        self.lst = lst
        self.limit = limit

    def set_num(self):
        size = len(self.lst) // self.limit
        remainder = len(self.lst) % self.limit
        return (size, remainder)

    def get(self, index):
        size, remainder = self.set_num()
        start = index * size + min(index, remainder)
        end = start + size
        if index + 1 <= remainder:
            end += 1
        if start < 0 or end > len(self.lst):
            raise IndexError
        return self.lst[start:end]

if __name__ == '__main__':
    lst = [1, 2, 3, 4]
    a = AvgPartition(lst, 2)
    print(a.get(0))
    print(a.get(1))