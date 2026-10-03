#include <iostream>
#include <vector>

class MetricsCalculator {
public:
    int truePositives;
    int falsePositives;
    int falseNegatives;
    int trueNegatives;

    MetricsCalculator() {
        this->truePositives = 0;
        this->falsePositives = 0;
        this->falseNegatives = 0;
        this->trueNegatives = 0;
    }

    void update(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        for (size_t i = 0; i < predictedLabels.size(); i++) {
            if (predictedLabels[i] == 1 && trueLabels[i] == 1) {
                this->truePositives++;
            } else if (predictedLabels[i] == 1 && trueLabels[i] == 0) {
                this->falsePositives++;
            } else if (predictedLabels[i] == 0 && trueLabels[i] == 1) {
                this->falseNegatives++;
            } else if (predictedLabels[i] == 0 && trueLabels[i] == 0) {
                this->trueNegatives++;
            }
        }
    }

    double precision(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        if (this->truePositives + this->falsePositives == 0) {
            return 0.0;
        }
        return (double) this->truePositives / (this->truePositives + this->falsePositives);
    }

    double recall(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        if (this->truePositives + this->falseNegatives == 0) {
            return 0.0;
        }
        return (double) this->truePositives / (this->truePositives + this->falseNegatives);
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
        int total = this->truePositives + this->trueNegatives + this->falsePositives + this->falseNegatives;
        if (total == 0) {
            return 0.0;
        }
        return (double) (this->truePositives + this->trueNegatives) / total;
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