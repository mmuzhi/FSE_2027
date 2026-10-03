class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = list(datas)

    @staticmethod
    def count(n, m=-1):
        if m == -1 or n == m:
            return ArrangementCalculator.factorial(n)
        else:
            return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def count_all(n):
        total = 0
        for i in range(1, n + 1):
            total += ArrangementCalculator.count(n, i)
        return total

    def _permutations_recursive(self, current, remaining, m, result):
        if len(current) == m:
            result.append(current)
        else:
            for i in range(len(remaining)):
                new_current = current + [remaining[i]]
                new_remaining = remaining[:i] + remaining[i + 1:]
                self._permutations_recursive(new_current, new_remaining, m, result)

    def select(self, m=-1):
        result = []
        if m == -1:
            m = len(self.datas)

        current = []
        remaining = list(self.datas)

        self._permutations_recursive(current, remaining, m, result)

        return result

    def select_all(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            partial_result = self.select(i)
            result.extend(partial_result)
        return result

    @staticmethod
    def factorial(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result