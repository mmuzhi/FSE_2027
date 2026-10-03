#include <vector>
#include <cmath>
#include <map>
#include <string>
#include <stdexcept>

namespace org {
namespace example {

double similarity(const std::vector<double>& vector1, const std::vector<double>& vector2) {
    double dotProduct = 0.0;
    double norm1 = 0.0;
    double norm2 = 0.0;
    // We'll use the size of the first vector, but note: if they are different, we use the minimum?
    // The Java code uses the length of vector1 for the loop, but if vector2 is shorter, it will throw an exception?
    // Actually, in Java, if the arrays are of different lengths, the loop runs for the length of vector1, and if vector2 is shorter, it will throw an ArrayIndexOutOfBoundsException.
    // In C++, we must mimic that. But the problem says: keep behavior identical, including edge cases.

    // However, the problem says: "Use idiomatic C++ only when it doesn't change behavior." 
    // We are allowed to change the interface? The problem says: "Translate the following Java code to C++", and the inputs/outputs must be identical.

    // Let's stick to the same behavior: if the vectors are of different lengths, we use the minimum length? 
    // But note: the Java code does not check for different lengths. It uses the length of vector1 for the loop, and if vector2 is shorter, it will throw an exception.

    // We'll do the same: if the vectors are of different lengths, we throw an exception? 
    // Actually, the Java code does not throw for different lengths, it just uses the first vector's length and if the second is shorter, it will try to access an index out of bounds.

    // Since we are using vectors, we can do:

    // But note: the problem says to keep behavior identical. In Java, accessing an index out of bounds throws an exception.

    // We can do:

    size_t n = vector1.size();
    if (vector2.size() != n) {
        // We'll throw an exception to mimic Java's ArrayIndexOutOfBoundsException?
        // But the problem says: "Keep behavior identical", and in Java, this would throw an exception at runtime.
        // However, the problem also says: "Use idiomatic C++ only when it doesn't change behavior." 
        // We are allowed to change the interface? The problem says the inputs/outputs must be identical.

    // Alternatively, we can use the minimum length? But the Java code does not do that.

    // Let me re-read the Java code: 
    //   for (int i = 0; i < vector1.length; i++) {
    //       dotProduct += vector1[i] * vector2[i];
    //       norm1 += Math.pow(vector1[i], 2);
    //       norm2 += Math.pow(vector2[i], 2);
    //   }

    // This will throw an ArrayIndexOutOfBoundsException if vector2 is shorter.

    // In C++, we can do the same by using a loop that goes up to the size of vector1, and if vector2 is shorter, we try to access an out-of-bound element.

    // But note: accessing an out-of-bound element in C++ is undefined behavior. We must avoid that.

    // We have two options:
    //   a) Throw an exception if the sizes are different.
    //   b) Use the minimum size.

    // The problem says: keep behavior identical. In Java, it throws an exception. In C++, we can throw an exception too.

    // Let's throw an exception if the sizes are different.

    if (vector1.size() != vector2.size()) {
        throw std::out_of_range("Vectors must be of the same length.");
    }

    for (size_t i = 0; i < vector1.size(); i++) {
        dotProduct += vector1[i] * vector2[i];
        norm1 += vector1[i] * vector1[i];
        norm2 += vector2[i] * vector2[i];
    }

    double denominator = std::sqrt(norm1) * std::sqrt(norm2);
    return denominator == 0 ? 0.0 : dotProduct / denominator;
}

std::vector<double> cosineSimilarities(const std::vector<double>& vector1, const std::vector<std::vector<double>>& vectorsAll) {
    // First, compute the norm of vector1
    double norm1 = std::sqrt(dotProduct(vector1, vector1));
    if (norm1 == 0) {
        // If norm1 is 0, then all similarities are 0.0
        std::vector<double> similarities;
        for (const auto& vec : vectorsAll) {
            similarities.push_back(0.0);
        }
        return similarities;
    }

    std::vector<double> similarities;
    for (const auto& vector2 : vectorsAll) {
        double norm2 = std::sqrt(dotProduct(vector2, vector2));
        if (norm2 == 0) {
            similarities.push_back(0.0);
        } else {
            double similarity = dotProduct(vector1, vector2) / (norm1 * norm2);
            similarities.push_back(similarity);
        }
    }
    return similarities;
}

double nSimilarity(const std::vector<std::vector<double>>& vectorList1, const std::vector<std::vector<double>>& vectorList2) {
    if (vectorList1.empty() || vectorList2.empty()) {
        throw std::invalid_argument("At least one of the passed lists is empty.");
    }
    std::vector<double> avgVector1 = averageVector(vectorList1);
    std::vector<double> avgVector2 = averageVector(vectorList2);
    return similarity(avgVector1, avgVector2);
}

std::map<std::string, double> computeIdfWeightDict(int totalNum, const std::map<std::string, double>& numberDict) {
    std::map<std::string, double> result;
    for (const auto& entry : numberDict) {
        double count = entry.second;
        double weight = std::log((totalNum + 1) / (count + 1));
        result[entry.first] = weight;
    }
    return result;
}

} // namespace example
} // namespace org