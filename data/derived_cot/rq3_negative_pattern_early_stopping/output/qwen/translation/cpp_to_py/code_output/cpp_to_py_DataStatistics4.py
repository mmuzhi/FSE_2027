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
        return numerator / denominator if denominator != 0 else 0.0

    @staticmethod
    def skewness(data):
        n = len(data)
        if n == 0:
            return 0.0
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        std_deviation = math.sqrt(variance)

        if std_deviation == 0:
            return 0.0

        sum_cubed = sum((x - mean) ** 3 for x in data)
        skewness_value = (n / ((n - 1) * (n - 2))) * (sum_cubed / (std_deviation ** 3))
        return skewness_value

    @staticmethod
    def kurtosis(data):
        n = len(data)
        if n == 0:
            return float('nan')
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)

        if std_dev == 0:
            return float('nan')

        fourth_moment = sum((x - mean) ** 4 for x in data) / n
        kurtosis_value = (fourth_moment / (std_dev ** 4)) - 3.0
        return kurtosis_value

    @staticmethod
    def pdf(data, mu, sigma):
        pdf_values = []
        for x in data:
            if sigma <= 0:
                pdf_values.append(0.0)
            else:
                coefficient = 1.0 / (sigma * math.sqrt(2 * math.pi))
                exponent = -0.5 * ((x - mu) / sigma) ** 2
                pdf_values.append(coefficient * math.exp(exponent))
        return pdf_values