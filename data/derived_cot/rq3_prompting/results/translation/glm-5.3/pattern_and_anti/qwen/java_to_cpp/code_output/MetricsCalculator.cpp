#include <iostream>
#include <vector>
#include <string>
#include <charconv>

class MetricsCalculator {
public:
    int truePositives = 0;
    int falsePositives = 0;
    int falseNegatives = 0;
    int trueNegatives = 0;

    MetricsCalculator() = default;

    void update(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        for (std::size_t i = 0; i < predictedLabels.size(); i++) {
            if (predictedLabels[i] == 1 && trueLabels.at(i) == 1) {
                this->truePositives++;
            } else if (predictedLabels[i] == 1 && trueLabels.at(i) == 0) {
                this->falsePositives++;
            } else if (predictedLabels[i] == 0 && trueLabels.at(i) == 1) {
                this->falseNegatives++;
            } else if (predictedLabels[i] == 0 && trueLabels.at(i) == 0) {
                this->trueNegatives++;
            }
        }
    }

    double precision(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        if (this->truePositives + this->falsePositives == 0) {
            return 0.0;
        }
        return static_cast<double>(this->truePositives) / (this->truePositives + this->falsePositives);
    }

    double recall(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        if (this->truePositives + this->falseNegatives == 0) {
            return 0.0;
        }
        return static_cast<double>(this->truePositives) / (this->truePositives + this->falseNegatives);
    }

    double f1Score(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        double prec = precision(predictedLabels, trueLabels);
        double rec = recall(predictedLabels, trueLabels);
        if (prec + rec == 0.0) {
            return 0.0;
        }
        return (2 * prec * rec) / (prec + rec);
    }

    double accuracy(const std::vector<int>& predictedLabels, const std::vector<int>& trueLabels) {
        update(predictedLabels, trueLabels);
        int total = this->truePositives + this->trueNegatives + this->falsePositives + this->falseNegatives;
        if (total == 0) {
            return 0.0;
        }
        return static_cast<double>(this->truePositives + this->trueNegatives) / total;
    }
};

// Mimics Java's System.out.println(double): shortest round-trip form, ".0" appended to integral results.
static void printlnDouble(double value) {
    char buf[32];
    auto res = std::to_chars(buf, buf + sizeof(buf), value);
    std::string s(buf, res.ptr);
    if (s.find('.') == std::string::npos && s.find('e') == std::string::npos) {
        s += ".0";
    }
    std::cout << s << "\n";
}

int main() {
    MetricsCalculator mc;
    std::vector<int> predictedLabels = {1, 1, 0, 0};
    std::vector<int> trueLabels = {1, 0, 0, 1};
    printlnDouble(mc.precision(predictedLabels, trueLabels));
    printlnDouble(mc.recall(predictedLabels, trueLabels));
    printlnDouble(mc.f1Score(predictedLabels, trueLabels));
    printlnDouble(mc.accuracy(predictedLabels, trueLabels));
    return 0;
}