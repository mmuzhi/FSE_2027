import math
from typing import List, Union, Dict, Any
from collections import Counter

class Statistics3:
    @staticmethod
    def median(data: List[int]) -> float:
        if not data:
            return float('nan')
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 1:
            return sorted_data[mid]
        else:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0

    @staticmethod
    def mode(data: List[int]) -> List[int]:
        if not data:
            return []
        counts = Counter(data)
        max_count = max(counts.values())
        return [num for num, count in counts.items() if count == max_count]

    @staticmethod
    def correlation(x: List[int], y: List[int]) -> float:
        if len(x) != len(y):
            raise ValueError("Vectors must be of the same length")
        n = len(x)
        if n < 1:
            return float('nan')
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
    def correlation_matrix(data: List[List[int]]) -> List[List[float]]:
        num_rows = len(data)
        if num_rows == 0:
            return []
        num_cols = len(data[0])
        matrix = [[0.0] * num_cols for _ in range(num_cols)]
        for i in range(num_cols):
            col_i = [data[k][i] for k in range(num_rows)]
            for j in range(num_cols):
                col_j = [data[k][j] for k in range(num_rows)]
                matrix[i][j] = Statistics3.correlation(col_i, col_j)
        return matrix

    @staticmethod
    def mean(data: List[int]) -> float:
        if not data:
            return float('nan')
        return sum(data) / len(data)

    @staticmethod
    def standard_deviation(data: List[int]) -> float:
        n = len(data)
        if n < 2:
            return float('nan')
        mean_val = Statistics3.mean(data)
        variance_sum = 0.0
        for x in data:
            diff = x - mean_val
            variance_sum += diff * diff
        variance = variance_sum / (n - 1)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data: List[int]) -> List[float]:
        n = len(data)
        if n < 1:
            return [float('nan')] * n
        mean_val = Statistics3.mean(data)
        std_dev = Statistics3.standard_deviation(data)
        if std_dev == 0 or std_dev == float('nan'):
            return [float('nan')] * n
        return [(x - mean_val) / std_dev for x in data]

    @staticmethod
    def variance(data: List[int], mean_value: float) -> float:
        variance_sum = 0.0
        for x in data:
            diff = x - mean_value
            variance_sum += diff * diff
        return variance_sum / (len(data) - 1)