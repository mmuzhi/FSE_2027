#include <vector>
#include <cmath>
#include <stdexcept>
#include <string>
#include <map>

namespace VectorUtil {

// Helper function to compute dot product
template <typename T>
T dot_product(const std::vector<T>& a, const std::vector<T>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must have the same size");
    }
    T result = 0;
    for (size_t i = 0; i < a.size(); ++i) {
        result += a[i] * b[i];
    }
    return result;
}

// Helper function to compute Euclidean norm
template <typename T>
T norm(const std::vector<T>& vec) {
    return std::sqrt(dot_product(vec, vec));
}

// Helper function to compute unit vector
template <typename T>
std::vector<T> unit_vector(const std::vector<T>& vec) {
    auto v = vec;
    T mag = norm(v);
    if (mag == 0) {
        return v; // Return zero vector if norm is zero
    }
    for (auto& x : v) {
        x /= mag;
    }
    return v;
}

// Compute cosine similarity between two vectors
template <typename T>
T similarity(const std::vector<T>& vec1, const std::vector<T>& vec2) {
    auto unit1 = unit_vector(vec1);
    auto unit2 = unit_vector(vec2);
    return dot_product(unit1, unit2);
}

// Compute cosine similarities between one vector and a list of vectors
template <typename T>
std::vector<T> cosine_similarities(const std::vector<T>& vec1, 
                                  const std::vector<std::vector<T>>& vec_list) {
    if (vec1.empty()) {
        throw std::invalid_argument("Input vector must not be empty");
    }
    T norm1 = norm(vec1);
    std::vector<T> norms;
    std::vector<T> dot_products;
    dot_products.reserve(vec_list.size());

    for (const auto& vec : vec_list) {
        if (vec.empty()) {
            norms.push_back(0);
            dot_products.push_back(0);
            continue;
        }
        T mag = norm(vec);
        norms.push_back(mag);
        dot_products.push_back(dot_product(vec, vec1));
    }

    std::vector<T> similarities;
    similarities.reserve(vec_list.size());
    for (size_t i = 0; i < vec_list.size(); ++i) {
        if (norms[i] == 0) {
            similarities.push_back(0);
        } else {
            similarities.push_back(dot_products[i] / (norm1 * norms[i]));
        }
    }
    return similarities;
}

// Compute normalized cosine similarity between two sets of vectors
template <typename T>
T n_similarity(const std::vector<std::vector<T>>& vec_list1, 
               const std::vector<std::vector<T>>& vec_list2) {
    if (vec_list1.empty() || vec_list2.empty()) {
        throw std::invalid_argument("At least one of the passed lists is empty");
    }

    // Compute the mean vector for each list
    std::vector<T> mean1;
    if (!vec_list1.empty()) {
        mean1.resize(vec_list1[0].size(), 0);
        for (const auto& vec : vec_list1) {
            for (size_t i = 0; i < vec.size(); ++i) {
                mean1[i] += vec[i];
            }
        }
        for (auto& x : mean1) {
            x /= vec_list1.size();
        }
    }

    std::vector<T> mean2;
    if (!vec_list2.empty()) {
        mean2.resize(vec_list2[0].size(), 0);
        for (const auto& vec : vec_list2) {
            for (size_t i = 0; i < vec.size(); ++i) {
                mean2[i] += vec[i];
            }
        }
        for (auto& x : mean2) {
            x /= vec_list2.size();
        }
    }

    return similarity(mean1, mean2);
}

// Compute IDF weights for a dictionary of counts
std::map<std::string, double> compute_idf_weight_dict(size_t total_num, 
                                                      const std::map<std::string, double>& count_dict) {
    if (count_dict.empty()) {
        return {};
    }

    // Create a list of counts and map keys to indices
    std::vector<double> count_list;
    std::vector<std::string> keys;
    for (const auto& kv : count_dict) {
        keys.push_back(kv.first);
        count_list.push_back(kv.second);
    }

    // Compute IDF weights
    std::vector<double> idf_weights;
    idf_weights.reserve(count_list.size());
    for (double count : count_list) {
        if (count <= 0) {
            idf_weights.push_back(std::log((total_num + 1) / 1.0)); // Handle zero count
        } else {
            idf_weights.push_back(std::log((total_num + 1) / (count + 1)));
        }
    }

    // Create result map
    std::map<std::string, double> result;
    for (size_t i = 0; i < keys.size(); ++i) {
        result[keys[i]] = idf_weights[i];
    }
    return result;
}

} // namespace VectorUtil