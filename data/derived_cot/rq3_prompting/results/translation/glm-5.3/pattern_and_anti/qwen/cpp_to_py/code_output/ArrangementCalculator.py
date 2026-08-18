from typing import List


class ArrangementCalculator:
    def __init__(self, datas: List[str]) -> None:
        self.datas = list(datas)

    @staticmethod
    def count(n: int, m: int = -1) -> int:
        if m == -1 or n == m:
            return ArrangementCalculator.factorial(n)
        else:
            return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def count_all(n: int) -> int:
        total = 0
        for i in range(1, n + 1):
            total += ArrangementCalculator.count(n, i)
        return total

    def _permutations_recursive(self, current: List[str], remaining: List[str], m: int,
                                result: List[List[str]]) -> None:
        if len(current) == m:
            result.append(list(current))
        else:
            for i in range(len(remaining)):
                new_current = current + [remaining[i]]
                new_remaining = remaining[:i] + remaining[i + 1:]
                self._permutations_recursive(new_current, new_remaining, m, result)

    def select(self, m: int = -1) -> List[List[str]]:
        result: List[List[str]] = []
        if m == -1:
            m = len(self.datas)

        current: List[str] = []
        remaining = list(self.datas)

        self._permutations_recursive(current, remaining, m, result)

        return result

    def select_all(self) -> List[List[str]]:
        result: List[List[str]] = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

    @staticmethod
    def factorial(n: int) -> int:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result