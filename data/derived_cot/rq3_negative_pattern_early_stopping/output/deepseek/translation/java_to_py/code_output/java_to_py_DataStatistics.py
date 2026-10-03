import math
from collections import Counter
from typing import List


class DataStatistics:
    def mean(self, data: List[int]) -> float:
        """Compute the arithmetic mean, rounded to 2 decimal places (half-up)."""
        total = sum(data)
        n = len(data)
        raw_mean = total / n
        rounded = math.floor(raw_mean * 100 + 0.5) / 100.0
        return rounded

    def median(self, data: List[int]) -> float:
        """Compute the median, rounded to 2 decimal places (half-up) for even length."""
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            middle = n // 2
            avg = (sorted_data[middle - 1] + sorted_data[middle]) / 2.0
            rounded = math.floor(avg * 100 + 0.5) / 100.0
            return rounded
        else:
            return float(sorted_data[n // 2])

    def mode(self, data: List[int]) -> List[int]:
        """Return the most frequent value(s), sorted ascending."""
        frequency = Counter(data)
        max_count = max(frequency.values())
        modes = sorted([key for key, cnt in frequency.items() if cnt == max_count])
        return modes