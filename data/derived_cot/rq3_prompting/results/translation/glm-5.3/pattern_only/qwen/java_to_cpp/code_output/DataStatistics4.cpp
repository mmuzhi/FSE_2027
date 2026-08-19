#include <cmath>
#include <limits>
#include <vector>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

class DataStatistics4 {
public:
    static double correlationCoefficient(const std::vector<double>& data1, const std::vector<double>& data2) {
        int n = static_cast<int>(data1.size());
        double mean1 = meanOrZero(data1);
        double mean2 = meanOrZero(data2);

        double numerator = 0.0;
        for (int i = 0; i < n; ++i) {
            // .at() mirrors Java's get(i), which throws when data2 is shorter than data1
            numerator += (data1[i] - mean1) * (data2.at(i) - mean2);
        }

        double sum1 = 0.0;
        for (double x : data1) sum1 += (x - mean1) * (x - mean1);
        double sum2 = 0.0;
        for (double x : data2) sum2 += (x - mean2) * (x - mean2);
        double denominator = std::sqrt(sum1) * std::sqrt(sum2);

        return denominator != 0.0 ? numerator / denominator : 0.0;
    }

    static double skewness(const std::vector<double>& data) {
        int n = static_cast<int>(data.size());
        double mean = meanOrZero(data);

        double sqSum = 0.0;
        for (double x : data) sqSum += (x - mean) * (x - mean);
        double variance = n > 0 ? sqSum / n : 0.0;   // average().orElse(0)
        double stdDeviation = std::sqrt(variance);

        if (stdDeviation == 0.0) {
            return 0.0;
        }

        double cubeSum = 0.0;
        for (double x : data) cubeSum += (x - mean) * (x - mean) * (x - mean);

        return cubeSum * n / ((n - 1) * (n - 2) * std::pow(stdDeviation, 3.0));
    }

    static double kurtosis(const std::vector<double>& data) {
        int n = static_cast<int>(data.size());
        double mean = meanOrZero(data);

        double sqSum = 0.0;
        for (double x : data) sqSum += (x - mean) * (x - mean);
        double stdDev = std::sqrt(n > 0 ? sqSum / n : 0.0);

        if (stdDev == 0.0) {
            return std::numeric_limits<double>::quiet_NaN();
        }

        double fourthSum = 0.0;
        for (double x : data) fourthSum += std::pow(x - mean, 4.0);   // centeredData then pow(x, 4)
        double fourthMoment = n > 0 ? fourthSum / n : 0.0;

        return (fourthMoment / std::pow(stdDev, 4.0)) - 3.0;
    }

    static std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
        std::vector<double> result;
        result.reserve(data.size());
        for (double x : data) {
            result.push_back((1 / (sigma * std::sqrt(2 * M_PI))) *
                             std::exp(-0.5 * std::pow((x - mu) / sigma, 2.0)));
        }
        return result;
    }

private:
    // Mirrors stream().mapToDouble(...).average().orElse(0)
    static double meanOrZero(const std::vector<double>& data) {
        if (data.empty()) return 0.0;
        double sum = 0.0;
        for (double x : data) sum += x;
        return sum / static_cast<double>(data.size());
    }
};