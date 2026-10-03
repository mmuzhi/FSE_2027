import math
from typing import List, Dict

class VectorUtil:
    @staticmethod
    def norm(vec: List[float]) -> float:
        """Calculate the Euclidean norm of a vector."""
        sum_sq = sum(x * x for x in vec)
        return math.sqrt(sum_sq) if sum_sq != 0 else 0.0

    @staticmethod
    def normalize(vec: List[float]) -> List[float]:
        """Normalize a vector to unit length or return zero vector if norm is zero."""
        vec_norm = VectorUtil.norm(vec)
        if vec_norm == 0.0:
            return vec[:]  # Return a copy of the zero vector
        return [x / vec_norm for x in vec]

    @staticmethod
    def similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        norm1 = VectorUtil.norm(vec1)
        norm2 = VectorUtil.norm(vec2)
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        dot_product = sum(x * y for x, y in zip(vec1, vec2))
        return dot_product / (norm1 * norm2)

    @staticmethod
    def cosine_similarities(vec: List[float], vec_list: List[List[float]]) -> List[float]:
        """Calculate cosine similarities between a vector and a list of vectors."""
        norm_vec = VectorUtil.norm(vec)
        result = []
        for v in vec_list:
            norm_v = VectorUtil.norm(v)
            if norm_v == 0.0:
                result.append(0.0)
                continue
            dot_product = sum(x * y for x, y in zip(vec, v))
            result.append(dot_product / (norm_vec * norm_v))
        return result

    @staticmethod
    def n_similarity(vec_list1: List[List[float]], vec_list2: List[List[float]]) -> float:
        """Calculate the cosine similarity between the means of two lists of vectors."""
        if not vec_list1 or not vec_list2:
            raise ValueError("At least one of the lists is empty.")
        mean1 = [0.0] * len(vec_list1[0])
        mean2 = [0.0] * len(vec_list1[0])
        for v in vec_list1:
            for i in range(len(v)):
                mean1[i] += v[i]
        for v in vec_list2:
            for i in range(len(v)):
                mean2[i] += v[i]
        for i in range(len(mean1)):
            mean1[i] /= len(vec_list1)
            mean2[i] /= len(vec_list2)
        return VectorUtil.similarity(mean1, mean2)

    @staticmethod
    def compute_idf_weight_dict(total_num: int, number_dict: Dict[str, float]) -> Dict[str, float]:
        """Compute IDF weights for a dictionary of term counts."""
        index_2_key_map = {}
        count_list = []
        for idx, (key, count) in enumerate(number_dict.items()):
            index_2_key_map[idx] = key
            count_list.append(count)
        a = [math.log((total_num + 1.0) / (count + 1.0)) for count in count_list]
        result = {index_2_key_map[i]: a[i] for i in range(len(a))}
        return result