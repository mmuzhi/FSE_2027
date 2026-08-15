#include <vector>
#include <cmath>
#include <stdexcept>
#include <limits>

class DataStatistics4 {
public:
    static double correlation_coefficient(const std::vector<double>& data1, const std::vector<double>& data2) {
        size_t n = data1.size();
        if (n == 0) {
            throw std::runtime_error("division by zero");
        }

        double mean1 = 0.0;
        for (double x : data1) {
            mean1 += x;
        }
        mean1 /= static_cast<double>(n);

        double mean2 = 0.0;
        for (double x : data2) {
            mean2 += x;
        }
        mean2 /= static_cast<double>(n);

        double numerator = 0.0;
        double sum1 = 0.0;
        double sum2 = 0.0;
        for (size_t i = 0; i < n; ++i) {
            double diff1 = data1[i] - mean1;
            double diff2 = data2.at(i) - mean2;
            numerator += diff1 * diff2;
            sum1 += diff1 * diff1;
            sum2 += diff2 * diff2;
        }

        double denominator = std::sqrt(sum1) * std::sqrt(sum2);
        if (denominator == 0.0) {
            return 0.0;
        }
        return numerator / denominator;
    }

    static double skewness(const std::vector<double>& data) {
        size_t n = data.size();
        if (n == 0) {
            throw std::runtime_error("division by zero");
        }

        double mean = 0.0;
        for (double x : data) {
            mean += x;
        }
        mean /= static_cast<double>(n);

        double variance = 0.0;
        for (double x : data) {
            double diff = x - mean;
            variance += diff * diff;
        }
        variance /= static_cast<double>(n);

        double std_deviation = std::sqrt(variance);
        if (std_deviation == 0.0) {
            return 0.0;
        }

        if (n < 3) {
            throw std::runtime_error("division by zero");
        }

        double sum_cubes = 0.0;
        for (double x : data) {
            double diff = x - mean;
            sum_cubes += diff * diff * diff;
        }

        double skewness = sum_cubes * static_cast<double>(n) /
                          (static_cast<double>(n - 1) * static_cast<double>(n - 2) * std::pow(std_deviation, 3));
        return skewness;
    }

    static double kurtosis(const std::vector<double>& data) {
        size_t n = data.size();
        if (n == 0) {
            throw std::runtime_error("division by zero");
        }

        double mean = 0.0;
        for (double x : data) {
            mean += x;
        }
        mean /= static_cast<double>(n);

        double variance = 0.0;
        for (double x : data) {
            double diff = x - mean;
            variance += diff * diff;
        }
        variance /= static_cast<double>(n);

        double std_dev = std::sqrt(variance);
        if (std_dev == 0.0) {
            return std::numeric_limits<double>::quiet_NaN();
        }

        double fourth_moment = 0.0;
        for (double x : data) {
            double diff = x - mean;
            fourth_moment += diff * diff * diff * diff;
        }
        fourth_moment /= static_cast<double>(n);

        double kurtosis_value = (fourth_moment / std::pow(std_dev, 4)) - 3.0;
        return kurtosis_value;
    }

    static std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
        if (sigma == 0.0) {
            throw std::runtime_error("division by zero");
        }

        const double pi = std::acos(-1.0);
        double inv_sigma = 1.0 / (sigma * std::sqrt(2.0 * pi));

        std::vector<double> pdf_values;
        pdf_values.reserve(data.size());
        for (double x : data) {
            double z = (x - mu) / sigma;
            pdf_values.push_back(inv_sigma * std::exp(-0.5 * z * z));
        }
        return pdf_values;
    }
};