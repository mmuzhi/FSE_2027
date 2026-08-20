#include <vector>
#include <algorithm>
#include <cstddef>

class MetricsCalculator {
public:
    // Initialize the number of all four samples to 0
    int true_positives = 0;
    int false_positives = 0;
    int false_negatives = 0;
    int true_negatives = 0;

    // Update the counts of the four sample types.
    // Mirrors Python's zip(): iteration stops at the shorter of the two lists.
    void update(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        const std::size_t n = std::min(predicted_labels.size(), true_labels.size());
        for (std::size_t i = 0; i < n; ++i) {
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

    // Calculate precision (also updates counts, like the Python version)
    double precision(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        if (true_positives + false_positives == 0) {
            return 0.0;
        }
        return static_cast<double>(true_positives) / (true_positives + false_positives);
    }

    // Calculate recall (also updates counts, like the Python version)
    double recall(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        if (true_positives + false_negatives == 0) {
            return 0.0;
        }
        return static_cast<double>(true_positives) / (true_positives + false_negatives);
    }

    // Calculate F1 score, the harmonic mean of precision and recall.
    // Note: like the Python original, update() runs once here and once inside
    // each precision()/recall() call, so counts are updated three times total.
    double f1_score(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        const double p = precision(predicted_labels, true_labels);
        const double r = recall(predicted_labels, true_labels);
        if (p + r == 0.0) {
            return 0.0;
        }
        return (2.0 * p * r) / (p + r);
    }

    // Calculate accuracy (also updates counts, like the Python version)
    double accuracy(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        const int total = true_positives + true_negatives + false_positives + false_negatives;
        if (total == 0) {
            return 0.0;
        }
        return static_cast<double>(true_positives + true_negatives) / total;
    }
};