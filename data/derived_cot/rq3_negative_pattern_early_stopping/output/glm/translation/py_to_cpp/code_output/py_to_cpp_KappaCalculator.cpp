#include <vector>
#include <stdexcept>

class KappaCalculator {
public:
    static double kappa(const std::vector<std::vector<double>>& testData, int k) {
        double P0 = 0.0;
        for (int i = 0; i < k; ++i) {
            P0 += testData[i][i];
        }
        
        std::vector<double> xsum(k, 0.0);
        std::vector<double> ysum(k, 0.0);
        double total_sum = 0.0;
        
        for (int i = 0; i < k; ++i) {
            for (int j = 0; j < k; ++j) {
                xsum[i] += testData[i][j];
                ysum[j] += testData[i][j];
                total_sum += testData[i][j];
            }
        }
        
        if (total_sum == 0.0) {
            throw std::runtime_error("ZeroDivisionError");
        }
        
        double yx_sum = 0.0;
        for (int i = 0; i < k; ++i) {
            yx_sum += ysum[i] * xsum[i];
        }
        
        double Pe = yx_sum / total_sum / total_sum;
        P0 = P0 / total_sum;
        
        if (1.0 - Pe == 0.0) {
            throw std::runtime_error("ZeroDivisionError");
        }
        
        double cohens_coefficient = (P0 - Pe) / (1.0 - Pe);
        return cohens_coefficient;
    }

    static double fleiss_kappa(const std::vector<std::vector<double>>& testData, int N, int k, int n) {
        if (N == 0 || (n - 1) * n == 0) {
            throw std::runtime_error("ZeroDivisionError");
        }
        
        double total_sum = 0.0;
        double P0 = 0.0;
        
        for (int i = 0; i < N; ++i) {
            double temp = 0.0;
            for (int j = 0; j < k; ++j) {
                total_sum += testData[i][j];
                temp += testData[i][j] * testData[i][j];
            }
            temp -= n;
            temp /= (n - 1.0) * n;
            P0 += temp;
        }
        
        P0 = P0 / N;
        
        if (total_sum == 0.0) {
            throw std::runtime_error("ZeroDivisionError");
        }
        
        std::vector<double> ysum(k, 0.0);
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < k; ++j) {
                ysum[j] += testData[i][j];
            }
        }
        
        double Pe = 0.0;
        for (int i = 0; i < k; ++i) {
            Pe += (ysum[i] / total_sum) * (ysum[i] / total_sum);
        }
        
        if (1.0 - Pe == 0.0) {
            throw std::runtime_error("ZeroDivisionError");
        }
        
        double ans = (P0 - Pe) / (1.0 - Pe);
        return ans;
    }
};