import math


def _java_div(a, b):
    """Divide like Java's double division: dividing by zero yields
    Infinity or NaN instead of raising ZeroDivisionError."""
    if b == 0:
        if a == 0 or math.isnan(a):
            return float("nan")
        return math.copysign(float("inf"), a) * math.copysign(1.0, b)
    return a / b


def kappa(test_data, k):
    data_mat = test_data
    p0 = 0.0
    for i in range(k):
        p0 += data_mat[i][i] * 1.0
    xsum = [0] * k
    ysum = [0] * k
    total = 0
    for i in range(k):
        for j in range(k):
            xsum[i] += data_mat[i][j]
            ysum[j] += data_mat[i][j]
            total += data_mat[i][j]
    pe = 0.0
    for i in range(k):
        pe += ysum[i] * xsum[i]
    pe = _java_div(pe, total * total)
    p0 = _java_div(p0, total)
    return _java_div(p0 - pe, 1 - pe)


def fleiss_kappa(test_data, N, k, n):
    data_mat = test_data
    P = [0.0] * N
    total = 0.0
    for i in range(N):
        temp = 0.0
        for j in range(k):
            total += data_mat[i][j]
            temp += data_mat[i][j] * data_mat[i][j]
        temp -= n
        temp = _java_div(temp, (n - 1) * n)
        P[i] = temp
    p0 = _java_div(sum(P), N)
    pj = [0.0] * k
    for j in range(k):
        for i in range(N):
            pj[j] += data_mat[i][j]
        pj[j] = _java_div(pj[j], total)
    pe = sum(p * p for p in pj)
    return _java_div(p0 - pe, 1 - pe)


def main():
    print(kappa([[2, 1, 1], [1, 2, 1], [1, 1, 2]], 3))  # 0.25
    print(fleiss_kappa([[0, 0, 0, 0, 14],
                        [0, 2, 6, 4, 2],
                        [0, 0, 3, 5, 6],
                        [0, 3, 9, 2, 0],
                        [2, 2, 8, 1, 1],
                        [7, 7, 0, 0, 0],
                        [3, 2, 6, 3, 0],
                        [2, 5, 3, 2, 2],
                        [6, 5, 2, 1, 0],
                        [0, 2, 2, 3, 7]], 10, 5, 14))


if __name__ == "__main__":
    main()