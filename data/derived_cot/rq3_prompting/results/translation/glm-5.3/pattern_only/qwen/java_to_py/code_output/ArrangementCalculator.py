class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def count(n, m=None):
        if m is None or n == m:
            return ArrangementCalculator.factorial(n)
        else:
            return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def countAll(n):
        total = 0
        for i in range(1, n + 1):
            total += ArrangementCalculator.count(n, i)
        return total

    def select(self, m=None):
        if m is None:
            m = len(self.datas)
        result = []
        self._selectPermutations([], list(self.datas), m, result)
        return result

    def selectAll(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

    def _selectPermutations(self, prefix, remaining, m, result):
        if len(prefix) == m:
            result.append(list(prefix))
            return
        for i in range(len(remaining)):
            new_prefix = prefix + [remaining[i]]
            new_remaining = remaining[:i] + remaining[i + 1:]
            self._selectPermutations(new_prefix, new_remaining, m, result)

    @staticmethod
    def factorial(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result