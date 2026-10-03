import math
from collections import Counter
from typing import List

class DataStatistics:

    def mean(self, data: List[int]) -> float:
        total = sum(data)
        return math.floor((total / len(data)) * 100.0 + 0.5) / 100.0

    def median(self, data: List[int]) -> float:
        sorted_data = sorted(data)
        n = len(sorted_data)

        if n % 2 == 0:
            middle = n // 2
            return math.floor(((sorted_data[middle - 1] + sorted_data[middle]) / 2.0) * 100.0 + 0.5) / 100.0
        else:
            middle = n // 2
            return float(sorted_data[middle])

    def mode(self, data: List[int]) -> List[int]:
        frequency_map = Counter(data)
        max_count = max(frequency_map.values())
        
        return sorted([k for k, v in frequency_map.items() if v == max_count])