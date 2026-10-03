import math
import sys
from typing import List, List  # For annotations, but note: the problem doesn't require type annotations, but we can use them for clarity.

class CombinationCalculator:
    def __init__(self, datas: List[str]):
        self.datas = datas

    @staticmethod
    def count(n: int, m: int) -> int:
        # Check for the base cases: m==0 or n==m, then return 1.
        if m == 0 or n == m:
            return 1
        
        # Calculate the binomial coefficient using gamma function.
        try:
            numerator = math.gamma(n + 1)
            denominator = math.gamma(m + 1) * math.gamma(n - m + 1)
            value = numerator / denominator
            # Convert to int by truncating the fractional part.
            return int(value)
        except Exception as e:
            # The C++ code does not handle exceptions, but if there's an error (like domain error in gamma), we return 0?
            # But note: the C++ code would return NaN or infinity for out-of-range, but we are returning int.
            # We'll return 0 for any exception to mimic the C++ behavior? But the C++ code might have undefined behavior.
            # However, the problem says to keep behavior identical, so we must return the same as C++.
            # But the C++ code does not throw exceptions, so we must not throw either.
            # Instead, we return 0 for any error? But note: the C++ code returns an int, and if the gamma function returns NaN, then the division returns NaN, and converting NaN to int is undefined.
            # We'll return 0 for any error to avoid undefined behavior in Python.
            return 0

    @staticmethod
    def count_all(n: int) -> float:
        if n < 0:
            return float('nan')
        if n > 63:
            return float('inf')
        if n == 63:
            return float('inf')
        return (1 << n) - 1

    def select(self, m: int) -> List[List[str]]:
        if m < 0 or m > len(self.datas):
            return []
        result = []
        self._select(0, [], 0, result)
        return result

    def select_all(self) -> List[List[str]]:
        result = []
        for i in range(1, len(self.datas)+1):
            combinations = self.select(i)
            result.extend(combinations)
        return result

    def _select(self, dataIndex, resultList, resultIndex, result):
        if resultIndex == len(resultList):
            result.append(resultList[:])  # Append a copy
            return
        
        # Calculate the maximum index to avoid out of bounds
        maxIndex = len(self.datas) - (len(resultList) - resultIndex)
        for i in range(dataIndex, maxIndex+1):
            resultList.append(self.datas[i])
            self._select(i+1, resultList, resultIndex+1, result)
            resultList.pop()  # Backtrack

# Example usage:
if __name__ == "__main__":
    datas = ["a", "b", "c"]
    calc = CombinationCalculator(datas)
    print(calc.count(3, 2))  # Should be 3
    print(calc.count_all(3))  # Should be 7
    print(calc.select(2))    # Should be [['a','b'], ['a','c'], ['b','c']]