import math


class CombinationCalculator:
    def __init__(self, datas):
        self.datas = list(datas)

    @staticmethod
    def count(n, m):
        if m == 0 or n == m:
            return 1
        return int(math.gamma(n + 1) / (math.gamma(m + 1) * math.gamma(n - m + 1)))

    @staticmethod
    def count_all(n):
        if n < 0:
            return float('nan')
        if n > 63:
            return float('inf')
        return float((1 << n) - 1) if n != 63 else float('inf')

    def select(self, m):
        result = []
        if m < 0 or m > len(self.datas):
            return result
        result_list = [''] * m
        self._select(0, result_list, 0, result)
        return result

    def select_all(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

    def _select(self, data_index, result_list, result_index, result):
        if result_index == len(result_list):
            result.append(result_list.copy())
            return
        for i in range(data_index, len(self.datas) - (len(result_list) - result_index) + 1):
            result_list[result_index] = self.datas[i]
            self._select(i + 1, result_list, result_index + 1, result)