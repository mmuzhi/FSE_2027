class MetricsCalculator:
    def __init__(self):
        self.truePositives = 0
        self.falsePositives = 0
        self.falseNegatives = 0
        self.trueNegatives = 0

    def update(self, predictedLabels, trueLabels):
        if len(predictedLabels) != len(trueLabels):
            raise ValueError("Both arrays must have the same length")
        for i in range(len(predictedLabels)):
            if predictedLabels[i] == 1 and trueLabels[i] == 1:
                self.truePositives += 1
            elif predictedLabels[i] == 1 and trueLabels[i] == 0:
                self.falsePositives += 1
            elif predictedLabels[i] == 0 and trueLabels[i] == 1:
                self.falseNegatives += 1
            elif predictedLabels[i] == 0 and trueLabels[i] == 0:
                self.trueNegatives += 1

    def precision(self, predictedLabels, trueLabels):
        self.update(predictedLabels, trueLabels)
        total_positive = self.truePositives + self.falsePositives
        if total_positive == 0:
            return 0.0
        return float(self.truePositives) / total_positive

    def recall(self, predictedLabels, trueLabels):
        self.update(predictedLabels, trueLabels)
        total_true = self.truePositives + self.falseNegatives
        if total_true == 0:
            return 0.0
        return float(self.truePositives) / total_true

    def f1Score(self, predictedLabels, trueLabels):
        self.update(predictedLabels, trueLabels)
        precision_val = self.precision(predictedLabels, trueLabels)
        recall_val = self.recall(predictedLabels, trueLabels)
        if precision_val + recall_val == 0.0:
            return 0.0
        return 2 * (precision_val * recall_val) / (precision_val + recall_val)

    def accuracy(self, predictedLabels, trueLabels):
        self.update(predictedLabels, trueLabels)
        total = self.truePositives + self.trueNegatives + self.falsePositives + self.falseNegatives
        if total == 0:
            return 0.0
        return float(self.truePositives + self.trueNegatives) / total

if __name__ == "__main__":
    mc = MetricsCalculator()
    predictedLabels = [1, 1, 0, 0]
    trueLabels = [1, 0, 0, 1]
    print(mc.precision(predictedLabels, trueLabels))
    print(mc.recall(predictedLabels, trueLabels))
    print(mc.f1Score(predictedLabels, trueLabels))
    print(mc.accuracy(predictedLabels, trueLabels))