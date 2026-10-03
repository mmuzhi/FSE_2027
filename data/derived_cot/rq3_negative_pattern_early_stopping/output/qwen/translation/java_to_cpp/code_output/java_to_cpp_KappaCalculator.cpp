#include <vector>
#include <iostream>

namespace org::example {

double kappa(const std::vector<std::vector<int>>& testData, int k) {
    if (k <= 0) {
        return 0.0;
    }
    int total = 0;
    int diagonalSum = 0;
    std::vector<int> rowSums(k, 0);
    std::vector<int> colSums(k, 0);

    for (int i = 0; i < k; ++i) {
        for (int j = 0; j < k; ++j) {
            diagonalSum += testData[i][j];
            rowSums[i] += testData[i][j];
            colSums[j] += testData[i][j];
            total += testData[i][j];
        }
    }

    double P0 = static_cast<double>(diagonalSum) / total;
    double Pe = 0.0;
    for (int i = 0; i < k; ++i) {
        Pe += static_cast<double>(rowSums[i]) * colSums[i];
    }
    Pe /= static_cast<double>(total * total);
    return (P0 - Pe) / (1.0 - Pe);
}

double fleissKappa(const std::vector<std::vector<int>>& testData, int N, int k, int n) {
    if (N <= 0 || k <= 0 || n <= 0) {
        return 0.0;
    }
    std::vector<double> P(N, 0.0);
    int totalRatings = 0;

    for (int i = 0; i < N; ++i) {
        int rowSum = 0;
        double tempSum = 0.0;
        for (int j = 0; j < k; ++j) {
            rowSum += testData[i][j];
            tempSum += static_cast<double>(testData[i][j]) * testData[i][j];
        }
        tempSum -= n;
        tempSum /= static_cast<double>((n - 1) * n);
        P[i] = tempSum;
        totalRatings += rowSum;
    }

    double P0 = 0.0;
    for (double val : P) {
        P0 += val;
    }
    P0 /= static_cast<double>(N);

    std::vector<double> pj(k, 0.0);
    for (int j = 0; j < k; ++j) {
        for (int i = 0; i < N; ++i) {
            pj[j] += testData[i][j];
        }
        pj[j] /= static_cast<double>(totalRatings);
    }

    double Pe = 0.0;
    for (double p : pj) {
        Pe += p * p;
    }
    return (P0 - Pe) / (1.0 - Pe);
}

} // namespace org::example

int main() {
    std::vector<std::vector<int>> testData1 = {{2, 1, 1}, {1, 2, 1}, {1, 1, 2}};
    std::cout << org::example::kappa(testData1, 3) << std::endl; // Expected output: 0.25

    std::vector<std::vector<int>> testData2 = {
        {0, 0, 0, 0, 14},
        {0, 2, 6, 4, 2},
        {0, 0, 3, 5, 6},
        {0, 3, 9, 2, 0},
        {2, 2, 8, 1, 1},
        {7, 7, 0, 0, 0},
        {3, 2, 6, 3, 0},
        {2, 5, 3, 2, 2},
        {6, 5, 2, 1, 0},
        {0, 2, 2, 3, 7}
    };
    std::cout << org::example::fleissKappa(testData2, 10, 5, 14) << std::endl; // Expected output: 0.573
    return 0;
}