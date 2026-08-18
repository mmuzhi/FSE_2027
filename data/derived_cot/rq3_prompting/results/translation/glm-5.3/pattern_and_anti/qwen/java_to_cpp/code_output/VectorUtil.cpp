#include <cmath>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace org::example {

namespace detail {

double dotProduct(const std::vector<double>& vector1, const std::vector<double>& vector2) {
    double result = 0.0;
    for (std::size_t i = 0; i < vector1.size(); i++) {
        result += vector1[i] * vector2.at(i);
    }
    return result;
}

std::vector<double> averageVector(const std::vector<std::vector<double>>& vectors) {
    std::vector<double> avgVector(vectors.at(0).size(), 0.0);
    for (const auto& vector : vectors) {
        for (std::size_t i = 0; i < vector.size(); i++) {
            avgVector[i] += vector[i];
        }
    }
    for (double& value : avgVector) {
        value /= static_cast<double>(vectors.size());
    }
    return avgVector;
}

} // namespace detail

double similarity(const std::vector<double>& vector1, const std::vector<double>& vector2) {
    double dotProduct = 0.0;
    double norm1 = 0.0;
    double norm2 = 0.0;
    for (std::size_t i = 0; i < vector1.size(); i++) {
        dotProduct += vector1[i] * vector2.at(i);
        norm1 += std::pow(vector1[i], 2.0);
        norm2 += std::pow(vector2.at(i), 2.0);
    }
    double denominator = std::sqrt(norm1) * std::sqrt(norm2);
    return denominator == 0 ? 0.0 : dotProduct / denominator;
}

std::vector<double> cosineSimilarities(const std::vector<double>& vector1,
                                       const std::vector<std::vector<double>>& vectorsAll) {
    std::vector<double> similarities;
    double norm1 = std::sqrt(detail::dotProduct(vector1, vector1));
    if (norm1 == 0) {
        for (std::size_t i = 0; i < vectorsAll.size(); i++) {
            similarities.push_back(0.0);
        }
        return similarities;
    }
    for (const auto& vector2 : vectorsAll) {
        double norm2 = std::sqrt(detail::dotProduct(vector2, vector2));
        if (norm2 == 0) {
            similarities.push_back(0.0);
        } else {
            double sim = detail::dotProduct(vector1, vector2) / (norm1 * norm2);
            similarities.push_back(sim);
        }
    }
    return similarities;
}

double nSimilarity(const std::vector<std::vector<double>>& vectorList1,
                   const std::vector<std::vector<double>>& vectorList2) {
    if (vectorList1.empty() || vectorList2.empty()) {
        throw std::invalid_argument("At least one of the passed lists is empty.");
    }
    std::vector<double> avgVector1 = detail::averageVector(vectorList1);
    std::vector<double> avgVector2 = detail::averageVector(vectorList2);
    return similarity(avgVector1, avgVector2);
}

std::unordered_map<std::string, double>
computeIdfWeightDict(int totalNum, const std::unordered_map<std::string, double>& numberDict) {
    std::unordered_map<std::string, double> result;
    for (const auto& entry : numberDict) {
        double count = entry.second;
        double weight = std::log((totalNum + 1) / (count + 1));
        result.emplace(entry.first, weight);
    }
    return result;
}

} // namespace org::example