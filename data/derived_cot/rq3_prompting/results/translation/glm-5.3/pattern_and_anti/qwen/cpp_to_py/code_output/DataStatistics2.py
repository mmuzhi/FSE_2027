import math


class DataStatistics2:
    def __init__(self, data):
        # C++ copies the vector; keep the same copy semantics
        self.data = list(data)

    def get_sum(self):
        return sum(self.data)

    def get_min(self):
        return min(self.data)

    def get_max(self):
        return max(self.data)

    def get_variance(self):
        n = len(self.data)
        mean = self.get_sum() / n
        variance = 0.0
        for value in self.data:
            variance += (value - mean) ** 2
        variance /= n
        return self._round2(variance)

    def get_std_deviation(self):
        variance = self.get_variance()
        std_dev = math.sqrt(variance)
        return self._round2(std_dev)

    def get_correlation(self):
        if len(self.data) < 2:
            return 1.0
        mean = self.get_sum() / len(self.data)
        sum_prod = 0.0
        sum_sq = 0.0
        for value in self.data:
            sum_prod += (value - mean) * (value - mean)
            sum_sq += (value - mean) * (value - mean)
        try:
            return sum_prod / sum_sq
        except ZeroDivisionError:
            # C++ 0.0/0.0 yields NaN rather than an exception
            return float('nan')

    @staticmethod
    def _round2(x):
        # std::round: half away from zero (Python round() is banker's rounding)
        y = x * 100.0
        r = math.floor(y + 0.5) if y >= 0 else math.ceil(y - 0.5)
        return r / 100.0