import math


def _div(dividend, divisor):
    """IEEE-754 division with Java semantics (zero divisor yields inf/nan, never raises)."""
    if divisor != 0.0:
        return dividend / divisor
    if dividend == 0.0 or math.isnan(dividend):
        return float('nan')
    sign = math.copysign(1.0, dividend) * math.copysign(1.0, divisor)
    return float('inf') if sign > 0 else float('-inf')


def _mean(data):
    """Average of a list; 0.0 for empty (mirrors Java's average().orElse(0))."""
    return sum(data) / len(data) if data else 0.0


def correlation_coefficient(data1, data2):
    n = len(data1)
    mean1 = _mean(data1)
    mean2 = _mean(data2)

    numerator = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n))

    denominator = (math.sqrt(sum((x - mean1) * (x - mean1) for x in data1))
                   * math.sqrt(sum((x - mean2) * (x - mean2) for x in data2)))

    return numerator / denominator if denominator != 0 else 0.0


def skewness(data):
    n = len(data)
    mean = _mean(data)
    variance = _mean([(x - mean) * (x - mean) for x in data])
    std_deviation = math.sqrt(variance)

    if std_deviation == 0:
        return 0.0

    total = sum((x - mean) * (x - mean) * (x - mean) for x in data)
    return _div(total * n, (n - 1) * (n - 2) * math.pow(std_deviation, 3))


def kurtosis(data):
    n = len(data)
    mean = _mean(data)
    std_dev = math.sqrt(_mean([(x - mean) * (x - mean) for x in data]))

    if std_dev == 0:
        return float('nan')

    centered_data = [x - mean for x in data]

    fourth_moment = _mean([math.pow(x, 4) for x in centered_data])

    return _div(fourth_moment, math.pow(std_dev, 4)) - 3


def pdf(data, mu, sigma):
    coeff = _div(1, sigma * math.sqrt(2 * math.pi))
    return [coeff * math.exp(-0.5 * math.pow(_div(x - mu, sigma), 2))
            for x in data]