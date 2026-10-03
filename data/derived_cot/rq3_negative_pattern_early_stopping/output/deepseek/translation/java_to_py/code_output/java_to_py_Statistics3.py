import math
from collections import Counter
from typing import Optional, List, Union

class Statistics3:
    def median(self, data: List[int]) -> float:
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 1:
            return float(sorted_data[n // 2])
        else:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0

    def mode(self, data: List[int]) -> List[int]:
        counts = Counter(data)
        max_count = max(counts.values())
        return [key for key, count in counts.items() if count == max_count]

    def correlation(self, x: List[int], y: List[int]) -> Optional[float]:
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
        if denom_x == 0.0 or denom_y == 0.0:
            return None
        return numerator / math.sqrt(denom_x * denom_y)

    def mean(self, data: List[int]) -> Optional[float]:
        if len(data) == 0:
            return None
        return sum(data) / len(data)

    def correlation_matrix(self, data: List[List[int]]) -> List[List[float]]:
        num_cols = len(data[0])
        matrix = [[0.0] * num_cols for _ in range(num_cols)]
        for i in range(num_cols):
            col1 = [row[i] for row in data]
            for j in range(num_cols):
                col2 = [row[j] for row in data]
                corr = self.correlation(col1, col2)
                matrix[i][j] = corr if corr is not None else float('nan')
        return matrix

    def standard_deviation(self, data: List[int]) -> Optional[float]:
        if len(data) < 2:
            return None
        mean_val = self.mean(data)
        variance = sum((x - mean_val) ** 2 for x in data) / (len(data) - 1)
        return math.sqrt(variance)

    def z_score(self, data: List[int]) -> Optional[List[float]]:
        mean_val = self.mean(data)
        std_dev = self.standard_deviation(data)
        if mean_val is None or std_dev is None or std_dev == 0:
            return None
        return [(x - mean_val) / std_dev for x in data]