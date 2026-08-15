import math
from collections import Counter


class DataStatistics:

    def mean(self, data):
        total = sum(data)
        return self._java_round((total / len(data)) * 100.0) / 100.0

    def median(self, data):
        sorted_data = sorted(data)
        n = len(sorted_data)

        if n % 2 == 0:
            middle = n // 2
            return self._java_round(((sorted_data[middle - 1] + sorted_data[middle]) / 2.0) * 100.0) / 100.0
        else:
            middle = n // 2
            return float(sorted_data[middle])

    def mode(self, data):
        frequency_map = Counter(data)
        max_count = max(frequency_map.values())

        return sorted([key for key, value in frequency_map.items() if value == max_count])

    @staticmethod
    def _java_round(x):
        return math.floor(x + 0.5)