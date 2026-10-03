import numpy as np

class KappaCalculator:
    @staticmethod
    def kappa(testData, k):
        dataMat = np.array(testData, dtype=float)

        P0 = 0.0
        for i in range(k):
            P0 += dataMat[i, i]

        xsum = np.sum(dataMat, axis=1)  # Equivalent to rowwise().sum()
        ysum = np.sum(dataMat, axis=0)  # Equivalent to colwise().sum()
        
        total_sum = np.sum(dataMat)

        Pe = np.dot(ysum, xsum) / (total_sum * total_sum)
        P0 /= total_sum

        cohens_coefficient = (P0 - Pe) / (1 - Pe)
        return cohens_coefficient

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        dataMat = np.array(testData, dtype=float)

        total_sum = np.sum(dataMat)

        P0 = 0.0
        for i in range(N):
            temp = np.sum(dataMat[i, :] ** 2)
            temp -= n
            temp /= (n - 1) * n
            P0 += temp

        P0 /= N

        ysum = np.sum(dataMat, axis=0)  # colwise().sum()
        ysum = ysum / total_sum          # ysum.array() / sum
        ysum = ysum ** 2                 # ysum.array().square()

        Pe = np.sum(ysum)

        ans = (P0 - Pe) / (1 - Pe)
        return ans