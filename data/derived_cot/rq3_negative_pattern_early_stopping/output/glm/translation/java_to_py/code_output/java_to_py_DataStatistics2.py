import math

class DataStatistics2:
    def __init__(self, data):
        self.data = [float(x) for x in data]

    def get_sum(self):
        return sum(self.data, 0.0)

    def get_min(self):
        if not self.data:
            return float('nan')
        if any(math.isnan(x) for x in self.data):
            return float('nan')
        return min(self.data)

    def get_max(self):
        if not self.data:
            return float('nan')
        if any(math.isnan(x) for x in self.data):
            return float('nan')
        return max(self.data)

    def get_variance(self):
        if not self.data:
            return float('nan')
        mean = self.get_sum() / len(self.data)
        return sum((val - mean) ** 2 for val in self.data) / len(self.data)

    def get_std_deviation(self):
        return math.sqrt(self.get_variance())

    def get_correlation(self):
        return 1.0