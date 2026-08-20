import math
from collections import Counter


def _std_round(x):
    """Round to the nearest integer, with halfway cases rounded away from zero.

    Mimics C++ std::round. (Python's built-in round() uses banker's rounding,
    which would produce different results for exact .5 ties.)
    NaN and infinities are propagated, as std::round does.
    """
    if math.isnan(x) or math.isinf(x):
        return x
    floor_x = math.floor(x)
    frac = x - floor_x
    if frac > 0.5 or (frac == 0.5 and x > 0):
        return floor_x + 1
    return floor_x


class DataStatistics:
    def mean(self, data: list) -> float:
        if not data:
            raise ValueError("Data vector is empty.")
        # Left-to-right accumulation from 0.0, matching
        # std::accumulate(data.begin(), data.end(), 0.0) exactly
        # (built-in sum() may use compensated summation on newer Pythons).
        total = 0.0
        for value in data:
            total += value
        return _std_round(total / len(data) * 100) / 100

    def median(self, data: list) -> float:
        if not data:
            raise ValueError("Data vector is empty.")
        data = sorted(data)  # sorted copy, like the by-value C++ parameter
        n = len(data)
        if n % 2 == 0:
            return _std_round((data[n // 2 - 1] + data[n // 2]) / 2 * 100) / 100
        else:
            return data[n // 2]

    def mode(self, data: list) -> list:
        if not data:
            raise ValueError("Data vector is empty.")
        counts = Counter(data)
        max_count = max(counts.values())
        # std::map iterates in ascending key order, so return keys sorted.
        return sorted(num for num, count in counts.items() if count == max_count)