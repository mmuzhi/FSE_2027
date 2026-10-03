class DataStatistics:
    @staticmethod
    def mean(data):
        if not data:
            raise ValueError("Data vector is empty.")
        total = sum(data)
        return round(total / len(data), 2)

    @staticmethod
    def median(data):
        if not data:
            raise ValueError("Data vector is empty.")
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return round((sorted_data[n//2 - 1] + sorted_data[n//2]) / 2, 2)
        else:
            return sorted_data[n//2]

    @staticmethod
    def mode(data):
        if not data:
            raise ValueError("Data vector is empty.")
        count_map = {}
        for num in data:
            count_map[num] = count_map.get(num, 0) + 1
        max_count = max(count_map.values())
        modes = [num for num, count in count_map.items() if count == max_count]
        return modes