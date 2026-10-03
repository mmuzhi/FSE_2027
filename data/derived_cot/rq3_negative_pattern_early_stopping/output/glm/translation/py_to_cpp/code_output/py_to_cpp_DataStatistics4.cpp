#include <vector>
#include <cmath>
#include <numeric>
#include <limits>

class DataStatistics4 {
public:
    static double correlation_coefficient(const std::vector<double>& data1, const std::vector<double>& data2) {
        int n = static_cast<int>(data1.size());
        double mean1 = std::accumulate(data1.begin(), data1.end(), 0.0) / n;
        double mean2 = std::accumulate(data2.begin(), data2.end(), 0.0) / n;

        double numerator = 0.0;
        double sum_sq1 = 0.0;
        double sum_sq2 = 0.0;
        for (int i = 0; i < n; ++i) {
            double d1 = data1[i] - mean1;
            double d2 = data2[i] - mean2;
            numerator += d1 * d2;
            sum_sq1 += d1 * d1;
            sum_sq2 += d2 * d2;
        }
        double denominator = std::sqrt(sum_sq1) * std::sqrt(sum_sq2);

        return denominator != 0.0 ? numerator / denominator : 0.0;
    }

    static double skewness(const std::vector<double>& data) {
        int n = static_cast<int>(data.size());
        double mean = std::accumulate(data.begin(), data.end(), 0.0) / n;

        double variance = 0.0;
        double sum_cubed = 0.0;
        for (const auto& x : data) {
            double d = x - mean;
            variance += d * d;
            sum_cubed += d * d * d;
        }
        variance /= n;
        double std_deviation = std::sqrt(variance);

        if (std_deviation == 0.0) {
            return 0.0;
        }
        return sum_cubed * n / ((n - 1) * (n - 2) * std_deviation * std_deviation * std_deviation);
    }

    static double kurtosis(const std::vector<double>& data) {
        int n = static_cast<int>(data.size());
        double mean = std::accumulate(data.begin(), data.end(), 0.0) / n;

        double sum_sq = 0.0;
        for (const auto& x : data) {
            double d = x - mean;
            sum_sq += d * d;
        }
        double std_dev = std::sqrt(sum_sq / n);

        if (std_dev == 0.0) {
            return std::numeric_limits<double>::quiet_NaN();
        }

        double fourth_moment = 0.0;
        for (const auto& x : data) {
            double d = x - mean;
            fourth_moment += d * d * d * d;
        }
        fourth_moment /= n;

        return fourth_moment / (std_dev * std_dev * std_dev * std_dev) - 3.0;
    }

    static std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
        static const double pi = std::acos(-1.0);
        std::vector<double> pdf_values;
        pdf_values.reserve(data.size());
        double coeff = 1.0 / (sigma * std::sqrt(2.0 * pi));
        for (const auto& x : data) {
            double z = (x - mu) / sigma;
            pdf_values.push_back(coeff * std::exp(-0.5 * z * z));
        }
        return pdf_values;
    }
};