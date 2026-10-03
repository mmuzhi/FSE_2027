import numpy as np

class KappaCalculator:
    @staticmethod
    def kappa(testData, k):
        dataMat = np.array(testData, dtype=np.float64)
        P0 = 0.0
        for i in range(k):
            P0 += dataMat[i, i]
        xsum = dataMat.sum(axis=1)  # row sums, shape (rows,)
        ysum = dataMat.sum(axis=0)  # col sums, shape (cols,)
        total = dataMat.sum()
        Pe = np.dot(ysum, xsum) / (total * total)
        P0 /= total
        cohens_coefficient = (P0 - Pe) / (1.0 - Pe)
        return cohens_coefficient

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        dataMat = np.array(testData, dtype=np.float64)
        total = 0.0
        P0 = 0.0
        for i in range(N):
            temp = 0.0
            for j in range(k):
                val = dataMat[i, j]
                total += val
                temp += val * val
            temp = (temp - n) / ((n - 1) * n)
            P0 += temp
        P0 /= N
        ysum = dataMat.sum(axis=0)  # column sums
        ysum = ysum / total
        ysum = ysum * ysum
        Pe = ysum.sum()
        ans = (P0 - Pe) / (1.0 - Pe)
        return ans