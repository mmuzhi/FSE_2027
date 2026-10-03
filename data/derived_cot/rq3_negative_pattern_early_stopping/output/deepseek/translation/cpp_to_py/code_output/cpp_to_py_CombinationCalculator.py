import math
import sys

class CombinationCalculator:
    def __init__(self, datas):
        self.datas = list(datas)

    @staticmethod
    def count(n, m):
        if m == 0 or n == m:
            return 1
        return math.comb(n, m)

    @staticmethod
    def count_all(n):
        if n < 0:
            return float('nan')
        if n > 63:
            return float('inf')
        if n == 63:
            return float('inf')
        return (1 << n) - 1

    def select(self, m):
        result = []
        if m < 0 or m > len(self.datas):
            return result
        resultList = [''] * m
        self._select(0, resultList, 0, result)
        return result

    def select_all(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            combinations = self.select(i)
            result.extend(combinations)
        return result

    def _select(self, dataIndex, resultList, resultIndex, result):
        if resultIndex == len(resultList):
            result.append(resultList.copy())
            return
        for i in range(dataIndex, len(self.datas) - (len(resultList) - resultIndex) + 1):
            resultList[resultIndex] = self.datas[i]
            self._select(i + 1, resultList, resultIndex + 1, result)