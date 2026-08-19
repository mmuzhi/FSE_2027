#include <vector>
#include <cmath>

class KappaCalculator {
public:
    // Calculate the cohens kappa value of a k-dimensional matrix
    static double kappa(const std::vector<std::vector<double>>& testData, int k) {
        double P0 = 0.0;
        for (int i = 0; i < k; ++i) {
            P0 += testData[i][i] * 1.0;
        }
        // xsum: row sums (k x 1), ysum: column sums (1 x k)
        std::vector<double> xsum(k, 0.0);
        std::vector<double> ysum(k, 0.0);
        double sum = 0.0;
        for (int i = 0; i < k; ++i) {
            for (int j = 0; j < k; ++j) {
                xsum[i] += testData[i][j];
                ysum[j] += testData[i][j];
                sum += testData[i][j];
            }
        }
        // Pe = float(ysum * xsum) / sum / sum  (ysum * xsum is the dot product)
        double dot = 0.0;
        for (int i = 0; i < k; ++i) {
            dot += ysum[i] * xsum[i];
        }
        double Pe = dot / sum / sum;
        P0 = P0 / sum * 1.0;
        double cohens_coefficient = (P0 - Pe) / (1 - Pe);
        return cohens_coefficient;
    }

    // Calculate the fleiss kappa value of an N * k matrix
    static double fleiss_kappa(const std::vector<std::vector<double>>& testData, int N, int k, int n) {
        double sum = 0.0;
        double P0 = 0.0;
        for (int i = 0; i < N; ++i) {
            double temp = 0.0;
            for (int j = 0; j < k; ++j) {
                sum += testData[i][j];
                temp += 1.0 * std::pow(testData[i][j], 2);
            }
            temp -= n;
            temp /= (n - 1) * n;
            P0 += temp;
        }
        P0 = 1.0 * P0 / N;
        // ysum: column sums (1 x k), then squared proportions
        std::vector<double> ysum(k, 0.0);
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < k; ++j) {
                ysum[j] += testData[i][j];
            }
        }
        for (int i = 0; i < k; ++i) {
            ysum[i] = std::pow(ysum[i] / sum, 2);
        }
        // Pe = ysum * oneMat * 1.0  (sum of squared proportions)
        double Pe = 0.0;
        for (int i = 0; i < k; ++i) {
            Pe += ysum[i];
        }
        double ans = (P0 - Pe) / (1 - Pe);
        return ans;  // ans[0, 0]
    }
};