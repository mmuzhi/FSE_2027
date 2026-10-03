import math

pai = 3.141592653589793


class DataStatistics4:
    @staticmethod
    def correlation_coefficient(data1, data2):
        n = len(data1)
        mean1 = 0.0
        mean2 = 0.0

        for i in range(n):
            mean1 += data1[i]
            mean2 += data2[i]
        mean1 /= n
        mean2 /= n

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
        return (numerator / denominator) if denominator != 0 else 0

    @staticmethod
    def skewness(data):
        n = len(data)
        mean = 0.0

        for x in data:
            mean += x
        mean /= n

        variance = 0.0
        for x in data:
            variance += (x - mean) * (x - mean)
        variance /= n

        std_deviation = math.sqrt(variance)

        if std_deviation == 0:
            return 0.0

        skew = 0.0
        for x in data:
            skew += math.pow((x - mean), 3)

        skew *= n / ((n - 1) * (n - 2) * math.pow(std_deviation, 3))
        return skew

    @staticmethod
    def kurtosis(data):
        n = len(data)
        mean = 0.0

        for x in data:
            mean += x
        mean /= n

        variance = 0.0
        for x in data:
            variance += (x - mean) * (x - mean)
        variance /= n

        std_dev = math.sqrt(variance)

        if std_dev == 0:
            return float('nan')

        fourth_moment = 0.0
        for x in data:
            fourth_moment += math.pow((x - mean), 4)
        fourth_moment /= n

        kurtosis_value = (fourth_moment / math.pow(std_dev, 4)) - 3.0
        return kurtosis_value

    @staticmethod
    def pdf(data, mu, sigma):
        pdf_values = []

        for x in data:
            value = (1 / (sigma * math.sqrt(2 * pai))) * math.exp(-0.5 * math.pow((x - mu) / sigma, 2))
            pdf_values.append(value)

        return pdf_values