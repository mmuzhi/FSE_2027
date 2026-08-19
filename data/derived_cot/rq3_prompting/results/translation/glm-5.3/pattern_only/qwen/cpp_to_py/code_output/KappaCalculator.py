import numpy as np


class KappaCalculator:

    @staticmethod
    def kappa(testData, k):
        dataMat = np.zeros((len(testData), k), dtype=np.float64)
        for i in range(len(testData)):
            for j in range(k):
                dataMat[i, j] = testData[i][j]

        P0 = np.float64(0.0)
        for i in range(k):
            P0 += dataMat[i, i]

        xsum = dataMat.sum(axis=1)
        ysum = dataMat.sum(axis=0)
        total = dataMat.sum()

        Pe = ysum.dot(xsum) / (total * total)
        P0 /= total

        return (P0 - Pe) / (1 - Pe)

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        dataMat = np.zeros((len(testData), k), dtype=np.float64)
        for i in range(len(testData)):
            for j in range(k):
                dataMat[i, j] = testData[i][j]

        total = np.float64(0.0)
        P0 = np.float64(0.0)

        for i in range(N):
            temp = np.float64(0.0)
            for j in range(k):
                total += dataMat[i, j]
                temp += dataMat[i, j] ** 2
            temp -= n
            temp /= (n - 1) * n
            P0 += temp

        P0 /= N

        ysum = dataMat.sum(axis=0)
        ysum = ysum / total
        ysum = ysum ** 2

        Pe = ysum.sum()

        ans = (P0 - Pe) / (1 - Pe)
        return ans