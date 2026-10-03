import math
from typing import Dict, List, Tuple, Union

class VectorUtil:
    @staticmethod
    def _norm(vec: List[float]) -> float:
        return math.sqrt(sum(v * v for v in vec))

    @staticmethod
    def _normalize(vec: List[float]) -> List[float]:
        n = VectorUtil._norm(vec)
        if n == 0.0:
            return [0.0] * len(vec)
        return [v / n for v in vec]

    @staticmethod
    def similarity(vector_1: List[float], vector_2: List[float]) -> float:
        norm1 = VectorUtil._normalize(vector_1)
        norm2 = VectorUtil._normalize(vector_2)
        return sum(a * b for a, b in zip(norm1, norm2))

    @staticmethod
    def cosine_similarities(vector_1: List[float], vectors_all: List[List[float]]) -> List[float]:
        norm_vec1 = VectorUtil._norm(vector_1)
        result = []
        for vec in vectors_all:
            norm_vec_all = VectorUtil._norm(vec)
            if norm_vec_all == 0.0:
                result.append(0.0)
                continue
            dot = sum(a * b for a, b in zip(vec, vector_1))
            result.append(dot / (norm_vec1 * norm_vec_all))
        return result

    @staticmethod
    def n_similarity(vector_list_1: List[List[float]], vector_list_2: List[List[float]]) -> float:
        if not vector_list_1 or not vector_list_2:
            raise ValueError("At least one of the lists is empty.")
        n = len(vector_list_1[0])
        mean1 = [0.0] * n
        mean2 = [0.0] * n
        for vec in vector_list_1:
            for i in range(n):
                mean1[i] += vec[i]
        for vec in vector_list_2:
            for i in range(n):
                mean2[i] += vec[i]
        for i in range(n):
            mean1[i] /= len(vector_list_1)
            mean2[i] /= len(vector_list_2)
        return VectorUtil.similarity(mean1, mean2)

    @staticmethod
    def compute_idf_weight_dict(total_num: int, number_dict: Dict[str, float]) -> Dict[str, float]:
        result = {}
        index_2_key_map = {}
        count_list = []
        idx = 0
        for key, count in number_dict.items():
            index_2_key_map[idx] = key
            count_list.append(count)
            idx += 1
        a = [math.log((total_num + 1.0) / (c + 1.0)) for c in count_list]
        for i, val in enumerate(a):
            result[index_2_key_map[i]] = val
        return result