#include <vector>
#include <cmath>
#include <map>
#include <string>
#include <stdexcept>

class VectorUtil {
public:
    static double similarity(const std::vector<double>& vector_1, const std::vector<double>& vector_2) {
        return dot_product(unitvec(vector_1), unitvec(vector_2));
    }

    static std::vector<double> cosine_similarities(const std::vector<double>& vector_1, const std::vector<std::vector<double>>& vectors_all) {
        if (vectors_all.empty()) {
            throw std::out_of_range("axis 1 is out of bounds for array of dimension 1");
        }
        std::size_t dim = vectors_all[0].size();
        for (const auto& v : vectors_all) {
            if (v.size() != dim) {
                throw std::invalid_argument("inhomogeneous shape");
            }
        }
        double norm = vector_norm(vector_1);
        std::vector<double> all_norms;
        all_norms.reserve(vectors_all.size());
        for (const auto& v : vectors_all) {
            all_norms.push_back(vector_norm(v));
        }
        std::vector<double> similarities;
        similarities.reserve(vectors_all.size());
        for (std::size_t i = 0; i < vectors_all.size(); ++i) {
            double dot = dot_product(vectors_all[i], vector_1);
            similarities.push_back(dot / (norm * all_norms[i]));
        }
        return similarities;
    }

    static double n_similarity(const std::vector<std::vector<double>>& vector_list_1, const std::vector<std::vector<double>>& vector_list_2) {
        if (vector_list_1.empty() || vector_list_2.empty()) {
            throw std::domain_error("At least one of the passed list is empty.");
        }
        std::vector<double> mean1 = mean_vector(vector_list_1);
        std::vector<double> mean2 = mean_vector(vector_list_2);
        return dot_product(unitvec(mean1), unitvec(mean2));
    }

    static std::map<std::string, double> compute_idf_weight_dict(int total_num, const std::map<std::string, double>& number_dict) {
        std::vector<std::string> keys;
        std::vector<double> count_list;
        keys.reserve(number_dict.size());
        count_list.reserve(number_dict.size());
        for (const auto& kv : number_dict) {
            keys.push_back(kv.first);
            count_list.push_back(kv.second);
        }
        std::vector<double> a(count_list.size());
        for (std::size_t i = 0; i < count_list.size(); ++i) {
            a[i] = std::log((static_cast<double>(total_num) + 1.0) / (count_list[i] + 1.0));
        }
        std::map<std::string, double> result;
        for (std::size_t i = 0; i < keys.size(); ++i) {
            result[keys[i]] = a[i];
        }
        return result;
    }

private:
    static double dot_product(const std::vector<double>& a, const std::vector<double>& b) {
        if (a.size() != b.size()) {
            throw std::invalid_argument("shapes not aligned");
        }
        double sum = 0.0;
        for (std::size_t i = 0; i < a.size(); ++i) {
            sum += a[i] * b[i];
        }
        return sum;
    }

    static double vector_norm(const std::vector<double>& v) {
        return std::sqrt(dot_product(v, v));
    }

    static std::vector<double> unitvec(const std::vector<double>& v) {
        double n = vector_norm(v);
        if (n > 0.0) {
            std::vector<double> result(v.size());
            for (std::size_t i = 0; i < v.size(); ++i) {
                result[i] = v[i] / n;
            }
            return result;
        } else {
            return v;
        }
    }

    static std::vector<double> mean_vector(const std::vector<std::vector<double>>& vectors) {
        if (vectors.empty()) return {};
        std::size_t dim = vectors[0].size();
        for (const auto& v : vectors) {
            if (v.size() != dim) {
                throw std::invalid_argument("inhomogeneous shape");
            }
        }
        std::vector<double> mean(dim, 0.0);
        for (const auto& v : vectors) {
            for (std::size_t i = 0; i < dim; ++i) {
                mean[i] += v[i];
            }
        }
        for (std::size_t i = 0; i < dim; ++i) {
            mean[i] /= static_cast<double>(vectors.size());
        }
        return mean;
    }
};