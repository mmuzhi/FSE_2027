#include <vector>
#include <iostream>
#include <cmath>

class KappaCalculator {
public:
    static double kappa(const std::vector<std::vector<int>>& testData, int k) {
        double P0 = 0.0;
        for (int i = 0; i < k; i++) {
            P0 += testData[i][i];
        }

        std::vector<double> rowSums(k, 0.0);
        for (int i = 0; i < k; i++) {
            for (int j = 0; j < k; j++) {
                rowSums[i] += testData[i][j];
            }
        }

        std::vector<double> colSums(k, 0.0);
        for (int j = 0; j < k; j++) {
            for (int i = 0; i < k; i++) {
                colSums[j] += testData[i][j];
            }
        }

        double total = 0.0;
        for (int i = 0; i < k; i++) {
            total += rowSums[i];
        }

        double pe = 0.0;
        for (int i = 0; i < k; i++) {
            pe += colSums[i] * rowSums[i];
        }
        pe /= total * total;

        double p0 = P0 / total;
        double cohens_coefficient = (p0 - pe) / (1 - pe);
        return cohens_coefficient;
    }

    static double fleiss_kappa(const std::vector<std::vector<int>>& testData, int N, int k, int n) {
        double P0 = 0.0;
        for (int i = 0; i < N; i++) {
            double temp = 0.0;
            double rowSum = 0.0;
            for (int j = 0; j < k; j++) {
                rowSum += testData[i][j];
                temp += static_cast<double>(testData[i][j]) * testData[i][j];
            }
            temp -= n;
            temp /= (n - 1) * n;
            P0 += temp;
        }
        P0 /= N;

        std::vector<double> ysum(k, 0.0);
        for (int j = 0; j < k; j++) {
            for (int i = 0; i < N; i++) {
                ysum[j] += testData[i][j];
            }
        }

        double totalRatings = static_cast<double>(N) * n;
        double pe = 0.0;
        for (int j = 0; j < k; j++) {
            double proportion = ysum[j] / totalRatings;
            pe += proportion * proportion;
        }

        double ans = (P0 - pe) / (1 - pe);
        return ans;
    }
};