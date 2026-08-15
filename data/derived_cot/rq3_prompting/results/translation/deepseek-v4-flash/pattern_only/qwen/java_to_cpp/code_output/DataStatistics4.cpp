#include <vector>
#include <cmath>
#include <numeric>
#include <limits>

namespace DataStatistics4 {

namespace {
double average(const std::vector<double>& data) {
    if (data.empty()) return 0.0;
    double sum = std::accumulate(data.begin(), data.end(), 0.0);
    return sum / data.size();
}
} // anonymous namespace

double correlationCoefficient(const std::vector<double>& data1, const std::vector<double>& data2) {
    int n = static_cast<int>(data1.size());
    double mean1 = average(data1);
    double mean2 = average(data2);

    double numerator = 0.0;
    for (int i = 0; i < n; ++i) {
        numerator += (data1[i] - mean1) * (data2.at(i) - mean2);
    }

    double sumSq1 = 0.0;
    for (double x : data1) {
        double d = x - mean1;
        sumSq1 += d * d;
    }

    double sumSq2 = 0.0;
    for (double x : data2) {
        double d = x - mean2;
        sumSq2 += d * d;
    }

    double denominator = std::sqrt(sumSq1) * std::sqrt(sumSq2);
    return denominator != 0.0 ? numerator / denominator : 0.0;
}

double skewness(const std::vector<double>& data) {
    int n = static_cast<int>(data.size());
    double mean = average(data);

    double sumSq = 0.0;
    for (double x : data) {
        double d = x - mean;
        sumSq += d * d;
    }
    double variance = data.empty() ? 0.0 : sumSq / n;
    double stdDeviation = std::sqrt(variance);

    if (stdDeviation == 0.0) {
        return 0.0;
    }

    double sumCubes = 0.0;
    for (double x : data) {
        double d = x - mean;
        sumCubes += d * d * d;
    }

    return sumCubes * n / ((n - 1) * (n - 2) * std::pow(stdDeviation, 3));
}

double kurtosis(const std::vector<double>& data) {
    int n = static_cast<int>(data.size());
    double mean = average(data);

    double sumSq = 0.0;
    for (double x : data) {
        double d = x - mean;
        sumSq += d * d;
    }
    double variance = data.empty() ? 0.0 : sumSq / n;
    double stdDev = std::sqrt(variance);

    if (stdDev == 0.0) {
        return std::numeric_limits<double>::quiet_NaN();
    }

    double sumFourth = 0.0;
    for (double x : data) {
        double d = x - mean;
        sumFourth += d * d * d * d;
    }
    double fourthMoment = data.empty() ? 0.0 : sumFourth / n;

    return (fourthMoment / std::pow(stdDev, 4)) - 3.0;
}

std::vector<double> pdf(const std::vector<double>& data, double mu, double sigma) {
    const double PI = 3.14159265358979323846;
    double coeff = 1.0 / (sigma * std::sqrt(2.0 * PI));

    std::vector<double> result;
    result.reserve(data.size());

    for (double x : data) {
        double z = (x - mu) / sigma;
        result.push_back(coeff * std::exp(-0.5 * z * z));
    }

    return result;
}

} // namespace DataStatistics4