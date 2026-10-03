import math

class Statistics3:
    @staticmethod
    def mean(data):
        if not data:
            return float('nan')
        return sum(data) / len(data)

    @staticmethod
    def _variance(data, mean_value):
        variance_sum = 0.0
        for x in data:
            diff = x - mean_value
            variance_sum += diff * diff
        return variance_sum / (len(data) - 1)

    @staticmethod
    def median(data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n == 0:
            return float('nan')
        if n % 2 == 1:
            return sorted_data[n // 2]
        else:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0

    @staticmethod
    def mode(data):
        counts = {}
        for value in data:
            counts[value] = counts.get(value, 0) + 1
        
        max_count = 0
        for count in counts.values():
            if count > max_count:
                max_count = count
                
        mode_values = []
        for value in sorted(counts.keys()):
            if counts[value] == max_count:
                mode_values.append(value)
                
        return mode_values

    @staticmethod
    def correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("Vectors must be of the same length")

        mean_x = Statistics3.mean(x)
        mean_y = Statistics3.mean(y)
        numerator = 0.0
        denominator_x = 0.0
        denominator_y = 0.0

        for i in range(n):
            diff_x = x[i] - mean_x
            diff_y = y[i] - mean_y
            numerator += diff_x * diff_y
            denominator_x += diff_x * diff_x
            denominator_y += diff_y * diff_y

        denominator = math.sqrt(denominator_x * denominator_y)
        if denominator == 0:
            return float('nan')
        return numerator / denominator

    @staticmethod
    def correlation_matrix(data):
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
        mean_value = Statistics3.mean(data)
        var = Statistics3._variance(data, mean_value)
        return math.sqrt(var)

    @staticmethod
    def z_score(data):
        mean_value = Statistics3.mean(data)
        std_deviation = Statistics3.standard_deviation(data)
        if std_deviation == 0:
            return [float('nan')] * len(data)

        z_scores = []
        for x in data:
            z_scores.append((x - mean_value) / std_deviation)
        return z_scores