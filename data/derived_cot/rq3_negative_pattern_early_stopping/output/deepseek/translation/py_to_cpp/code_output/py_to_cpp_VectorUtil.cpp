#include <vector>
#include <cmath>
#include <stdexcept>
#include <unordered_map>
#include <string>
#include <numeric>

class VectorUtil {
public:
    // Compute cosine similarity between two vectors.
    static double similarity(const std::vector<double>& v1, const std::vector<double>& v2) {
        auto u1 = unitvec(v1);
        auto u2 = unitvec(v2);
        return dot_product(u1, u2);
    }

    // Compute cosine similarities between one vector and a set of vectors.
    static std::vector<double> cosine_similarities(const std::vector<double>& v1,
                                                    const std::vector<std::vector<double>>& vectors_all) {
        double norm_v1 = norm(v1);
        std::vector<double> similarities(vectors_all.size());
        for (size_t i = 0; i < vectors_all.size(); ++i) {
            double dot = dot_product(vectors_all[i], v1);
            double norm_v = norm(vectors_all[i]);
            similarities[i] = dot / (norm_v1 * norm_v);
        }
        return similarities;
    }

    // Compute cosine similarity between two sets of vectors (means).
    static double n_similarity(const std::vector<std::vector<double>>& list1,
                               const std::vector<std::vector<double>>& list2) {
        if (list1.empty() || list2.empty()) {
            throw std::domain_error("At least one of the passed list is empty.");
        }
        auto mean1 = mean_vectors(list1);
        auto mean2 = mean_vectors(list2);
        auto u1 = unitvec(mean1);
        auto u2 = unitvec(mean2);
        return dot_product(u1, u2);
    }

    // Compute IDF weight dictionary.
    static std::unordered_map<std::string, double> compute_idf_weight_dict(
            int total_num,
            const std::unordered_map<std::string, double>& number_dict) {
        std::unordered_map<std::string, double> result;
        for (const auto& entry : number_dict) {
            double val = std::log((total_num + 1.0) / (entry.second + 1.0));
            result[entry.first] = val;
        }
        return result;
    }

private:
    // Compute dot product of two vectors.
    static double dot_product(const std::vector<double>& a, const std::vector<double>& b) {
        double sum = 0.0;
        for (size_t i = 0; i < a.size(); ++i) {
            sum += a[i] * b[i];
        }
        return sum;
    }

    // Compute Euclidean norm.
    static double norm(const std::vector<double>& v) {
        return std::sqrt(dot_product(v, v));
    }

    // Normalize vector to unit vector.
    static std::vector<double> unitvec(const std::vector<double>& v) {
        double n = norm(v);
        if (n == 0.0) return v; // Return zero vector as is
        std::vector<double> u(v.size());
        for (size_t i = 0; i < v.size(); ++i) {
            u[i] = v[i] / n;
        }
        return u;
    }

    // Compute element-wise mean of a list of vectors.
    static std::vector<double> mean_vectors(const std::vector<std::vector<double>>& vecs) {
        if (vecs.empty()) return {};
        size_t dim = vecs[0].size();
        std::vector<double> mean(dim, 0.0);
        for (const auto& v : vecs) {
            for (size_t i = 0; i < dim; ++i) {
                mean[i] += v[i];
            }
        }
        double inv = 1.0 / static_cast<double>(vecs.size());
        for (size_t i = 0; i < dim; ++i) {
            mean[i] *= inv;
        }
        return mean;
    }
};