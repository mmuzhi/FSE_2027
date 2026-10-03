import math
from typing import List

def correlation_coefficient(data1: List[float], data2: List[float]) -> float:
    n = len(data1)
    if n == 0:
        return 0.0
    
    mean1 = sum(data1) / n
    mean2 = sum(data2) / n

    numerator = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n))
    
    ssd1 = sum((x - mean1) ** 2 for x in data1)
    ssd2 = sum((x - mean2) ** 2 for x in data2)
    denominator = math.sqrt(ssd1) * math.sqrt(ssd2)
    
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
    
    sum_cubed_deviations = sum((x - mean) ** 3 for x in data)
    skewness = sum_cubed_deviations * n / ((n - 1) * (n - 2) * std_dev ** 3)
    return skewness

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
    kurtosis_value = (fourth_moment / (std_dev ** 4)) - 3
    return kurtosis_value

def pdf(data: List[float], mu: float, sigma: float) -> List[float]:
    return [
        (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)
        for x in data
    ]