class MetricsCalculator:
    def __init__(self):
        self.truePositives = 0
        self.falsePositives = 0
        self.falseNegatives = 0
        self.trueNegatives = 0

    def update(self, predictedLabels, trueLabels):
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
        if self.truePositives + self.falsePositives == 0:
            return 0.0
        return self.truePositives / (self.truePositives + self.falsePositives)

    def recall(self, predictedLabels, trueLabels):
        self.update(predictedLabels, trueLabels)
        if self.truePositives + self.falseNegatives == 0:
            return 0.0
        return self.truePositives / (self.truePositives + self.falseNegatives)

    def f1Score(self, predictedLabels, trueLabels):
        self.update(predictedLabels, trueLabels)
        p = self.precision(predictedLabels, trueLabels)
        r = self.recall(predictedLabels, trueLabels)
        if p + r == 0.0:
            return 0.0
        return (2 * p * r) / (p + r)

    def accuracy(self, predictedLabels, trueLabels):
        self.update(predictedLabels, trueLabels)
        total = self.truePositives + self.trueNegatives + self.falsePositives + self.falseNegatives
        if total == 0:
            return 0.0
        return (self.truePositives + self.trueNegatives) / total


if __name__ == "__main__":
    mc = MetricsCalculator()
    predictedLabels = [1, 1, 0, 0]
    trueLabels = [1, 0, 0, 1]
    print(mc.precision(predictedLabels, trueLabels))
    print(mc.recall(predictedLabels, trueLabels))
    print(mc.f1Score(predictedLabels, trueLabels))
    print(mc.accuracy(predictedLabels, trueLabels))