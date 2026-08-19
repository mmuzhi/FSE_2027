import math


def _round_half_away(x):
    # Mimics C++ std::round (round half away from zero), unlike Python's round().
    return math.copysign(math.floor(abs(x) + 0.5), x)


class DataStatistics2:
    def __init__(self, data):
        # C++ copies the vector; copy the list to preserve value semantics.
        self.data = list(data)

    def get_sum(self):
        total = 0.0
        for value in self.data:
            total += value
        return total

    def get_min(self):
        return min(self.data)

    def get_max(self):
        return max(self.data)

    def get_variance(self):
        mean = self.get_sum() / len(self.data)
        variance = 0.0
        for value in self.data:
            variance += (value - mean) ** 2
        variance /= len(self.data)
        return _round_half_away(variance * 100) / 100

    def get_std_deviation(self):
        variance = self.get_variance()
        std_dev = math.sqrt(variance)
        return _round_half_away(std_dev * 100) / 100

    def get_correlation(self):
        if len(self.data) < 2:
            return 1.0
        mean = self.get_sum() / len(self.data)
        sum_prod = 0.0
        sum_sq = 0.0
        for value in self.data:
            sum_prod += (value - mean) * (value - mean)
            sum_sq += (value - mean) * (value - mean)
        # C++ 0.0/0.0 yields NaN; Python raises ZeroDivisionError, so guard it.
        if sum_sq == 0.0:
            return float('nan')
        return sum_prod / sum_sq