#include <vector>
#include <cstddef>
#include <cmath>

class KappaCalculator {
public:
    /**
     * Calculate Cohen's kappa value for a k × k matrix.
     * @param testData : k × k matrix of counts (as integers)
     * @param k : matrix dimension
     * @return Cohen's kappa coefficient
     */
    static double kappa(const std::vector<std::vector<int>>& testData, int k) {
        // Convert to double matrix
        std::vector<std::vector<double>> dataMat(k, std::vector<double>(k, 0.0));
        double totalSum = 0.0;
        double diagSum = 0.0;
        std::vector<double> rowSums(k, 0.0);
        std::vector<double> colSums(k, 0.0);

        for (int i = 0; i < k; ++i) {
            for (int j = 0; j < k; ++j) {
                double val = static_cast<double>(testData[i][j]);
                dataMat[i][j] = val;
                totalSum += val;
                rowSums[i] += val;
                colSums[j] += val;
                if (i == j) {
                    diagSum += val;
                }
            }
        }

        double P0 = diagSum / totalSum;

        // Pe = sum(rowSums[i] * colSums[i]) / (totalSum * totalSum)
        double peNumerator = 0.0;
        for (int i = 0; i < k; ++i) {
            peNumerator += rowSums[i] * colSums[i];
        }
        double Pe = peNumerator / (totalSum * totalSum);

        return (P0 - Pe) / (1.0 - Pe);
    }

    /**
     * Calculate Fleiss' kappa value for an N × k matrix.
     * @param testData : N × k matrix where each row sums to n (number of raters)
     * @param N : number of subjects (rows)
     * @param k : number of categories (columns)
     * @param n : number of raters per subject (constant)
     * @return Fleiss' kappa coefficient
     */
    static double fleiss_kappa(const std::vector<std::vector<int>>& testData, int N, int k, int n) {
        // Convert to double matrix
        std::vector<std::vector<double>> dataMat(N, std::vector<double>(k, 0.0));
        double totalSum = 0.0;
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < k; ++j) {
                double val = static_cast<double>(testData[i][j]);
                dataMat[i][j] = val;
                totalSum += val;
            }
        }

        // Compute P0
        double P0 = 0.0;
        for (int i = 0; i < N; ++i) {
            double temp = 0.0;
            for (int j = 0; j < k; ++j) {
                temp += dataMat[i][j] * dataMat[i][j];
            }
            temp = (temp - static_cast<double>(n)) / (static_cast<double>(n - 1) * n);
            P0 += temp;
        }
        P0 /= static_cast<double>(N);

        // Compute column sums
        std::vector<double> colSums(k, 0.0);
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < k; ++j) {
                colSums[j] += dataMat[i][j];
            }
        }

        // Compute Pe = sum_j (colSums[j] / totalSum)^2
        double Pe = 0.0;
        for (int j = 0; j < k; ++j) {
            double pj = colSums[j] / totalSum;
            Pe += pj * pj;
        }

        return (P0 - Pe) / (1.0 - Pe);
    }
};