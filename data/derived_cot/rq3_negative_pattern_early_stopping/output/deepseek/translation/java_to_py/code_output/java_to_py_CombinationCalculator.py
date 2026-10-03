import math
from typing import List, Optional


class CombinationCalculator:
    def __init__(self, datas: List[str]) -> None:
        self.datas = datas

    @staticmethod
    def count(n: int, m: int) -> int:
        if m == 0 or n == m:
            return 1
        return CombinationCalculator.factorial(n) // (
            CombinationCalculator.factorial(n - m) * CombinationCalculator.factorial(m)
        )

    @staticmethod
    def factorial(x: int) -> int:
        result = 1
        for i in range(1, x + 1):
            result *= i
        return result

    @staticmethod
    def countAll(n: int) -> float:
        if n < 0 or n > 63:
            return float("nan")
        if n == 63:
            return float("inf")
        return float((1 << n) - 1)

    def select(self, m: int) -> List[List[str]]:
        result: List[List[str]] = []
        self._select(0, [None] * m, 0, result, m)  # pre-allocate list of size m
        return result

    def selectAll(self) -> List[List[str]]:
        result: List[List[str]] = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

    def _select(
        self,
        dataIndex: int,
        resultList: List[str],
        resultIndex: int,
        result: List[List[str]],
        m: int,
    ) -> None:
        if resultIndex == m:
            result.append(resultList[:])  # copy the current combination
            return

        for i in range(dataIndex, len(self.datas) - (m - resultIndex) + 1):
            resultList[resultIndex] = self.datas[i]
            self._select(i + 1, resultList, resultIndex + 1, result, m)