import math

class DataStatistics2:
    def __init__(self, data):
        self._data = list(data)  # make a copy

    def get_sum(self):
        return sum(self._data)

    def get_min(self):
        return min(self._data)

    def get_max(self):
        return max(self._data)

    def _round_half_up(self, x, decimals=2):
        factor = 10 ** decimals
        if x >= 0:
            return math.floor(x * factor + 0.5) / factor
        else:
            return math.ceil(x * factor - 0.5) / factor

    def get_variance(self):
        n = len(self._data)
        if n == 0:
            return 0.0  # not specified in C++ but defensive
        mean = self.get_sum() / n
        variance = sum((x - mean) ** 2 for x in self._data) / n
        return self._round_half_up(variance)

    def get_std_deviation(self):
        variance = self.get_variance()
        std_dev = math.sqrt(variance)
        return self._round_half_up(std_dev)

    def get_correlation(self):
        n = len(self._data)
        if n < 2:
            return 1.0
        mean = self.get_sum() / n
        sum_prod = 0.0
        sum_sq = 0.0
        for x in self._data:
            diff = x - mean
            sum_prod += diff * diff
            sum_sq += diff * diff
        return sum_prod / sum_sq