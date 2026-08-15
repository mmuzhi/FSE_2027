#include <vector>
#include <algorithm>

class MetricsCalculator {
public:
    int true_positives = 0;
    int false_positives = 0;
    int false_negatives = 0;
    int true_negatives = 0;

    void update(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        size_t n = std::min(predicted_labels.size(), true_labels.size());
        for (size_t i = 0; i < n; ++i) {
            int predicted = predicted_labels[i];
            int true_label = true_labels[i];
            if (predicted == 1 && true_label == 1) {
                true_positives += 1;
            } else if (predicted == 1 && true_label == 0) {
                false_positives += 1;
            } else if (predicted == 0 && true_label == 1) {
                false_negatives += 1;
            } else if (predicted == 0 && true_label == 0) {
                true_negatives += 1;
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
        update(predicted_labels, true_labels);
        double precision_val = precision(predicted_labels, true_labels);
        double recall_val = recall(predicted_labels, true_labels);
        if (precision_val + recall_val == 0.0) {
            return 0.0;
        }
        return (2.0 * precision_val * recall_val) / (precision_val + recall_val);
    }

    double accuracy(const std::vector<int>& predicted_labels, const std::vector<int>& true_labels) {
        update(predicted_labels, true_labels);
        int total = true_positives + true_negatives + false_positives + false_negatives;
        if (total == 0) {
            return 0.0;
        }
        return static_cast<double>(true_positives + true_negatives) / total;
    }
};