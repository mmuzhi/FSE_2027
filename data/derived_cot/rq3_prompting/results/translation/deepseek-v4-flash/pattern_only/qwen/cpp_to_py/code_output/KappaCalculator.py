import math

def _div(a, b):
    if b == 0.0:
        if a == 0.0 or math.isnan(a):
            return float('nan')
        sign = math.copysign(1.0, a) * math.copysign(1.0, b)
        return math.copysign(float('inf'), sign)
    return a / b

class KappaCalculator:
    @staticmethod
    def kappa(testData, k):
        rows = len(testData)
        dataMat = [[float(testData[i][j]) for j in range(k)] for i in range(rows)]

        P0 = 0.0
        for i in range(k):
            P0 += dataMat[i][i]

        xsum = [sum(row) for row in dataMat]
        ysum = [sum(dataMat[i][j] for i in range(rows)) for j in range(k)]
        total = sum(xsum)

        if len(xsum) != len(ysum):
            raise ValueError("dot product size mismatch")

        dot = sum(xsum[i] * ysum[i] for i in range(len(xsum)))

        Pe = _div(dot, total * total)
        P0 = _div(P0, total)

        return _div(P0 - Pe, 1 - Pe)

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        rows = len(testData)
        dataMat = [[float(testData[i][j]) for j in range(k)] for i in range(rows)]

        total = 0.0
        P0 = 0.0

        for i in range(N):
            temp = 0.0
            for j in range(k):
                total += dataMat[i][j]
                temp += dataMat[i][j] ** 2
            temp = _div(temp - n, (n - 1) * n)
            P0 += temp

        P0 = _div(P0, N)

        ysum = [sum(dataMat[i][j] for i in range(rows)) for j in range(k)]

        Pe = 0.0
        for v in ysum:
            Pe += _div(v, total) ** 2

        return _div(P0 - Pe, 1 - Pe)