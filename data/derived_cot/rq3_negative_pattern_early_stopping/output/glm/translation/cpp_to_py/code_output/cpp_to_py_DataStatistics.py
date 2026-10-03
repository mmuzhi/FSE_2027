import math

class DataStatistics:
    def mean(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        total = sum(data)
        return self._round_half_away_from_zero(total / len(data), 2)

    def median(self, data):
        if not data:
            raise ValueError("Data vector is empty.")
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return self._round_half_away_from_zero((sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2, 2)
        else:
            return sorted_data[n // 2]

    def mode(self, data):
        if not data:
            raise ValueError("Data vector is empty.")

        count_map = {}
        for num in data:
            count_map[num] = count_map.get(num, 0) + 1

        max_count = max(count_map.values())

        modes = [key for key, count in count_map.items() if count == max_count]
        modes.sort()

        return modes

    def _round_half_away_from_zero(self, x, decimals):
        multiplier = 10 ** decimals
        return math.copysign(math.floor(abs(x) * multiplier + 0.5), x) / multiplier