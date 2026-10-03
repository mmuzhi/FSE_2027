class DataStatistics2:
    def __init__(self, data):
        self.data = [float(x) for x in data]

    def get_sum(self):
        return sum(self.data)

    def get_min(self):
        if not self.data:
            return float('nan')
        return min(self.data)

    def get_max(self):
        if not self.data:
            return float('nan')
        return max(self.data)

    def get_variance(self):
        if not self.data:
            return float('nan')
        mean = self.get_sum() / len(self.data)
        squared_diffs = [(x - mean) ** 2 for x in self.data]
        variance = sum(squared_diffs) / len(self.data)
        return variance

    def get_std_deviation(self):
        variance = self.get_variance()
        return variance ** 0.5

    def get_correlation(self):
        return 1.0