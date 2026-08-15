#include <vector>
#include <stdexcept>

class KappaCalculator {
private:
    template<typename T>
    static double kappa_impl(const std::vector<std::vector<T>>& testData, int k) {
        int R = static_cast<int>(testData.size());
        int C = R > 0 ? static_cast<int>(testData[0].size()) : 0;

        for (int i = 0; i < R; ++i) {
            if (static_cast<int>(testData[i].size()) != C) {
                throw std::invalid_argument("Inconsistent row sizes");
            }
        }

        double P0 = 0.0;
        for (int i = 0; i < k; ++i) {
            P0 += static_cast<double>(testData.at(i).at(i));
        }

        std::vector<double> xsum(R, 0.0);
        std::vector<double> ysum(C, 0.0);
        double sum = 0.0;
        for (int i = 0; i < R; ++i) {
            for (int j = 0; j < C; ++j) {
                double val = static_cast<double>(testData[i][j]);
                xsum[i] += val;
                ysum[j] += val;
                sum += val;
            }
        }

        if (C != R) {
            throw std::invalid_argument("Shapes not aligned");
        }

        double yxsum = 0.0;
        for (int j = 0; j < C; ++j) {
            yxsum += ysum[j] * xsum[j];
        }

        if (sum == 0.0) {
            throw std::runtime_error("Division by zero");
        }

        double Pe = yxsum / sum / sum;
        double P0_val = P0 / sum;
        double denom = 1.0 - Pe;
        if (denom == 0.0) {
            throw std::runtime_error("Division by zero");
        }
        return (P0_val - Pe) / denom;
    }

    template<typename T>
    static double fleiss_kappa_impl(const std::vector<std::vector<T>>& testData, int N, int k, int n) {
        int R = static_cast<int>(testData.size());
        int C = R > 0 ? static_cast<int>(testData[0].size()) : 0;

        for (int i = 0; i < R; ++i) {
            if (static_cast<int>(testData[i].size()) != C) {
                throw std::invalid_argument("Inconsistent row sizes");
            }
        }

        if (N == 0) {
            throw std::runtime_error("Division by zero");
        }

        double sum = 0.0;
        double P0 = 0.0;
        for (int i = 0; i < N; ++i) {
            double temp = 0.0;
            for (int j = 0; j < k; ++j) {
                double val = static_cast<double>(testData.at(i).at(j));
                sum += val;
                temp += val * val;
            }
            temp -= n;
            double denom = (static_cast<double>(n) - 1.0) * n;
            if (denom == 0.0) {
                throw std::runtime_error("Division by zero");
            }
            temp /= denom;
            P0 += temp;
        }
        P0 = P0 / N;

        std::vector<double> ysum(C, 0.0);
        for (int i = 0; i < R; ++i) {
            for (int j = 0; j < C; ++j) {
                ysum[j] += static_cast<double>(testData[i][j]);
            }
        }

        if (k > 0 && sum == 0.0) {
            throw std::runtime_error("Division by zero");
        }
        if (C != k) {
            throw std::invalid_argument("Shapes not aligned");
        }

        double Pe = 0.0;
        for (int i = 0; i < k; ++i) {
            double p = ysum[i] / sum;
            Pe += p * p;
        }

        double denom = 1.0 - Pe;
        if (denom == 0.0) {
            throw std::runtime_error("Division by zero");
        }
        return (P0 - Pe) / denom;
    }

public:
    static double kappa(const std::vector<std::vector<double>>& testData, int k) {
        return kappa_impl(testData, k);
    }

    template<typename T>
    static double kappa(const std::vector<std::vector<T>>& testData, int k) {
        return kappa_impl(testData, k);
    }

    static double fleiss_kappa(const std::vector<std::vector<double>>& testData, int N, int k, int n) {
        return fleiss_kappa_impl(testData, N, k, n);
    }

    template<typename T>
    static double fleiss_kappa(const std::vector<std::vector<T>>& testData, int N, int k, int n) {
        return fleiss_kappa_impl(testData, N, k, n);
    }
};