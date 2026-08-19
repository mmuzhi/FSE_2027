import math


class DataStatistics:

    @staticmethod
    def _round2(value):
        # Java Math.round semantics: floor(value * 100.0 + 0.5) / 100.0 (half-up,
        # matching Java's round(double) rather than Python's banker's rounding)
        return math.floor(value * 100.0 + 0.5) / 100.0

    def mean(self, data):
        n = len(data)
        if n == 0:
            # Java: 0.0/0 -> NaN; Math.round(NaN) -> 0 -> 0.0
            return 0.0
        total = float(sum(data))
        return self._round2(total / n)

    def median(self, data):
        sorted_data = sorted(data)
        n = len(sorted_data)

        if n % 2 == 0:
            middle = n // 2
            return self._round2(
                (sorted_data[middle - 1] + sorted_data[middle]) / 2.0
            )
        else:
            middle = n // 2
            return float(sorted_data[middle])

    def mode(self, data):
        frequency = {}
        for e in data:
            frequency[e] = frequency.get(e, 0) + 1

        max_count = max(frequency.values())

        return sorted(
            key for key, count in frequency.items() if count == max_count
        )