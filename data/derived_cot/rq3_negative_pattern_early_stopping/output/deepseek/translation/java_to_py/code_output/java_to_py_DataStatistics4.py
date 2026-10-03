import math
from typing import List

def correlation_coefficient(data1: List[float], data2: List[float]) -> float:
    n = len(data1)
    mean1 = sum(data1) / n if n > 0 else 0.0
    mean2 = sum(data2) / n if n > 0 else 0.0

    numerator = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n))

    sum_sq1 = sum((x - mean1) ** 2 for x in data1)
    sum_sq2 = sum((x - mean2) ** 2 for x in data2)
    denominator = math.sqrt(sum_sq1) * math.sqrt(sum_sq2)

    return numerator / denominator if denominator != 0 else 0.0

def skewness(data: List[float]) -> float:
    n = len(data)
    if n == 0:
        return 0.0
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return 0.0

    skew = sum((x - mean) ** 3 for x in data) * n / ((n - 1) * (n - 2) * (std_dev ** 3))
    return skew

def kurtosis(data: List[float]) -> float:
    n = len(data)
    if n == 0:
        return float('nan')
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return float('nan')

    fourth_moment = sum((x - mean) ** 4 for x in data) / n
    kurt = fourth_moment / (std_dev ** 4) - 3.0
    return kurt

def pdf(data: List[float], mu: float, sigma: float) -> List[float]:
    coeff = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
    return [coeff * math.exp(-0.5 * ((x - mu) / sigma) ** 2) for x in data]