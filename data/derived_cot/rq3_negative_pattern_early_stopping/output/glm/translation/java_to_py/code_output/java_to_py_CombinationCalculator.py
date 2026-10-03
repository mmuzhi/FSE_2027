class CombinationCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def count(n, m):
        if m == 0 or n == m:
            return 1
        return CombinationCalculator._factorial(n) // (CombinationCalculator._factorial(n - m) * CombinationCalculator._factorial(m))

    @staticmethod
    def _factorial(x):
        result = 1
        for i in range(1, x + 1):
            result *= i
        return result

    @staticmethod
    def countAll(n):
        if n < 0 or n > 63:
            return float('nan')
        if n != 63:
            return (1 << n) - 1
        else:
            return float('inf')

    def select(self, m):
        result = []
        self._select(0, [], 0, result, m)
        return result

    def selectAll(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

    def _select(self, data_index, result_list, result_index, result, m):
        if result_index == m:
            result.append(list(result_list))
            return

        for i in range(data_index, len(self.datas) - (m - result_index) + 1):
            result_list.insert(result_index, self.datas[i])
            self._select(i + 1, result_list, result_index + 1, result, m)
            del result_list[result_index]