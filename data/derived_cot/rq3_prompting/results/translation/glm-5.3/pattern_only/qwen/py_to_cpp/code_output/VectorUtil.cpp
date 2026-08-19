#include <algorithm>
#include <cmath>
#include <stdexcept>
#include <string>
#include <vector>
#include <map>

// Maps Python's ZeroDivisionError semantics
struct ZeroDivisionError : std::runtime_error {
    explicit ZeroDivisionError(const std::string& msg) : std::runtime_error(msg) {}
};

class VectorUtil {
public:
    static double similarity(const std::vector<double>& vector_1,
                             const std::vector<double>& vector_2) {
        return dot(unitvec(vector_1), unitvec(vector_2));
    }

    static std::vector<double> cosine_similarities(
            const std::vector<double>& vector_1,
            const std::vector<std::vector<double>>& vectors_all) {
        const double norm = vector_norm(vector_1);
        std::vector<double> similarities;
        similarities.reserve(vectors_all.size());
        for (const auto& v : vectors_all) {
            const double all_norm = vector_norm(v);
            const double dot_product = dot(v, vector_1);
            similarities.push_back(dot_product / (norm * all_norm));
        }
        return similarities;
    }

    static double n_similarity(const std::vector<std::vector<double>>& vector_list_1,
                               const std::vector<std::vector<double>>& vector_list_2) {
        if (vector_list_1.empty() || vector_list_2.empty()) {
            throw ZeroDivisionError("At least one of the passed list is empty.");
        }
        return dot(unitvec(mean_axis0(vector_list_1)),
                   unitvec(mean_axis0(vector_list_2)));
    }

    static std::map<std::string, double> compute_idf_weight_dict(
            int total_num, const std::map<std::string, double>& number_dict) {
        std::map<std::string, double> result;
        for (const auto& kv : number_dict) {
            // log((total_num + 1) / (count + 1)), natural log like np.log
            result[kv.first] = std::log(static_cast<double>(total_num + 1) /
                                        (kv.second + 1.0));
        }
        return result;
    }

private:
    static double dot(const std::vector<double>& a, const std::vector<double>& b) {
        double s = 0.0;
        const size_t n = std::min(a.size(), b.size());
        for (size_t i = 0; i < n; ++i) s += a[i] * b[i];
        return s;
    }

    static double vector_norm(const std::vector<double>& v) {
        double s = 0.0;
        for (double x : v) s += x * x;
        return std::sqrt(s);
    }

    // gensim matutils.unitvec: zero-norm vector returned unchanged
    static std::vector<double> unitvec(const std::vector<double>& v) {
        const double n = vector_norm(v);
        if (n == 0.0) return v;
        std::vector<double> out;
        out.reserve(v.size());
        for (double x : v) out.push_back(x / n);
        return out;
    }

    // numpy array(...).mean(axis=0): column-wise mean
    static std::vector<double> mean_axis0(const std::vector<std::vector<double>>& vs) {
        std::vector<double> sum(vs[0].size(), 0.0);
        for (const auto& v : vs)
            for (size_t i = 0; i < v.size(); ++i) sum[i] += v[i];
        std::vector<double> mean;
        mean.reserve(sum.size());
        for (double s : sum) mean.push_back(s / static_cast<double>(vs.size()));
        return mean;
    }
};