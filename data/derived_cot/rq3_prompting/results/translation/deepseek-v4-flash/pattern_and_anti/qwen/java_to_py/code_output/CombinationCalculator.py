class CombinationCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def count(n, m):
        if m == 0 or n == m:
            return 1
        denom = _to_int32(_factorial(n - m) * _factorial(m))
        return _trunc_div(_factorial(n), denom)

    @staticmethod
    def countAll(n):
        if n < 0 or n > 63:
            return float('nan')
        if n == 63:
            return float('inf')
        shift = n & 31
        val = _to_int32((1 << shift) - 1)
        return float(val)

    def select(self, m):
        if m < 0:
            raise ValueError("Illegal Capacity: " + str(m))
        result = []
        self._select(0, [], 0, result, m)
        return result

    def selectAll(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

    def _select(self, dataIndex, resultList, resultIndex, result, m):
        if resultIndex == m:
            result.append(list(resultList))
            return
        for i in range(dataIndex, len(self.datas) - (m - resultIndex) + 1):
            resultList.insert(resultIndex, self.datas[i])
            self._select(i + 1, resultList, resultIndex + 1, result, m)
            resultList.pop(resultIndex)


def _to_int32(x):
    x &= 0xffffffff
    return x if x < 0x80000000 else x - 0x100000000


def _factorial(x):
    result = 1
    for i in range(1, x + 1):
        result = _to_int32(result * i)
    return result


def _trunc_div(a, b):
    if b == 0:
        raise ZeroDivisionError("/ by zero")
    q = abs(a) // abs(b)
    if (a < 0) ^ (b < 0):
        q = -q
    return _to_int32(q)