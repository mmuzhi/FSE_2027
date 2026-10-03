import math
from typing import List, Optional, Any

def median(data: List[int]) -> float:
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0

def mode(data: List[int]) -> List[int]:
    count_dict = {}
    for num in data:
        count_dict[num] = count_dict.get(num, 0) + 1
    max_count = max(count_dict.values()) if count_dict else 0
    return [num for num, cnt in count_dict.items() if cnt == max_count]

def correlation(x: List[int], y: List[int]) -> Optional[float]:
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
        denom_x += diff_x ** 2
        denom_y += diff_y ** 2
    if denom_x == 0 or denom_y == 0:
        return None
    return numerator / math.sqrt(denom_x * denom_y)

def mean(data: List[int]) -> Optional[float]:
    if not data:
        return None
    return sum(data) / len(data)

def correlation_matrix(data: List[List[int]]) -> List[List[float]]:
    if not data or not data[0]:
        return []
    num_cols = len(data[0])
    matrix = [[0.0] * num_cols for _ in range(num_cols)]
    for i in range(num_cols):
        col_i = [row[i] for row in data]
        for j in range(num_cols):
            col_j = [row[j] for row in data]
            corr = correlation(col_i, col_j)
            matrix[i][j] = corr if corr is not None else float('nan')
    return matrix

def standard_deviation(data: List[int]) -> Optional[float]:
    if len(data) < 2:
        return None
    m = mean(data)
    variance = sum((x - m) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)

def z_score(data: List[int]) -> Optional[List[float]]:
    m = mean(data)
    std_dev = standard_deviation(data)
    if m is None or std_dev is None or std_dev == 0:
        return None
    return [(x - m) / std_dev for x in data]