import math


class DataStatistics4:

    @staticmethod
    def correlationCoefficient(data1, data2):
        n = len(data1)
        mean1 = sum(data1) / n if n > 0 else 0
        mean2 = sum(data2) / n if n > 0 else 0

        numerator = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n))

        denominator = (math.sqrt(sum((x - mean1) ** 2 for x in data1))
                       * math.sqrt(sum((x - mean2) ** 2 for x in data2)))

        return numerator / denominator if denominator != 0 else 0

    @staticmethod
    def skewness(data):
        n = len(data)
        mean = sum(data) / n if n > 0 else 0
        variance = sum((x - mean) ** 2 for x in data) / n if n > 0 else 0
        stdDeviation = math.sqrt(variance)

        if stdDeviation == 0:
            return 0

        skewness_val = (sum((x - mean) ** 3 for x in data)
                        * n / ((n - 1) * (n - 2) * stdDeviation ** 3))

        return skewness_val

    @staticmethod
    def kurtosis(data):
        n = len(data)
        mean = sum(data) / n if n > 0 else 0
        variance = sum((x - mean) ** 2 for x in data) / n if n > 0 else 0
        stdDev = math.sqrt(variance)

        if stdDev == 0:
            return float('nan')

        centeredData = [x - mean for x in data]

        fourthMoment = sum(x ** 4 for x in centeredData) / n if n > 0 else 0

        kurtosisValue = (fourthMoment / stdDev ** 4) - 3

        return kurtosisValue

    @staticmethod
    def pdf(data, mu, sigma):
        return [(1 / (sigma * math.sqrt(2 * math.pi)))
                * math.exp(-0.5 * ((x - mu) / sigma) ** 2)
                for x in data]