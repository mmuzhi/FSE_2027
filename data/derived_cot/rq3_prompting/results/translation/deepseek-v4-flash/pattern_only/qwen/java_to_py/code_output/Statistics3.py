import math
from collections import Counter


class Statistics3:
    def median(self, data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n == 0:
            raise IndexError("Index -1 out of bounds for length 0")
        if n % 2 == 1:
            return float(sorted_data[n // 2])
        else:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0

    def mode(self, data):
        counts = Counter(data)
        max_count = max(counts.values())
        return [key for key, count in counts.items() if count == max_count]

    def correlation(self, x, y):
        if len(x) != len(y) or len(x) == 0:
            return None

        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)

        numerator = 0.0
        denom_x = 0.0
        denom_y = 0.0

        for xi, yi in zip(x, y):
            diff_x = xi - mean_x
            diff_y = yi - mean_y
            numerator += diff_x * diff_y
            denom_x += diff_x * diff_x
            denom_y += diff_y * diff_y

        if denom_x == 0 or denom_y == 0:
            return None

        return numerator / math.sqrt(denom_x * denom_y)

    def mean(self, data):
        if len(data) == 0:
            return None
        return sum(data) / len(data)

    def correlationMatrix(self, data):
        num_cols = len(data[0])
        matrix = [[0.0] * num_cols for _ in range(num_cols)]

        for i in range(num_cols):
            for j in range(num_cols):
                col1 = [row[i] for row in data]
                col2 = [row[j] for row in data]
                corr = self.correlation(col1, col2)
                matrix[i][j] = corr if corr is not None else float('nan')

        return matrix

    def standardDeviation(self, data):
        if len(data) < 2:
            return None
        m = self.mean(data)
        variance = sum((x - m) ** 2 for x in data) / (len(data) - 1)
        return math.sqrt(variance)

    def zScore(self, data):
        m = self.mean(data)
        std = self.standardDeviation(data)
        if m is None or std is None or std == 0:
            return None
        return [(x - m) / std for x in data]