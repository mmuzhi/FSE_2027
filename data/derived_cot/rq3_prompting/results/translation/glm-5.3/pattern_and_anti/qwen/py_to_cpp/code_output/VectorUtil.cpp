#include <algorithm>
#include <cmath>
#include <cstddef>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

// Analog of Python's ZeroDivisionError.
class ZeroDivisionError : public std::runtime_error {
public:
    explicit ZeroDivisionError(const std::string& message)
        : std::runtime_error(message) {}
};

class VectorUtil {
public:
    // Compute the cosine similarity between one vector and another vector.
    static double similarity(const std::vector<double>& vector_1,
                             const std::vector<double>& vector_2) {
        return dot(unitvec(vector_1), unitvec(vector_2));
    }

    // Compute cosine similarities between one vector and a set of other vectors.
    static std::vector<double> cosine_similarities(
            const std::vector<double>& vector_1,
            const std::vector<std::vector<double>>& vectors_all) {
        const double norm = vector_norm(vector_1);
        std::vector<double> similarities;
        similarities.reserve(vectors_all.size());
        for (const std::vector<double>& row : vectors_all) {
            // No unitvec protection here (as in Python): zero norms yield NaN/Inf
            // via IEEE-754 semantics, matching numpy.
            similarities.push_back(dot(row, vector_1) / (norm * vector_norm(row)));
        }
        return similarities;
    }

    // Compute cosine similarity between two sets of vectors.
    static double n_similarity(const std::vector<std::vector<double>>& vector_list_1,
                               const std::vector<std::vector<double>>& vector_list_2) {
        if (vector_list_1.empty() || vector_list_2.empty()) {
            throw ZeroDivisionError("At least one of the passed list is empty.");
        }
        return dot(unitvec(mean_axis0(vector_list_1)),
                   unitvec(mean_axis0(vector_list_2)));
    }

    // Calculate log((total_num + 1) / (count + 1)) for each count in number_dict.
    static std::map<std::string, double> compute_idf_weight_dict(
            int total_num, const std::map<std::string, double>& number_dict) {
        std::map<std::string, double> result;
        for (const auto& entry : number_dict) {
            result[entry.first] =
                std::log(static_cast<double>(total_num + 1) / (entry.second + 1.0));
        }
        return result;
    }

private:
    static double dot(const std::vector<double>& a, const std::vector<double>& b) {
        if (a.size() != b.size()) {
            // numpy dot raises on mismatched shapes.
            throw std::invalid_argument("vectors are not aligned");
        }
        double sum = 0.0;
        for (std::size_t i = 0; i < a.size(); ++i) {
            sum += a[i] * b[i];
        }
        return sum;
    }

    static double vector_norm(const std::vector<double>& v) {
        double sum = 0.0;
        for (double x : v) {
            sum += x * x;
        }
        return std::sqrt(sum);
    }

    // gensim matutils.unitvec (l2): returns v / ||v|| when ||v|| > 0,
    // otherwise returns v unchanged (gensim's zero-norm behavior).
    static std::vector<double> unitvec(const std::vector<double>& v) {
        const double norm = vector_norm(v);
        if (norm > 0.0) {
            std::vector<double> out;
            out.reserve(v.size());
            for (double x : v) {
                out.push_back(x / norm);
            }
            return out;
        }
        return v;
    }

    // numpy array(list).mean(axis=0): column-wise mean (rows share one dim).
    static std::vector<double> mean_axis0(
            const std::vector<std::vector<double>>& rows) {
        std::vector<double> mean = rows[0];
        for (std::size_t r = 1; r < rows.size(); ++r) {
            for (std::size_t c = 0; c < mean.size(); ++c) {
                mean[c] += rows[r][c];
            }
        }
        const double n = static_cast<double>(rows.size());
        for (double& value : mean) {
            value /= n;
        }
        return mean;
    }
};