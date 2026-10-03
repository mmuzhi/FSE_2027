from typing import Any, List, Optional

class ArrangementCalculator:
    def __init__(self, datas: List[Any]) -> None:
        self.datas = datas

    @staticmethod
    def factorial(n: int) -> int:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def count(n: int, m: Optional[int]) -> int:
        if m is None or n == m:
            return ArrangementCalculator.factorial(n)
        else:
            return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def countAll(n: int) -> int:
        total = 0
        for i in range(1, n + 1):
            total += ArrangementCalculator.count(n, i)
        return total

    def select(self, m: Optional[int]) -> List[List[Any]]:
        if m is None:
            m = len(self.datas)
        result = []
        ArrangementCalculator.selectPermutations([], self.datas[:], m, result)
        return result

    def selectAll(self) -> List[List[Any]]:
        result = []
        n = len(self.datas)
        for i in range(1, n + 1):
            result.extend(self.select(i))
        return result

    @staticmethod
    def selectPermutations(prefix, remaining, m, result):
        if len(prefix) == m:
            result.append(prefix[:])
            return
        for i in range(len(remaining)):
            newPrefix = prefix + [remaining[i]]
            newRemaining = remaining[:]
            newRemaining.pop(i)
            ArrangementCalculator.selectPermutations(newPrefix, newRemaining, m, result)