import math
from collections import Counter


class DataStatistics:

    def mean(self, data):
        if not data:  # Java: 0.0/0 -> NaN -> Math.round(NaN) == 0
            return 0.0
        total = sum(data)
        # Java Math.round = floor(x + 0.5): half-up, not Python's banker's rounding
        return math.floor((total / len(data)) * 100.0 + 0.5) / 100.0

    def median(self, data):
        sorted_data = sorted(data)  # new list, original untouched (Arrays.copyOf + sort)
        n = len(sorted_data)

        if n % 2 == 0:
            middle = n // 2
            return math.floor(((sorted_data[middle - 1] + sorted_data[middle]) / 2.0) * 100.0 + 0.5) / 100.0
        else:
            middle = n // 2
            return float(sorted_data[middle])

    def mode(self, data):
        frequency = Counter(data)
        max_count = max(frequency.values())
        return sorted(key for key, count in frequency.items() if count == max_count)