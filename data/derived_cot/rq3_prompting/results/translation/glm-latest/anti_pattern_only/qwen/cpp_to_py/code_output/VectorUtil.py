import math
from typing import Dict, Iterable, List, Mapping, Sequence


class VectorUtil:
    @staticmethod
    def _norm(vec: Sequence[float]) -> float:
        total = 0.0
        for val in vec:
            total += val * val
        return math.sqrt(total)

    @staticmethod
    def _normalize(vec: Sequence[float]) -> List[float]:
        vec_norm = VectorUtil._norm(vec)
        if vec_norm == 0.0:
            return [0.0] * len(vec)
        return [val / vec_norm for val in vec]

    @staticmethod
    def similarity(vector_1: Sequence[float], vector_2: Sequence[float]) -> float:
        norm_vec1 = VectorUtil._normalize(vector_1)
        norm_vec2 = VectorUtil._normalize(vector_2)
        dot_product = 0.0
        for a, b in zip(norm_vec1, norm_vec2):
            dot_product += a * b
        return dot_product

    @staticmethod
    def cosine_similarities(vector_1: Sequence[float],
                            vectors_all: Iterable[Sequence[float]]) -> List[float]:
        similarities: List[float] = []
        norm_vec1 = VectorUtil._norm(vector_1)

        for vec in vectors_all:
            norm_vec_all = VectorUtil._norm(vec)
            if norm_vec_all == 0.0:
                similarities.append(0.0)
                continue
            dot_product = 0.0
            for v, v1 in zip(vec, vector_1):
                dot_product += v * v1
            denominator = norm_vec1 * norm_vec_all
            if denominator == 0.0:
                # Mirror C++ IEEE-754 division by zero (inf/nan) instead of raising.
                similarity = (math.nan if dot_product == 0.0
                              else math.copysign(math.inf, dot_product))
            else:
                similarity = dot_product / denominator
            similarities.append(similarity)
        return similarities

    @staticmethod
    def n_similarity(vector_list_1: Sequence[Sequence[float]],
                     vector_list_2: Sequence[Sequence[float]]) -> float:
        if not vector_list_1 or not vector_list_2:
            raise ValueError("At least one of the lists is empty.")

        size_1 = len(vector_list_1)
        size_2 = len(vector_list_2)

        mean_vec1 = [sum(vec[i] for vec in vector_list_1) / size_1
                     for i in range(len(vector_list_1[0]))]
        mean_vec2 = [sum(vec[i] for vec in vector_list_2) / size_2
                     for i in range(len(vector_list_2[0]))]

        return VectorUtil.similarity(mean_vec1, mean_vec2)

    @staticmethod
    def compute_idf_weight_dict(total_num: int,
                                number_dict: Mapping[str, float]) -> Dict[str, float]:
        return {key: math.log((total_num + 1.0) / (count + 1.0))
                for key, count in number_dict.items()}