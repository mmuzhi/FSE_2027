import math

class DataStatistics2:
    def __init__(self, data):
        self.data = [float(x) for x in data]

    def getSum(self):
        return sum(self.data, 0.0)

    def getMin(self):
        if not self.data:
            return float('nan')
        return min(self.data)

    def getMax(self):
        if not self.data:
            return float('nan')
        return max(self.data)

    def getVariance(self):
        n = len(self.data)
        if n == 0:
            return float('nan')
        mean = self.getSum() / n
        return sum((x - mean) ** 2 for x in self.data) / n

    def getStdDeviation(self):
        return math.sqrt(self.getVariance())

    def getCorrelation(self):
        return 1.0