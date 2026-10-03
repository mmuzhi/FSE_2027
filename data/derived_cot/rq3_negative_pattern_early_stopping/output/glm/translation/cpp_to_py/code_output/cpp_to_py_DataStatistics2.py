import math

class DataStatistics2:
    def __init__(self, data):
        self.data = list(data)

    def get_sum(self):
        return sum(self.data, 0.0)

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
            variance += (value - mean) ** 2
        variance /= len(self.data)
        if math.isnan(variance) or math.isinf(variance):
            return variance
        return math.floor(variance * 100 + 0.5) / 100.0

    def get_std_deviation(self):
        variance = self.get_variance()
        if math.isnan(variance) or math.isinf(variance):
            return variance
        std_dev = math.sqrt(variance)
        if math.isnan(std_dev) or math.isinf(std_dev):
            return std_dev
        return math.floor(std_dev * 100 + 0.5) / 100.0

    def get_correlation(self):
        if len(self.data) < 2:
            return 1.0
        mean = self.get_sum() / len(self.data)
        sum_prod = 0.0
        sum_sq = 0.0
        for value in self.data:
            diff = value - mean
            sum_prod += diff * diff
            sum_sq += diff * diff
        if sum_sq == 0.0:
            return float('nan')
        return sum_prod / sum_sq