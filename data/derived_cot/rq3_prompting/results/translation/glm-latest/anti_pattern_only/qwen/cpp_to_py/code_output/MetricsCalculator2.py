from typing import List, Sequence, Tuple


def _calculate_mrr(vec: Sequence[int], k: int) -> float:
    # Note: k is unused, mirroring the C++ signature.
    try:
        index = vec.index(1)
    except ValueError:
        return 0.0
    return 1.0 / (index + 1)


def _calculate_map(vec: Sequence[int], k: int) -> float:
    # Note: k is unused, mirroring the C++ signature.
    # (This helper is unused in the original C++ as well.)
    total = 0.0
    count = 0
    for i in range(len(vec)):
        if vec[i] == 1:
            count += 1
            total += count / float(i + 1)
    return total / count if count else 0.0


class MetricsCalculator2:
    @staticmethod
    def mrr(data: List[Tuple[List[int], int]]) -> Tuple[float, List[float]]:
        if not data:
            return 0.0, [0.0]

        sum_mrr = 0.0
        individual_mrr: List[float] = []

        for vec, k in data:
            if k <= 0 or not vec:
                individual_mrr.append(0.0)
            else:
                mrr = _calculate_mrr(vec, k)
                individual_mrr.append(mrr)
                sum_mrr += mrr

        average_mrr = sum_mrr / len(data) if data else 0.0
        return average_mrr, individual_mrr

    @staticmethod
    def map(data: List[Tuple[List[int], int]]) -> Tuple[float, List[float]]:
        if not data:
            return 0.0, [0.0]

        separate_result: List[float] = []

        for sub_list, total_num in data:
            if total_num == 0:
                separate_result.append(0.0)
                continue

            length = len(sub_list)
            ranking_array = [1.0 / i for i in range(1, length + 1)]

            right_ranking_list: List[float] = [0.0] * length
            count = 1

            for i in range(length):
                if sub_list[i] != 0:
                    right_ranking_list[i] = count
                    count += 1

            ap = sum(
                (r * a for r, a in zip(right_ranking_list, ranking_array)),
                0.0,
            ) / total_num
            separate_result.append(ap)

        mean_ap = sum(separate_result, 0.0) / len(separate_result)
        return mean_ap, separate_result