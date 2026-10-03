#include <iostream>
#include <vector>

struct MetricsCalculator {
    int truePositives;
    int falsePositives;
    int falseNegatives;
    int trueNegatives;

    MetricsCalculator() : 
        truePositives(0), falsePositives(0), 
        falseNegatives(0), trueNegatives(0) {}

    void update(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        for (size_t i = 0; i < predictedLabels.size(); ++i) {
            if (predictedLabels[i] == 1 && trueLabels[i] == 1) {
                truePositives++;
            } else if (predictedLabels[i] == 1 && trueLabels[i] == 0) {
                falsePositives++;
            } else if (predictedLabels[i] == 0 && trueLabels[i] == 1) {
                falseNegatives++;
            } else if (predictedLabels[i] == 0 && trueLabels[i] == 0) {
                trueNegatives++;
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
        double precision = this->precision(predictedLabels, trueLabels);
        double recall = this->recall(predictedLabels, trueLabels);
        if (precision + recall == 0.0) {
            return 0.0;
        }
        return (2 * precision * recall) / (precision + recall);
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