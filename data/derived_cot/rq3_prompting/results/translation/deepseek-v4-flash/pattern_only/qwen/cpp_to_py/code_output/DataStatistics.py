import math

def _round_cpp(x):
    if x >= 0:
        return math.floor(x + 0.5)
    else:
        return math.ceil(x - 0.5)

class DataStatistics:
    def mean(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        total = sum(data)
        return _round_cpp(total / len(data) * 100) / 100

    def median(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return _round_cpp(((sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2) * 100) / 100
        else:
            return float(sorted_data[n // 2])

    def mode(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        count_map = {}
        for num in data:
            count_map[num] = count_map.get(num, 0) + 1
        max_count = max(count_map.values())
        return [num for num in sorted(count_map) if count_map[num] == max_count]