class CombinationCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def count(n, m):
        if m == 0 or n == m:
            return 1
        return CombinationCalculator.factorial(n) // (CombinationCalculator.factorial(n - m) * CombinationCalculator.factorial(m))

    @staticmethod
    def factorial(x):
        result = 1
        for i in range(1, x + 1):
            result *= i
        return result

    @staticmethod
    def countAll(n):
        if n < 0 or n > 63:
            return float('nan')
        return float('inf') if n == 63 else (1 << n) - 1

    def select(self, m):
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
        
        max_index = len(self.datas) - (m - resultIndex)
        for i in range(dataIndex, max_index + 1):
            resultList.insert(resultIndex, self.datas[i])
            self._select(i + 1, resultList, resultIndex + 1, result, m)
            resultList.pop(resultIndex)