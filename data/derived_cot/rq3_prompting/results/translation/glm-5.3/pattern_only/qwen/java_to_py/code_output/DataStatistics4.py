import math


class DataStatistics4:

    @staticmethod
    def _average(values):
        # Mirrors Java's stream.average().orElse(0)
        return sum(values) / len(values) if values else 0.0

    @staticmethod
    def correlationCoefficient(data1, data2):
        n = len(data1)
        mean1 = DataStatistics4._average(data1)
        mean2 = DataStatistics4._average(data2)

        numerator = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n))

        denominator = (math.sqrt(sum((x - mean1) * (x - mean1) for x in data1))
                       * math.sqrt(sum((x - mean2) * (x - mean2) for x in data2)))

        return numerator / denominator if denominator != 0 else 0.0

    @staticmethod
    def skewness(data):
        n = len(data)
        mean = DataStatistics4._average(data)
        variance = DataStatistics4._average([(x - mean) * (x - mean) for x in data])
        std_deviation = math.sqrt(variance)

        if std_deviation == 0:
            return 0.0

        numerator = sum((x - mean) * (x - mean) * (x - mean) for x in data) * n
        denominator = (n - 1) * (n - 2) * math.pow(std_deviation, 3)

        if denominator == 0:
            # Java double division by zero yields NaN / ±Infinity instead of raising
            if numerator == 0:
                return float('nan')
            return float('inf') if numerator > 0 else float('-inf')

        return numerator / denominator

    @staticmethod
    def kurtosis(data):
        n = len(data)
        mean = DataStatistics4._average(data)
        std_dev = math.sqrt(DataStatistics4._average([(x - mean) * (x - mean) for x in data]))

        if std_dev == 0:
            return float('nan')

        centered_data = [x - mean for x in data]
        fourth_moment = DataStatistics4._average([math.pow(x, 4) for x in centered_data])

        return fourth_moment / math.pow(std_dev, 4) - 3

    @staticmethod
    def pdf(data, mu, sigma):
        return [(1 / (sigma * math.sqrt(2 * math.pi)))
                * math.exp(-0.5 * math.pow((x - mu) / sigma, 2)) for x in data]