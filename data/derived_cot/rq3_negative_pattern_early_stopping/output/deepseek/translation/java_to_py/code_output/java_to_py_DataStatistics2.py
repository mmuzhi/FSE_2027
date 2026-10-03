import math

class DataStatistics2:
    def __init__(self, data):
        self.data = [float(x) for x in data]

    def getSum(self):
        return sum(self.data)

    def getMin(self):
        return min(self.data, default=float('nan'))

    def getMax(self):
        return max(self.data, default=float('nan'))

    def getVariance(self):
        n = len(self.data)
        if n == 0:
            return float('nan')
        mean = self.getSum() / n
        variance = sum((x - mean) ** 2 for x in self.data) / n
        return variance

    def getStdDeviation(self):
        return math.sqrt(self.getVariance())

    def getCorrelation(self):
        return 1.0