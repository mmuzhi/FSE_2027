import math

class DataStatistics4:
    pai = 3.141592653589793

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
            variance += (x - mean) ** 2
        variance /= n

        std_deviation = math.sqrt(variance)
        if std_deviation == 0:
            return 0.0

        skewness_val = 0.0
        for x in data:
            skewness_val += (x - mean) ** 3

        skewness_val *= n / ((n - 1) * (n - 2) * (std_deviation ** 3))
        return skewness_val

    @staticmethod
    def kurtosis(data):
        n = len(data)
        mean = 0.0
        for x in data:
            mean += x
        mean /= n

        variance = 0.0
        for x in data:
            variance += (x - mean) ** 2
        variance /= n

        std_dev = math.sqrt(variance)
        if std_dev == 0:
            return float('nan')

        fourth_moment = 0.0
        for x in data:
            fourth_moment += (x - mean) ** 4
        fourth_moment /= n

        kurtosis_val = (fourth_moment / (std_dev ** 4)) - 3.0
        return kurtosis_val

    @staticmethod
    def pdf(data, mu, sigma):
        pdf_values = []
        for x in data:
            value = (1.0 / (sigma * math.sqrt(2 * DataStatistics4.pai))) * \
                    math.exp(-0.5 * ((x - mu) / sigma) ** 2)
            pdf_values.append(value)
        return pdf_values