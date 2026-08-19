#include <cmath>
#include <limits>
#include <vector>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

class DataStatistics4 {
public:
    static double correlation_coefficient(const std::vector<double>& data1,
                                          const std::vector<double>& data2) {
        std::size_t n = data1.size();
        double mean1 = sum(data1) / static_cast<double>(n);
        double mean2 = sum(data2) / static_cast<double>(n);

        double numerator = 0.0;
        double sum_sq1 = 0.0;
        double sum_sq2 = 0.0;
        for (std::size_t i = 0; i < n; ++i) {
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
        std::size_t n = data.size();
        double mean = sum(data) / static_cast<double>(n);
        double variance = 0.0;
        for (double x : data) {
            variance += std::pow(x - mean, 2.0);
        }
        variance /= static_cast<double>(n);
        double std_deviation = std::sqrt(variance);

        if (std_deviation != 0.0) {
            double m3 = 0.0;
            for (double x : data) {
                m3 += std::pow(x - mean, 3.0);
            }
            return m3 * static_cast<double>(n) /
                   ((static_cast<double>(n) - 1.0) * (static_cast<double>(n) - 2.0) *
                    std::pow(std_deviation, 3.0));
        }
        return 0.0;
    }

    static double kurtosis(const std::vector<double>& data) {
        std::size_t n = data.size();
        double mean = sum(data) / static_cast<double>(n);

        double sq_sum = 0.0;
        for (double x : data) {
            sq_sum += std::pow(x - mean, 2.0);
        }
        double std_dev = std::sqrt(sq_sum / static_cast<double>(n));

        if (std_dev == 0.0) {
            return std::numeric_limits<double>::quiet_NaN();
        }

        double fourth_moment = 0.0;
        for (double x : data) {
            fourth_moment += std::pow(x - mean, 4.0);
        }
        fourth_moment /= static_cast<double>(n);

        return (fourth_moment / std::pow(std_dev, 4.0)) - 3.0;
    }

    static std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
        std::vector<double> pdf_values;
        pdf_values.reserve(data.size());
        double coef = 1.0 / (sigma * std::sqrt(2.0 * M_PI));
        for (double x : data) {
            double z = (x - mu) / sigma;
            pdf_values.push_back(coef * std::exp(-0.5 * z * z));
        }
        return pdf_values;
    }

private:
    static double sum(const std::vector<double>& v) {
        double s = 0.0;
        for (double x : v) {
            s += x;
        }
        return s;
    }
};