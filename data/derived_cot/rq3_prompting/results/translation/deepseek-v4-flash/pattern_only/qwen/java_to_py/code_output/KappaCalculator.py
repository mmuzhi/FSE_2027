def _div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        if a != a:
            return float('nan')
        if a == 0:
            return float('nan')
        return float('inf') if a > 0 else float('-inf')


def kappa(testData, k):
    dataMat = testData
    P0 = 0.0
    for i in range(k):
        P0 += dataMat[i][i] * 1.0

    xsum = [0] * k
    ysum = [0] * k
    sum_ = 0
    for i in range(k):
        for j in range(k):
            xsum[i] += dataMat[i][j]
            ysum[j] += dataMat[i][j]
            sum_ += dataMat[i][j]

    Pe = 0.0
    for i in range(k):
        Pe += ysum[i] * xsum[i]

    Pe = _div(Pe, sum_ * sum_)
    P0 = _div(P0, sum_)
    return _div(P0 - Pe, 1 - Pe)


def fleissKappa(testData, N, k, n):
    dataMat = testData
    P = [0.0] * N
    sum_ = 0.0
    for i in range(N):
        temp = 0.0
        for j in range(k):
            sum_ += dataMat[i][j]
            temp += dataMat[i][j] * dataMat[i][j]
        temp -= n
        temp = _div(temp, (n - 1) * n)
        P[i] = temp

    P0 = _div(sum(P), N)

    pj = [0.0] * k
    for j in range(k):
        for i in range(N):
            pj[j] += dataMat[i][j]
        pj[j] = _div(pj[j], sum_)

    Pe = sum(p * p for p in pj)
    return _div(P0 - Pe, 1 - Pe)


if __name__ == "__main__":
    print(kappa([[2, 1, 1], [1, 2, 1], [1, 1, 2]], 3))
    print(fleissKappa([[0, 0, 0, 0, 14],
                       [0, 2, 6, 4, 2],
                       [0, 0, 3, 5, 6],
                       [0, 3, 9, 2, 0],
                       [2, 2, 8, 1, 1],
                       [7, 7, 0, 0, 0],
                       [3, 2, 6, 3, 0],
                       [2, 5, 3, 2, 2],
                       [6, 5, 2, 1, 0],
                       [0, 2, 2, 3, 7]], 10, 5, 14))