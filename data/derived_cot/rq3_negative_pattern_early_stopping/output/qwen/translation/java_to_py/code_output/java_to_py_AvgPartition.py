class AvgPartition:
    def __init__(self, lst, limit):
        self.lst = lst
        self.limit = limit

    def setNum(self):
        total = len(self.lst)
        base_size = total // self.limit
        remainder = total % self.limit
        return (base_size, remainder)

    def get(self, index):
        base_size, remainder = self.setNum()
        start = index * base_size + min(index, remainder)
        end = start + base_size
        if index < remainder:
            end += 1
        return self.lst[start:end]

if __name__ == '__main__':
    lst = [1, 2, 3, 4]
    a = AvgPartition(lst, 2)
    print(a.get(0))
    print(a.get(1))