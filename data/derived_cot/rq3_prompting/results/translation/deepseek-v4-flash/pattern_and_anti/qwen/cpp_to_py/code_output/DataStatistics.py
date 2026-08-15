import math


def _round_custom(x):
    # Equivalent to std::round: round half away from zero
    if x >= 0:
        return math.floor(x + 0.5)
    else:
        return math.ceil(x - 0.5)


class DataStatistics:
    def mean(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        total = sum(data)
        return _round_custom(total / len(data) * 100) / 100

    def median(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        data_sorted = sorted(data)
        n = len(data_sorted)
        if n % 2 == 0:
            return _round_custom(((data_sorted[n // 2 - 1] + data_sorted[n // 2]) / 2) * 100) / 100
        else:
            return data_sorted[n // 2]

    def mode(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        count_map = {}
        for num in data:
            count_map[num] = count_map.get(num, 0) + 1
        max_count = max(count_map.values())
        return [num for num, cnt in sorted(count_map.items()) if cnt == max_count]