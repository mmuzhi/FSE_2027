#include <vector>
#include <map>
#include <string>
#include <cmath>
#include <stdexcept>

class VectorUtil {
public:
    static double l2_norm(const std::vector<double>& v) {
        double sum = 0.0;
        for (double x : v) {
            sum += x * x;
        }
        return std::sqrt(sum);
    }

    static std::vector<double> unitvec(const std::vector<double>& v) {
        double norm = l2_norm(v);
        if (norm == 0.0) {
            return v;
        }
        std::vector<double> result(v.size());
        for (size_t i = 0; i < v.size(); ++i) {
            result[i] = v[i] / norm;
        }
        return result;
    }

    static double dot(const std::vector<double>& a, const std::vector<double>& b) {
        double result = 0.0;
        for (size_t i = 0; i < a.size(); ++i) {
            result += a[i] * b[i];
        }
        return result;
    }

    static double similarity(const std::vector<double>& vector_1, const std::vector<double>& vector_2) {
        return dot(unitvec(vector_1), unitvec(vector_2));
    }

    static std::vector<double> cosine_similarities(const std::vector<double>& vector_1, const std::vector<std::vector<double>>& vectors_all) {
        double norm = l2_norm(vector_1);
        std::vector<double> all_norms;
        all_norms.reserve(vectors_all.size());
        for (const auto& v : vectors_all) {
            all_norms.push_back(l2_norm(v));
        }
        std::vector<double> dot_products;
        dot_products.reserve(vectors_all.size());
        for (const auto& v : vectors_all) {
            dot_products.push_back(dot(v, vector_1));
        }
        std::vector<double> similarities;
        similarities.reserve(vectors_all.size());
        for (size_t i = 0; i < vectors_all.size(); ++i) {
            similarities.push_back(dot_products[i] / (norm * all_norms[i]));
        }
        return similarities;
    }

    static double n_similarity(const std::vector<std::vector<double>>& vector_list_1, const std::vector<std::vector<double>>& vector_list_2) {
        if (vector_list_1.empty() || vector_list_2.empty()) {
            throw std::runtime_error("At least one of the passed list is empty.");
        }

        size_t dim1 = vector_list_1[0].size();
        std::vector<double> mean1(dim1, 0.0);
        for (const auto& v : vector_list_1) {
            for (size_t i = 0; i < dim1; ++i) {
                mean1[i] += v[i];
            }
        }
        for (size_t i = 0; i < dim1; ++i) {
            mean1[i] /= static_cast<double>(vector_list_1.size());
        }

        size_t dim2 = vector_list_2[0].size();
        std::vector<double> mean2(dim2, 0.0);
        for (const auto& v : vector_list_2) {
            for (size_t i = 0; i < dim2; ++i) {
                mean2[i] += v[i];
            }
        }
        for (size_t i = 0; i < dim2; ++i) {
            mean2[i] /= static_cast<double>(vector_list_2.size());
        }

        return dot(unitvec(mean1), unitvec(mean2));
    }

    static std::map<std::string, double> compute_idf_weight_dict(int total_num, const std::map<std::string, double>& number_dict) {
        std::map<int, std::string> index_2_key_map;
        std::vector<double> count_list;
        int index = 0;

        for (const auto& kv : number_dict) {
            index_2_key_map[index] = kv.first;
            count_list.push_back(kv.second);
            index++;
        }

        std::vector<double> a(count_list.size());
        for (size_t i = 0; i < count_list.size(); ++i) {
            a[i] = std::log((static_cast<double>(total_num) + 1.0) / (count_list[i] + 1.0));
        }

        std::map<std::string, double> result;
        for (size_t i = 0; i < a.size(); ++i) {
            std::string key = index_2_key_map[static_cast<int>(i)];
            result[key] = a[i];
        }

        return result;
    }
};