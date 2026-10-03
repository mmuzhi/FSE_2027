#include <vector>
#include <cmath>
#include <numeric>
#include <stdexcept> // for potential domain errors (optional)

class DataStatistics4 {
public:
    static double correlation_coefficient(const std::vector<double>& data1, const std::vector<double>& data2) {
        int n = static_cast<int>(data1.size());
        double mean1 = std::accumulate(data1.begin(), data1.end(), 0.0) / n;
        double mean2 = std::accumulate(data2.begin(), data2.end(), 0.0) / n;

        double numerator = 0.0;
        double denom1 = 0.0;
        double denom2 = 0.0;
        for (int i = 0; i < n; ++i) {
            double diff1 = data1[i] - mean1;
            double diff2 = data2[i] - mean2;
            numerator += diff1 * diff2;
            denom1 += diff1 * diff1;
            denom2 += diff2 * diff2;
        }
        double denominator = std::sqrt(denom1) * std::sqrt(denom2);
        if (denominator == 0.0) {
            return 0.0;
        }
        return numerator / denominator;
    }

    static double skewness(const std::vector<double>& data) {
        int n = static_cast<int>(data.size());
        double mean = std::accumulate(data.begin(), data.end(), 0.0) / n;

        double variance = 0.0;
        for (double x : data) {
            double diff = x - mean;
            variance += diff * diff;
        }
        variance /= n;
        double std_dev = std::sqrt(variance);

        if (std_dev == 0.0) {
            return 0.0;
        }

        double skew = 0.0;
        for (double x : data) {
            double diff = x - mean;
            skew += diff * diff * diff;
        }
        skew = skew * n / ((n - 1) * (n - 2) * std_dev * std_dev * std_dev);
        return skew;
    }

    static double kurtosis(const std::vector<double>& data) {
        int n = static_cast<int>(data.size());
        double mean = std::accumulate(data.begin(), data.end(), 0.0) / n;

        double variance = 0.0;
        for (double x : data) {
            double diff = x - mean;
            variance += diff * diff;
        }
        variance /= n;
        double std_dev = std::sqrt(variance);

        if (std_dev == 0.0) {
            return std::numeric_limits<double>::quiet_NaN();
        }

        double fourth_moment = 0.0;
        for (double x : data) {
            double diff = x - mean;
            fourth_moment += diff * diff * diff * diff;
        }
        fourth_moment /= n;

        double kurt = (fourth_moment / (std_dev * std_dev * std_dev * std_dev)) - 3.0;
        return kurt;
    }

    static std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
        std::vector<double> pdf_values;
        pdf_values.reserve(data.size());
        double inv_sigma_sqrt_2pi = 1.0 / (sigma * std::sqrt(2.0 * M_PI));
        for (double x : data) {
            double exponent = -0.5 * ((x - mu) / sigma) * ((x - mu) / sigma);
            pdf_values.push_back(inv_sigma_sqrt_2pi * std::exp(exponent));
        }
        return pdf_values;
    }
};