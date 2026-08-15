#include <iostream>
#include <vector>

class MetricsCalculator {
    int truePositives;
    int falsePositives;
    int falseNegatives;
    int trueNegatives;

public:
    MetricsCalculator() : truePositives(0), falsePositives(0), falseNegatives(0), trueNegatives(0) {}

    void update(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        for (std::size_t i = 0; i < predictedLabels.size(); ++i) {
            int pred = predictedLabels.at(i);
            int truth = trueLabels.at(i);
            if (pred == 1 && truth == 1) {
                ++truePositives;
            } else if (pred == 1 && truth == 0) {
                ++falsePositives;
            } else if (pred == 0 && truth == 1) {
                ++falseNegatives;
            } else if (pred == 0 && truth == 0) {
                ++trueNegatives;
            }
        }
    }

    double precision(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        if (truePositives + falsePositives == 0) {
            return 0.0;
        }
        return static_cast<double>(truePositives) / (truePositives + falsePositives);
    }

    double recall(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        if (truePositives + falseNegatives == 0) {
            return 0.0;
        }
        return static_cast<double>(truePositives) / (truePositives + falseNegatives);
    }

    double f1Score(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        double p = precision(predictedLabels, trueLabels);
        double r = recall(predictedLabels, trueLabels);
        if (p + r == 0.0) {
            return 0.0;
        }
        return (2 * p * r) / (p + r);
    }

    double accuracy(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        int total = truePositives + trueNegatives + falsePositives + falseNegatives;
        if (total == 0) {
            return 0.0;
        }
        return static_cast<double>(truePositives + trueNegatives) / total;
    }
};

int main() {
    MetricsCalculator mc;
    std::vector<int> predictedLabels = {1, 1, 0, 0};
    std::vector<int> trueLabels = {1, 0, 0, 1};
    std::cout << mc.precision(predictedLabels, trueLabels) << std::endl;
    std::cout << mc.recall(predictedLabels, trueLabels) << std::endl;
    std::cout << mc.f1Score(predictedLabels, trueLabels) << std::endl;
    std::cout << mc.accuracy(predictedLabels, trueLabels) << std::endl;
    return 0;
}