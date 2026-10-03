import math
import collections

class Statistics3:
    @staticmethod
    def median(data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n == 0:
            return float('nan')
        if n % 2 == 1:
            return float(sorted_data[n // 2])
        else:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0

    @staticmethod
    def mode(data):
        if not data:
            return []
        counts = collections.Counter(data)
        max_count = max(counts.values())
        return [key for key, val in counts.items() if val == max_count]

    @staticmethod
    def correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("Vectors must be of the same length")
        if n == 0:
            return float('nan')
        mean_x = Statistics3.mean(x)
        mean_y = Statistics3.mean(y)
        numerator = 0.0
        denominator_x = 0.0
        denominator_y = 0.0
        for xi, yi in zip(x, y):
            diff_x = xi - mean_x
            diff_y = yi - mean_y
            numerator += diff_x * diff_y
            denominator_x += diff_x * diff_x
            denominator_y += diff_y * diff_y
        denominator = math.sqrt(denominator_x * denominator_y)
        if denominator == 0:
            return float('nan')
        return numerator / denominator

    @staticmethod
    def mean(data):
        if not data:
            return float('nan')
        return sum(data) / len(data)

    @staticmethod
    def correlation_matrix(data):
        if not data or not data[0]:
            return [[]]  # consistent with behavior? Actually C++ would have data[0].size() and potentially index out of bounds. We'll handle empty rows.
        num_rows = len(data)
        num_cols = len(data[0])
        matrix = [[0.0] * num_cols for _ in range(num_cols)]
        for i in range(num_cols):
            for j in range(num_cols):
                column1 = [data[k][i] for k in range(num_rows)]
                column2 = [data[k][j] for k in range(num_rows)]
                matrix[i][j] = Statistics3.correlation(column1, column2)
        return matrix

    @staticmethod
    def standard_deviation(data):
        n = len(data)
        if n < 2:
            return float('nan')
        mean_val = Statistics3.mean(data)
        var = sum((x - mean_val) ** 2 for x in data) / (n - 1)
        return math.sqrt(var)

    @staticmethod
    def z_score(data):
        mean_val = Statistics3.mean(data)
        std_dev = Statistics3.standard_deviation(data)
        if math.isnan(std_dev) or std_dev == 0:
            return [float('nan')] * len(data)
        return [(x - mean_val) / std_dev for x in data]