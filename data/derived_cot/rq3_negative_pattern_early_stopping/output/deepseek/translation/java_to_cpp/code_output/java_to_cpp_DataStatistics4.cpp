#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>

namespace org_example {

class DataStatistics4 {
public:
    static double correlationCoefficient(const std::vector<double>& data1, const std::vector<double>& data2) {
        int n = data1.size();
        if (n == 0) return 0.0;
        double mean1 = std::accumulate(data1.begin(), data1.end(), 0.0) / n;
        double mean2 = std::accumulate(data2.begin(), data2.end(), 0.0) / n;

        double numerator = 0.0;
        double sumSq1 = 0.0;
        double sumSq2 = 0.0;
        for (int i = 0; i < n; ++i) {
            double diff1 = data1[i] - mean1;
            double diff2 = data2[i] - mean2;
            numerator += diff1 * diff2;
            sumSq1 += diff1 * diff1;
            sumSq2 += diff2 * diff2;
        }

        double denominator = std::sqrt(sumSq1) * std::sqrt(sumSq2);
        return denominator != 0.0 ? numerator / denominator : 0.0;
    }

    static double skewness(const std::vector<double>& data) {
        int n = data.size();
        if (n == 0) return 0.0;
        double mean = std::accumulate(data.begin(), data.end(), 0.0) / n;

        double variance = 0.0;
        for (double x : data) {
            variance += (x - mean) * (x - mean);
        }
        variance /= n;
        double stdDeviation = std::sqrt(variance);

        if (stdDeviation == 0.0) {
            return 0.0;
        }

        double sumCubed = 0.0;
        for (double x : data) {
            double diff = x - mean;
            sumCubed += diff * diff * diff;
        }
        double skewness = sumCubed * n / ((n - 1) * (n - 2) * std::pow(stdDeviation, 3));
        return skewness;
    }

    static double kurtosis(const std::vector<double>& data) {
        int n = data.size();
        if (n == 0) return std::numeric_limits<double>::quiet_NaN();
        double mean = std::accumulate(data.begin(), data.end(), 0.0) / n;

        double variance = 0.0;
        for (double x : data) {
            variance += (x - mean) * (x - mean);
        }
        variance /= n;
        double stdDev = std::sqrt(variance);

        if (stdDev == 0.0) {
            return std::numeric_limits<double>::quiet_NaN();
        }

        double fourthMoment = 0.0;
        for (double x : data) {
            double diff = x - mean;
            fourthMoment += std::pow(diff, 4);
        }
        fourthMoment /= n;

        double kurtosisValue = (fourthMoment / std::pow(stdDev, 4)) - 3.0;
        return kurtosisValue;
    }

    static std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
        std::vector<double> result;
        result.reserve(data.size());
        double invSigmaSqrt2Pi = 1.0 / (sigma * std::sqrt(2.0 * M_PI));
        for (double x : data) {
            double exponent = -0.5 * std::pow((x - mu) / sigma, 2);
            result.push_back(invSigmaSqrt2Pi * std::exp(exponent));
        }
        return result;
    }
};

} // namespace org_example