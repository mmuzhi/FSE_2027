import numpy as np


class KappaCalculator:
    @staticmethod
    def kappa(testData, k):
        rows = len(testData)
        dataMat = np.array([[testData[i][j] for j in range(k)] for i in range(rows)], dtype=float)

        P0 = 0.0
        for i in range(k):
            P0 += dataMat[i, i]

        xsum = dataMat.sum(axis=1)
        ysum = dataMat.sum(axis=0)
        total = dataMat.sum()

        Pe = np.dot(ysum, xsum) / (total * total)
        P0 /= total

        return (P0 - Pe) / (1 - Pe)

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        rows = len(testData)
        dataMat = np.array([[testData[i][j] for j in range(k)] for i in range(rows)], dtype=float)

        sum_ = 0.0
        P0 = 0.0

        for i in range(N):
            temp = 0.0
            for j in range(k):
                sum_ += dataMat[i, j]
                temp += dataMat[i, j] ** 2
            temp -= n
            temp /= (n - 1) * n
            P0 += temp

        P0 /= N

        ysum = dataMat.sum(axis=0)
        ysum = ysum / sum_
        ysum = ysum ** 2

        Pe = ysum.sum()

        return (P0 - Pe) / (1 - Pe)