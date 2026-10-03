import math
from typing import List

class CombinationCalculator:
    def __init__(self, datas: List[str]):
        self.datas = datas

    @staticmethod
    def count(n: int, m: int) -> int:
        if m == 0 or n == m:
            return 1
        return math.comb(n, m)

    @staticmethod
    def count_all(n: int) -> float:
        if n < 0:
            return float('nan')
        if n > 63:
            return float('inf')
        if n == 63:
            return float('inf')
        return float((1 << n) - 1)

    def select(self, m: int) -> List[List[str]]:
        result: List[List[str]] = []
        if m < 0 or m > len(self.datas):
            return result
        result_list = [""] * m
        self._select(0, result_list, 0, result)
        return result

    def select_all(self) -> List[List[str]]:
        result: List[List[str]] = []
        for i in range(1, len(self.datas) + 1):
            combinations = self.select(i)
            result.extend(combinations)
        return result

    def _select(self, data_index: int, result_list: List[str], result_index: int, result: List[List[str]]) -> None:
        if result_index == len(result_list):
            result.append(result_list.copy())
            return

        limit = len(self.datas) - (len(result_list) - result_index)
        for i in range(data_index, limit + 1):
            result_list[result_index] = self.datas[i]
            self._select(i + 1, result_list, result_index + 1, result)