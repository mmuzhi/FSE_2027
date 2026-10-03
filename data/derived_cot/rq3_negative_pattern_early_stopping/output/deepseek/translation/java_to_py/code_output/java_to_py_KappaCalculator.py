def kappa(test_data, k):
    data_mat = test_data
    P0 = 0.0
    for i in range(k):
        P0 += data_mat[i][i]
    xsum = [0] * k
    ysum = [0] * k
    total = 0
    for i in range(k):
        for j in range(k):
            xsum[i] += data_mat[i][j]
            ysum[j] += data_mat[i][j]
            total += data_mat[i][j]
    Pe = 0.0
    for i in range(k):
        Pe += ysum[i] * xsum[i]
    Pe = Pe / (total * total)
    P0 = P0 / total
    return (P0 - Pe) / (1 - Pe)

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
        temp /= (n - 1) * n
        P[i] = temp
    P0 = sum(P) / N
    pj = [0.0] * k
    for j in range(k):
        for i in range(N):
            pj[j] += data_mat[i][j]
        pj[j] /= total
    Pe = sum(p * p for p in pj)
    return (P0 - Pe) / (1 - Pe)

if __name__ == "__main__":
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