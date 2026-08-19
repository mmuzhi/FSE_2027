#include <vector>
#include <algorithm>

class MetricsCalculator {
public:
    int true_positives;
    int false_positives;
    int false_negatives;
    int true_negatives;

    MetricsCalculator()
        : true_positives(0), false_positives(0), false_negatives(0), true_negatives(0) {}

    void update(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        // zip semantics: iterate only over the shorter length;
        // values other than 0/1 fall through all branches (ignored), as in Python.
        const size_t n = std::min(predicted_labels.size(), true_labels.size());
        for (size_t i = 0; i < n; ++i) {
            const int predicted = predicted_labels[i];
            const int true_label = true_labels[i];
            if (predicted == 1 && true_label == 1) {
                ++true_positives;
            } else if (predicted == 1 && true_label == 0) {
                ++false_positives;
            } else if (predicted == 0 && true_label == 1) {
                ++false_negatives;
            } else if (predicted == 0 && true_label == 0) {
                ++true_negatives;
            }
        }
    }

    double precision(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        if (true_positives + false_positives == 0) {
            return 0.0;
        }
        return static_cast<double>(true_positives) / (true_positives + false_positives);
    }

    double recall(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        if (true_positives + false_negatives == 0) {
            return 0.0;
        }
        return static_cast<double>(true_positives) / (true_positives + false_negatives);
    }

    double f1_score(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        // Preserves the original stateful behavior: update is applied three times
        // (here, then again inside precision, then again inside recall).
        update(predicted_labels, true_labels);
        const double p = precision(predicted_labels, true_labels);
        const double r = recall(predicted_labels, true_labels);
        if (p + r == 0.0) {
            return 0.0;
        }
        return (2 * p * r) / (p + r);
    }

    double accuracy(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        const long long total = static_cast<long long>(true_positives) + true_negatives
                              + false_positives + false_negatives;
        if (total == 0) {
            return 0.0;
        }
        return static_cast<double>(true_positives + true_negatives) / static_cast<double>(total);
    }
};