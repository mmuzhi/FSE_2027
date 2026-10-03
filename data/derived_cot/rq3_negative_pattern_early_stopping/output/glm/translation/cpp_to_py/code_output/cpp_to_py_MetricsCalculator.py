class MetricsCalculator:
    def __init__(self):
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.true_negatives = 0

    def update(self, predicted_labels, true_labels):
        for i in range(len(predicted_labels)):
            predicted = predicted_labels[i]
            true_label = true_labels[i]

            if predicted == 1 and true_label == 1:
                self.true_positives += 1
            elif predicted == 1 and true_label == 0:
                self.false_positives += 1
            elif predicted == 0 and true_label == 1:
                self.false_negatives += 1
            elif predicted == 0 and true_label == 0:
                self.true_negatives += 1

    def precision(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        if self.true_positives + self.false_positives == 0:
            return 0.0
        return float(self.true_positives) / (self.true_positives + self.false_positives)

    def recall(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        if self.true_positives + self.false_negatives == 0:
            return 0.0
        return float(self.true_positives) / (self.true_positives + self.false_negatives)

    def f1_score(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        precision_value = self.precision(predicted_labels, true_labels)
        recall_value = self.recall(predicted_labels, true_labels)
        if precision_value + recall_value == 0.0:
            return 0.0
        return 2.0 * precision_value * recall_value / (precision_value + recall_value)

    def accuracy(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        total = self.true_positives + self.true_negatives + self.false_positives + self.false_negatives
        if total == 0:
            return 0.0
        return float(self.true_positives + self.true_negatives) / total