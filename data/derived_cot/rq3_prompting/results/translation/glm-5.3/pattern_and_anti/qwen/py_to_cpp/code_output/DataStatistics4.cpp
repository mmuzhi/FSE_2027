#include <cmath>
#include <limits>
#include <vector>

class DataStatistics4 {
public:
    static double correlation_coefficient(const std::vector<double>& data1, const std::vector<double>& data2) {
        size_t n = data1.size();
        double mean1 = sum(data1) / n;
        double mean2 = sum(data2) / n;

        double numerator = 0.0;
        double sq1 = 0.0;
        double sq2 = 0.0;
        for (size_t i = 0; i < n; ++i) {
            numerator += (data1[i] - mean1) * (data2[i] - mean2);
            sq1 += std::pow(data1[i] - mean1, 2);
            sq2 += std::pow(data2[i] - mean2, 2);
        }
        double denominator = std::sqrt(sq1) * std::sqrt(sq2);

        return denominator != 0 ? numerator / denominator : 0;
    }

    static double skewness(const std::vector<double>& data) {
        size_t n = data.size();
        double mean = sum(data) / n;
        double variance = 0.0;
        for (double x : data) variance += std::pow(x - mean, 2);
        variance /= n;
        double std_deviation = std::sqrt(variance);

        if (std_deviation != 0) {
            double sum_cubed = 0.0;
            for (double x : data) sum_cubed += std::pow(x - mean, 3);
            double dn = static_cast<double>(n);
            return sum_cubed * dn / ((dn - 1) * (dn - 2) * std::pow(std_deviation, 3));
        }
        return 0;
    }

    static double kurtosis(const std::vector<double>& data) {
        size_t n = data.size();
        double mean = sum(data) / n;
        double sum_sq = 0.0;
        for (double x : data) sum_sq += std::pow(x - mean, 2);
        double std_dev = std::sqrt(sum_sq / n);

        if (std_dev == 0)
            return std::numeric_limits<double>::quiet_NaN();

        double fourth_moment = 0.0;
        for (double x : data) fourth_moment += std::pow(x - mean, 4);
        fourth_moment /= n;

        return (fourth_moment / std::pow(std_dev, 4)) - 3;
    }

    static std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
        const double PI = 3.14159265358979323846;
        std::vector<double> pdf_values;
        pdf_values.reserve(data.size());
        for (double x : data) {
            pdf_values.push_back(
                1 / (sigma * std::sqrt(2 * PI)) *
                std::exp(-0.5 * std::pow((x - mu) / sigma, 2)));
        }
        return pdf_values;
    }

private:
    static double sum(const std::vector<double>& v) {
        double s = 0.0;
        for (double x : v) s += x;
        return s;
    }
};