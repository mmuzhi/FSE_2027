#include <vector>
#include <string>
#include <unordered_map>
#include <cmath>
#include <stdexcept>

class VectorUtil {
public:
    static double similarity(const std::vector<double>& vector1, const std::vector<double>& vector2) {
        double dotProduct = 0.0;
        double norm1 = 0.0;
        double norm2 = 0.0;
        for (size_t i = 0; i < vector1.size(); i++) {
            if (i >= vector2.size()) {
                throw std::out_of_range("Vector index out of bounds");
            }
            dotProduct += vector1[i] * vector2[i];
            norm1 += std::pow(vector1[i], 2.0);
            norm2 += std::pow(vector2[i], 2.0);
        }
        double denominator = std::sqrt(norm1) * std::sqrt(norm2);
        return denominator == 0.0 ? 0.0 : dotProduct / denominator;
    }

    static std::vector<double> cosineSimilarities(const std::vector<double>& vector1, const std::vector<std::vector<double>>& vectorsAll) {
        std::vector<double> similarities;
        double norm1 = std::sqrt(dotProduct(vector1, vector1));
        if (norm1 == 0.0) {
            for (size_t i = 0; i < vectorsAll.size(); i++) {
                similarities.push_back(0.0);
            }
            return similarities;
        }
        for (const auto& vector2 : vectorsAll) {
            double norm2 = std::sqrt(dotProduct(vector2, vector2));
            if (norm2 == 0.0) {
                similarities.push_back(0.0);
            } else {
                double similarity = dotProduct(vector1, vector2) / (norm1 * norm2);
                similarities.push_back(similarity);
            }
        }
        return similarities;
    }

    static double nSimilarity(const std::vector<std::vector<double>>& vectorList1, const std::vector<std::vector<double>>& vectorList2) {
        if (vectorList1.empty() || vectorList2.empty()) {
            throw std::invalid_argument("At least one of the passed lists is empty.");
        }
        std::vector<double> avgVector1 = averageVector(vectorList1);
        std::vector<double> avgVector2 = averageVector(vectorList2);
        return similarity(avgVector1, avgVector2);
    }

    static std::unordered_map<std::string, double> computeIdfWeightDict(int totalNum, const std::unordered_map<std::string, double>& numberDict) {
        std::unordered_map<std::string, double> result;
        for (const auto& entry : numberDict) {
            double count = entry.second;
            double weight = std::log((totalNum + 1.0) / (count + 1.0));
            result[entry.first] = weight;
        }
        return result;
    }

private:
    static double dotProduct(const std::vector<double>& vector1, const std::vector<double>& vector2) {
        double result = 0.0;
        for (size_t i = 0; i < vector1.size(); i++) {
            if (i >= vector2.size()) {
                throw std::out_of_range("Vector index out of bounds");
            }
            result += vector1[i] * vector2[i];
        }
        return result;
    }

    static std::vector<double> averageVector(const std::vector<std::vector<double>>& vectors) {
        std::vector<double> avgVector(vectors[0].size(), 0.0);
        for (const auto& vector : vectors) {
            for (size_t i = 0; i < vector.size(); i++) {
                avgVector[i] += vector[i];
            }
        }
        for (double& val : avgVector) {
            val /= vectors.size();
        }
        return avgVector;
    }
};