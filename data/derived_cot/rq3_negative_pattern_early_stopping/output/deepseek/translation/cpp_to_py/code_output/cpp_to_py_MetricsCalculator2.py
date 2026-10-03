from typing import List, Tuple


def calculate_mrr(vec: List[int], k: int) -> float:
    """Find first occurrence of 1 in vec (0-indexed), return 1/(index+1) or 0."""
    try:
        idx = vec.index(1)
        return 1.0 / (idx + 1)
    except ValueError:
        return 0.0


def calculate_map(vec: List[int], k: int) -> float:
    """Compute average precision for a single query (not used by the class methods, but kept for completeness)."""
    total = 0.0
    count = 0
    for i, val in enumerate(vec):
        if val == 1:
            count += 1
            total += count / (i + 1)
    return total / count if count else 0.0


class MetricsCalculator2:
    @staticmethod
    def mrr(data: List[Tuple[List[int], int]]) -> Tuple[float, List[float]]:
        """
        Compute mean reciprocal rank over a list of (vector, k) pairs.
        Returns (average_mrr, list_of_individual_mrr).
        """
        if not data:
            return (0.0, [0.0])

        individual_mrr: List[float] = []
        sum_mrr = 0.0

        for vec, k in data:
            if k <= 0 or not vec:
                individual_mrr.append(0.0)
            else:
                mrr_val = calculate_mrr(vec, k)
                individual_mrr.append(mrr_val)
                sum_mrr += mrr_val

        average_mrr = sum_mrr / len(data)
        return (average_mrr, individual_mrr)

    @staticmethod
    def map(data: List[Tuple[List[int], int]]) -> Tuple[float, List[float]]:
        """
        Compute mean average precision over a list of (sub_list, total_num) pairs.
        Returns (mean_ap, list_of_individual_ap).
        """
        if not data:
            return (0.0, [0.0])

        separate_result: List[float] = []

        for sub_list, total_num in data:
            if total_num == 0:
                separate_result.append(0.0)
                continue

            length = len(sub_list)
            ranking_array = [1.0 / (i + 1) for i in range(length)]
            right_ranking_list = [0.0] * length
            count = 1

            for i, val in enumerate(sub_list):
                if val != 0:
                    right_ranking_list[i] = count
                    count += 1

            ap = sum(r * rrl for r, rrl in zip(ranking_array, right_ranking_list)) / total_num
            separate_result.append(ap)

        mean_ap = sum(separate_result) / len(separate_result)
        return (mean_ap, separate_result)