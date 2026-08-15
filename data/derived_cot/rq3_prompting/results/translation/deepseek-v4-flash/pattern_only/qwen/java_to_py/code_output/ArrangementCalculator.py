class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def _to_java_int(x):
        x &= 0xFFFFFFFF
        if x >= 0x80000000:
            x -= 0x100000000
        return x

    @staticmethod
    def _java_div(a, b):
        q = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            q = -q
        return ArrangementCalculator._to_java_int(q)

    @staticmethod
    def count(n, m):
        if m is None or n == m:
            return ArrangementCalculator.factorial(n)
        else:
            return ArrangementCalculator._java_div(
                ArrangementCalculator.factorial(n),
                ArrangementCalculator.factorial(n - m)
            )

    @staticmethod
    def countAll(n):
        total = 0
        for i in range(1, n + 1):
            total = ArrangementCalculator._to_java_int(total + ArrangementCalculator.count(n, i))
        return total

    @staticmethod
    def factorial(n):
        result = 1
        for i in range(2, n + 1):
            result = ArrangementCalculator._to_java_int(result * i)
        return result

    def select(self, m):
        if m is None:
            m = len(self.datas)
        result = []
        self._select_permutations([], list(self.datas), m, result)
        return result

    def selectAll(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

    def _select_permutations(self, prefix, remaining, m, result):
        if len(prefix) == m:
            result.append(list(prefix))
            return
        for i in range(len(remaining)):
            new_prefix = list(prefix)
            new_prefix.append(remaining[i])
            new_remaining = list(remaining)
            new_remaining.pop(i)
            self._select_permutations(new_prefix, new_remaining, m, result)