#include <vector>
#include <cmath>
#include <numeric>
#include <stdexcept>

namespace DataStatistics4 {

double correlationCoefficient(std::vector<double> data1, std::vector<double> data2) {
    if (data1.size() != data2.size()) {
        throw std::out_of_range("Vectors must be of the same size");
    }

    double mean1 = std::accumulate(data1.begin(), data1.end(), 0.0) / data1.size();
    double mean2 = std::accumulate(data2.begin(), data2.end(), 0.0) / data2.size();

    double numerator = 0.0;
    for (int i = 0; i < data1.size(); i++) {
        numerator += (data1[i] - mean1) * (data2[i] - mean2);
    }

    double sum1 = 0.0;
    for (int i = 0; i < data1.size(); i++) {
        sum1 += (data1[i] - mean1) * (data1[i] - mean1);
    }

    double sum2 = 0.0;
    for (int i = 0; i < data2.size(); i++) {
        sum2 += (data2[i] - mean2) * (data2[i] - mean2);
    }

    double denominator = std::sqrt(sum1) * std::sqrt(sum2);

    if (denominator == 0) {
        return 0;
    }

    return numerator / denominator;
}

double skewness(std::vector<double> data) {
    int n = data.size();
    if (n == 0) {
        return 0;
    }

    double mean = std::accumulate(data.begin(), data.end(), 0.0) / n;
    double variance = std::accumulate(data.begin(), data.end(), 0.0, [&](double sum, double x) {
        return sum + (x - mean) * (x - mean);
    }) / n;

    double stdDeviation = std::sqrt(variance);

    if (stdDeviation == 0) {
        return 0;
    }

    double sumCubed = 0.0;
    for (int i = 0; i < n; i++) {
        sumCubed += (data[i] - mean) * (data[i] - mean) * (data[i] - mean);
    }

    double skewness = sumCubed * n / ((n - 1) * (n - 2) * std::pow(stdDeviation, 3));

    return skewness;
}

double kurtosis(std::vector<double> data) {
    int n = data.size();
    if (n == 0) {
        return 0;
    }

    double mean = std::accumulate(data.begin(), data.end(), 0.0) / n;
    double variance = std::accumulate(data.begin(), data.end(), 0.0, [&](double sum, double x) {
        return sum + (x - mean) * (x - mean);
    }) / n;

    double stdDev = std::sqrt(variance);

    if (stdDev == 0) {
        return std::numeric_limits<double>::quiet_NaN();
    }

    double fourthMoment = 0.0;
    for (int i = 0; i < n; i++) {
        double centered = data[i] - mean;
        fourthMoment += centered * centered * centered * centered;
    }

    fourthMoment /= n; // average

    double kurtosisValue = (fourthMoment / (stdDev * stdDev * stdDev * stdDev)) - 3;

    return kurtosisValue;
}

std::vector<double> pdf(std::vector<double> data, double mu, double sigma) {
    std::vector<double> result;
    result.reserve(data.size());
    for (int i = 0; i < data.size(); i++) {
        double x = data[i];
        double value = (1.0 / (sigma * std::sqrt(2 * M_PI))) * std::exp(-0.5 * std::pow((x - mu) / sigma, 2));
        result.push_back(value);
    }
    return result;
}

} // namespace DataStatistics4