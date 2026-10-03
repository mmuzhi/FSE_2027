#include <vector>
#include <cmath>
#include <iostream>
#include <algorithm>

class DataStatistics4 {
public:
    static double correlation_coefficient(const std::vector<double>& data1, const std::vector<double>& data2) {
        if (data1.size() != data2.size()) {
            throw std::invalid_argument("Data sets must be of the same length");
        }
        size_t n = data1.size();
        double mean1 = 0.0, mean2 = 0.0;
        for (double x : data1) mean1 += x;
        for (double x : data2) mean2 += x;
        mean1 /= n;
        mean2 /= n;

        double numerator = 0.0, den1_sq = 0.0, den2_sq = 0.0;
        for (size_t i = 0; i < n; ++i) {
            numerator += (data1[i] - mean1) * (data2[i] - mean2);
            den1_sq += (data1[i] - mean1) * (data1[i] - mean1);
            den2_sq += (data2[i] - mean2) * (data2[i] - mean2);
        }

        double denominator = std::sqrt(den1_sq) * std::sqrt(den2_sq);
        if (denominator == 0) return 0.0;
        return numerator / denominator;
    }

    static double skewness(const std::vector<double>& data) {
        if (data.empty()) throw std::invalid_argument("Data set is empty");
        size_t n = data.size();
        double mean = 0.0;
        for (double x : data) mean += x;
        mean /= n;

        double variance = 0.0;
        for (double x : data) variance += (x - mean) * (x - mean);
        variance /= n;

        if (variance == 0.0) return 0.0;

        double std_dev = std::sqrt(variance);
        double skewness_numerator = 0.0;
        for (double x : data) skewness_numerator += std::pow(x - mean, 3.0);
        skewness_numerator /= (n - 1.0) * (n - 2.0) * std_dev * std_dev * std_dev;

        return skewness_numerator;
    }

    static double kurtosis(const std::vector<double>& data) {
        if (data.empty()) throw std::invalid_argument("Data set is empty");
        size_t n = data.size();
        double mean = 0.0;
        for (double x : data) mean += x;
        mean /= n;

        double variance = 0.0;
        for (double x : data) variance += (x - mean) * (x - mean);
        variance /= n;

        if (variance == 0.0) {
            // Return NaN as in the original Python code
            return std::numeric_limits<double>::quiet_NaN();
        }

        double std_dev = std::sqrt(variance);
        double fourth_moment = 0.0;
        for (double x : data) fourth_moment += std::pow(x - mean, 4.0);
        fourth_moment /= n;

        return (fourth_moment / (std_dev * std_dev * std_dev * std_dev)) - 3.0;
    }

    static std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
        std::vector<double> result;
        const double sqrt_two_pi = std::sqrt(2.0 * M_PI);
        for (double x : data) {
            result.push_back(std::exp(-0.5 * std::pow((x - mu) / sigma, 2.0)) / (sigma * sqrt_two_pi));
        }
        return result;
    }
};

// Example usage
int main() {
    // Test correlation_coefficient
    std::vector<double> data1 = {1, 2, 3};
    std::vector<double> data2 = {4, 5, 6};
    std::cout << "Correlation: " << DataStatistics4::correlation_coefficient(data1, data2) << std::endl;

    // Test skewness
    std::vector<double> data = {1, 2, 5};
    std::cout << "Skewness: " << DataStatistics4::skewness(data) << std::endl;

    // Test kurtosis
    std::vector<double> data_kurtosis = {1, 20, 100};
    std::cout << "Kurtosis: " << DataStatistics4::kurtosis(data_kurtosis) << std::endl;

    // Test pdf
    std::vector<double> pdf_data = {1, 2, 3};
    std::vector<double> pdf_result = DataStatistics4::pdf(pdf_data, 1, 1);
    for (double val : pdf_result) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    return 0;
}