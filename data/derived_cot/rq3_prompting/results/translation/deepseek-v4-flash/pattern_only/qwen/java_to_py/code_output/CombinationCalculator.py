class CombinationCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def _to_int32(x):
        x &= 0xFFFFFFFF
        if x >= 0x80000000:
            x -= 0x100000000
        return x

    @staticmethod
    def _int_div(a, b):
        if b == 0:
            raise ZeroDivisionError("division by zero")
        q = abs(a) // abs(b)
        if (a < 0) ^ (b < 0):
            q = -q
        return CombinationCalculator._to_int32(q)

    @staticmethod
    def _factorial(x):
        result = 1
        for i in range(1, x + 1):
            result = CombinationCalculator._to_int32(result * i)
        return result

    @staticmethod
    def count(n, m):
        if m == 0 or n == m:
            return 1
        numerator = CombinationCalculator._factorial(n)
        denominator = CombinationCalculator._to_int32(
            CombinationCalculator._factorial(n - m) * CombinationCalculator._factorial(m)
        )
        return CombinationCalculator._int_div(numerator, denominator)

    @staticmethod
    def countAll(n):
        if n < 0 or n > 63:
            return float('nan')
        if n == 63:
            return float('inf')
        return float((1 << (n & 31)) - 1)

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
            resultList.append(self.datas[i])
            self._select(i + 1, resultList, resultIndex + 1, result, m)
            resultList.pop()