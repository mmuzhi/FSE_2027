import math


class Statistics3:

    def median(self, data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 1:
            return float(sorted_data[n // 2])
        else:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0

    def mode(self, data):
        counts = {}
        for e in data:
            counts[e] = counts.get(e, 0) + 1
        max_count = max(counts.values())
        return [key for key, value in counts.items() if value == max_count]

    def correlation(self, x, y):
        if len(x) != len(y) or len(x) == 0:
            return None

        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)

        numerator = 0.0
        denom_x = 0.0
        denom_y = 0.0

        for i in range(len(x)):
            diff_x = x[i] - mean_x
            diff_y = y[i] - mean_y
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

    def correlation_matrix(self, data):
        num_cols = len(data[0])
        matrix = [[0.0] * num_cols for _ in range(num_cols)]

        for i in range(num_cols):
            for j in range(num_cols):
                column1 = [row[i] for row in data]
                column2 = [row[j] for row in data]
                corr = self.correlation(column1, column2)
                matrix[i][j] = corr if corr is not None else float('nan')

        return matrix

    def standard_deviation(self, data):
        if len(data) < 2:
            return None
        m = self.mean(data)
        variance = sum(math.pow(x - m, 2) for x in data) / (len(data) - 1)
        return math.sqrt(variance)

    def z_score(self, data):
        m = self.mean(data)
        std_deviation = self.standard_deviation(data)
        if m is None or std_deviation is None or std_deviation == 0:
            return None
        return [(x - m) / std_deviation for x in data]