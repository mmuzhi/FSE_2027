import math

class DataStatistics4:
    @staticmethod
    def correlation_coefficient(data1, data2):
        n = len(data1)
        if n == 0:
            return 0.0
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n
        numerator = 0.0
        denominator1 = 0.0
        denominator2 = 0.0
        for i in range(n):
            diff1 = data1[i] - mean1
            diff2 = data2[i] - mean2
            numerator += diff1 * diff2
            denominator1 += diff1 * diff1
            denominator2 += diff2 * diff2
        denominator = math.sqrt(denominator1) * math.sqrt(denominator2)
        if denominator != 0:
            return numerator / denominator
        return 0.0

    @staticmethod
    def skewness(data):
        n = len(data)
        if n == 0:
            return 0.0
        mean = sum(data) / n
        variance = 0.0
        for x in data:
            variance += (x - mean) * (x - mean)
        variance /= n
        std_deviation = math.sqrt(variance)
        if std_deviation == 0:
            return 0.0
        skewness = 0.0
        for x in data:
            skewness += (x - mean) ** 3
        denominator = (n - 1) * (n - 2) * (std_deviation ** 3)
        if denominator == 0:
            factor = float('inf')
        else:
            factor = n / denominator
        skewness *= factor
        return skewness

    @staticmethod
    def kurtosis(data):
        n = len(data)
        if n == 0:
            return float('nan')
        mean = sum(data) / n
        variance = 0.0
        for x in data:
            variance += (x - mean) * (x - mean)
        variance /= n
        std_dev = math.sqrt(variance)
        if std_dev == 0:
            return float('nan')
        fourth_moment = 0.0
        for x in data:
            fourth_moment += (x - mean) ** 4
        fourth_moment /= n
        denominator_kurt = std_dev ** 4
        if denominator_kurt == 0:
            if fourth_moment > 0:
                ratio = float('inf')
            elif fourth_moment < 0:
                ratio = float('-inf')
            else:
                ratio = float('nan')
        else:
            ratio = fourth_moment / denominator_kurt
        return ratio - 3.0

    @staticmethod
    def pdf(data, mu, sigma):
        if sigma == 0:
            return [float('nan') for _ in data]
        coefficient = 1.0 / (sigma * math.sqrt(2 * math.pi))
        result = []
        for x in data:
            result.append(coefficient * math.exp(-0.5 * ((x - mu) / sigma) ** 2))
        return result