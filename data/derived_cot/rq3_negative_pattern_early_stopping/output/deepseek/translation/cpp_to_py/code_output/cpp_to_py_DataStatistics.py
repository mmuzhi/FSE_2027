import math

class DataStatistics:
    def mean(self, data: list[float]) -> float:
        if not data:
            raise ValueError('Data vector is empty.')
        total = sum(data)
        result = total / len(data)
        return self._round_half_up(result * 100) / 100

    def median(self, data: list[float]) -> float:
        if not data:
            raise ValueError('Data vector is empty.')
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            avg = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
            return self._round_half_up(avg * 100) / 100
        else:
            return sorted_data[n//2]

    def mode(self, data: list[int]) -> list[int]:
        if not data:
            raise ValueError('Data vector is empty.')
        count_map = {}
        for num in data:
            count_map[num] = count_map.get(num, 0) + 1
        max_count = max(count_map.values())
        modes = [key for key, value in count_map.items() if value == max_count]
        return modes

    @staticmethod
    def _round_half_up(x: float) -> float:
        """Round to nearest integer, rounding half away from zero."""
        if x >= 0:
            return math.floor(x + 0.5)
        else:
            return math.ceil(x - 0.5)