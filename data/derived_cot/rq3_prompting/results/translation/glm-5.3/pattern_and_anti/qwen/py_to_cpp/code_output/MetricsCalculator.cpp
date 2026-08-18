#include <vector>
#include <algorithm>
#include <cstddef>

class MetricsCalculator {
public:
    int true_positives = 0;
    int false_positives = 0;
    int false_negatives = 0;
    int true_negatives = 0;

    void update(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        // zip() semantics: iterate only up to the shorter of the two lists
        const std::size_t n = std::min(predicted_labels.size(), true_labels.size());
        for (std::size_t i = 0; i < n; ++i) {
            const int predicted = predicted_labels[i];
            const int true_val = true_labels[i];
            if (predicted == 1 && true_val == 1) {
                ++true_positives;
            } else if (predicted == 1 && true_val == 0) {
                ++false_positives;
            } else if (predicted == 0 && true_val == 1) {
                ++false_negatives;
            } else if (predicted == 0 && true_val == 0) {
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
        // Preserves the Python quirk: update runs, then precision() and recall()
        // each call update() again, so counters accumulate multiple times.
        update(predicted_labels, true_labels);
        const double prec = precision(predicted_labels, true_labels);
        const double rec = recall(predicted_labels, true_labels);
        if (prec + rec == 0.0) {
            return 0.0;
        }
        return (2 * prec * rec) / (prec + rec);
    }

    double accuracy(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        const int total = true_positives + true_negatives + false_positives + false_negatives;
        if (total == 0) {
            return 0.0;
        }
        return static_cast<double>(true_positives + true_negatives) / total;
    }
};