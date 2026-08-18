#include <vector>
#include <cmath>

class KappaCalculator {
public:
    // Calculate the cohens kappa value of a k-dimensional matrix
    // testData: The k-dimensional matrix that needs to calculate the cohens kappa value
    // k: Matrix dimension
    // returns: the cohens kappa value of the matrix
    static double kappa(const std::vector<std::vector<double>>& testData, int k) {
        double P0 = 0.0;
        for (int i = 0; i < k; ++i)
            P0 += testData[i][i] * 1.0;

        std::size_t rows = testData.size();
        std::size_t cols = rows > 0 ? testData[0].size() : 0;
        std::vector<double> xsum(rows, 0.0);   // row sums
        std::vector<double> ysum(cols, 0.0);   // column sums
        double total = 0.0;
        for (std::size_t i = 0; i < rows; ++i)
            for (std::size_t j = 0; j < testData[i].size(); ++j) {
                xsum[i] += testData[i][j];
                ysum[j] += testData[i][j];
                total += testData[i][j];
            }

        // Pe = float(ysum * xsum) / sum / sum  (dot product of column and row sums)
        double Pe = 0.0;
        for (int i = 0; i < k; ++i)
            Pe += ysum[i] * xsum[i];
        Pe /= total * total;

        P0 = P0 / total * 1.0;
        double cohens_coefficient = (P0 - Pe) / (1.0 - Pe);
        return cohens_coefficient;
    }

    // Calculate the fleiss kappa value of an N * k matrix
    // testData: Input data matrix, N * k
    // N: Number of samples, k: Number of categories, n: Number of raters
    // returns: fleiss kappa value
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
            temp /= (n - 1) * n;   // temp is double, so this is float division
            P0 += temp;
        }
        P0 = 1.0 * P0 / N;

        std::vector<double> ysum(k, 0.0);   // column sums
        for (int j = 0; j < k; ++j)
            for (int i = 0; i < N; ++i)
                ysum[j] += testData[i][j];

        for (int i = 0; i < k; ++i)
            ysum[i] = std::pow(ysum[i] / sum, 2);

        // Pe = ysum * oneMat : sum of squared proportions
        double Pe = 0.0;
        for (int i = 0; i < k; ++i)
            Pe += ysum[i] * 1.0;

        double ans = (P0 - Pe) / (1.0 - Pe);
        return ans;   // ans[0, 0] of the 1x1 matrix result
    }
};