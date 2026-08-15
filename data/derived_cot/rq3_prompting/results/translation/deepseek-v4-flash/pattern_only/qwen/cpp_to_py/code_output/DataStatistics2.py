import math

class DataStatistics2:
    def __init__(self, data):
        self.data = list(data)

    def get_sum(self):
        return sum(self.data)

    def get_min(self):
        return min(self.data)

    def get_max(self):
        return max(self.data)

    def get_variance(self):
        if not self.data:
            return float('nan')

        mean = self.get_sum() / len(self.data)
        variance = 0.0
        for value in self.data:
            variance += math.pow(value - mean, 2)
        variance /= len(self.data)

        return _round_2(variance)

    def get_std_deviation(self):
        variance = self.get_variance()
        std_dev = math.sqrt(variance)
        return _round_2(std_dev)

    def get_correlation(self):
        if len(self.data) < 2:
            return 1.0

        mean = self.get_sum() / len(self.data)
        sum_prod = 0.0
        sum_sq = 0.0
        for value in self.data:
            sum_prod += (value - mean) * (value - mean)
            sum_sq += (value - mean) * (value - mean)

        if sum_sq == 0.0:
            return float('nan')

        return sum_prod / sum_sq


def _round_2(x):
    if math.isnan(x) or math.isinf(x):
        return x

    scaled = x * 100
    if math.isinf(scaled):
        return scaled / 100.0

    return math.floor(scaled + 0.5) / 100.0