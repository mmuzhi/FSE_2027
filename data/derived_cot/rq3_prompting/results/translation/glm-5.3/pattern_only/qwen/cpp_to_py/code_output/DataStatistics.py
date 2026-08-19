import math


class DataStatistics:
    @staticmethod
    def _round2(x):
        # std::round: round half away from zero (Python's round is banker's rounding)
        return math.copysign(math.floor(abs(x) * 100 + 0.5), x) / 100

    def mean(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        total = 0.0
        for value in data:
            total += value
        return self._round2(total / len(data))

    def median(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        data = sorted(data)  # by-value parameter in C++: sort a copy
        n = len(data)
        if n % 2 == 0:
            return self._round2((data[n // 2 - 1] + data[n // 2]) / 2)
        else:
            return data[n // 2]

    def mode(self, data):
        if not data:
            raise ValueError("Data vector is empty.")

        count_map = {}
        for num in data:
            count_map[num] = count_map.get(num, 0) + 1

        max_count = 0
        for count in count_map.values():
            if count > max_count:
                max_count = count

        modes = []
        for key in sorted(count_map.keys()):  # std::map iterates in ascending key order
            if count_map[key] == max_count:
                modes.append(key)

        return modes