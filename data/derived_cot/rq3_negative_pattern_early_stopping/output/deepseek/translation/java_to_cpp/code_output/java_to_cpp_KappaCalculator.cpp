#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>

double kappa(const std::vector<std::vector<int>>& dataMat, int k) {
    double P0 = 0.0;
    for (int i = 0; i < k; ++i) {
        P0 += dataMat[i][i];
    }

    std::vector<int> xsum(k, 0);
    std::vector<int> ysum(k, 0);
    int sum = 0;

    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < k; ++j) {
            xsum[i] += dataMat[i][j];
            ysum[j] += dataMat[i][j];
            sum += dataMat[i][j];
        }
    }

    double Pe = 0.0;
    for (int i = 0; i < k; ++i) {
        Pe += static_cast<double>(ysum[i]) * xsum[i];
    }
    Pe = Pe / (static_cast<double>(sum) * sum);
    P0 = P0 / sum;

    return (P0 - Pe) / (1.0 - Pe);
}

double fleissKappa(const std::vector<std::vector<int>>& dataMat, int N, int k, int n) {
    std::vector<double> P(N);
    double totalSum = 0.0;

    for (int i = 0; i < N; ++i) {
        double temp = 0.0;
        for (int j = 0; j < k; ++j) {
            totalSum += dataMat[i][j];
            temp += static_cast<double>(dataMat[i][j]) * dataMat[i][j];
        }
        temp -= n;
        temp /= static_cast<double>(n - 1) * n;
        P[i] = temp;
    }

    double P0 = std::accumulate(P.begin(), P.end(), 0.0) / N;

    std::vector<double> pj(k, 0.0);
    for (int j = 0; j < k; ++j) {
        for (int i = 0; i < N; ++i) {
            pj[j] += dataMat[i][j];
        }
        pj[j] /= totalSum;
    }

    double Pe = 0.0;
    for (int j = 0; j < k; ++j) {
        Pe += pj[j] * pj[j];
    }

    return (P0 - Pe) / (1.0 - Pe);
}

int main() {
    std::cout << kappa({{2, 1, 1}, {1, 2, 1}, {1, 1, 2}}, 3) << std::endl;
    std::cout << fleissKappa({{0, 0, 0, 0, 14},
                              {0, 2, 6, 4, 2},
                              {0, 0, 3, 5, 6},
                              {0, 3, 9, 2, 0},
                              {2, 2, 8, 1, 1},
                              {7, 7, 0, 0, 0},
                              {3, 2, 6, 3, 0},
                              {2, 5, 3, 2, 2},
                              {6, 5, 2, 1, 0},
                              {0, 2, 2, 3, 7}}, 10, 5, 14) << std::endl;
    return 0;
}