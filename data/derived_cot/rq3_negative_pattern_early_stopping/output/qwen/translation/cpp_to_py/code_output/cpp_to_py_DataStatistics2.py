class DataStatistics2:
    def __init__(self, data):
        self.data = data

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
        variance = round(variance * 100) / 100
        return variance

    def get_std_deviation(self):
        variance = self.get_variance()
        std_dev = variance ** 0.5
        std_dev = round(std_dev * 100) / 100
        return std_dev

    def get_correlation(self):
        n = len(self.data)
        if n < 2:
            return 1.0
        mean = self.get_sum() / n
        sum_prod = 0.0
        sum_sq = 0.0
        for value in self.data:
            diff = value - mean
            sum_prod += diff * diff
            sum_sq += diff * diff
        return sum_prod / sum_sq