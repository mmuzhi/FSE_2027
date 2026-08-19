import math
from typing import Dict, List


def similarity(vector1: List[float], vector2: List[float]) -> float:
    dot_product = 0.0
    norm1 = 0.0
    norm2 = 0.0
    for i in range(len(vector1)):
        dot_product += vector1[i] * vector2[i]
        norm1 += vector1[i] ** 2
        norm2 += vector2[i] ** 2
    denominator = math.sqrt(norm1) * math.sqrt(norm2)
    return 0.0 if denominator == 0 else dot_product / denominator


def cosine_similarities(vector1: List[float], vectors_all: List[List[float]]) -> List[float]:
    similarities = []
    norm1 = math.sqrt(_dot_product(vector1, vector1))
    if norm1 == 0:
        for _ in range(len(vectors_all)):
            similarities.append(0.0)
        return similarities
    for vector2 in vectors_all:
        norm2 = math.sqrt(_dot_product(vector2, vector2))
        if norm2 == 0:
            similarities.append(0.0)
        else:
            sim = _dot_product(vector1, vector2) / (norm1 * norm2)
            similarities.append(sim)
    return similarities


def n_similarity(vector_list1: List[List[float]], vector_list2: List[List[float]]) -> float:
    if len(vector_list1) == 0 or len(vector_list2) == 0:
        raise ValueError("At least one of the passed lists is empty.")
    avg_vector1 = _average_vector(vector_list1)
    avg_vector2 = _average_vector(vector_list2)
    return similarity(avg_vector1, avg_vector2)


def compute_idf_weight_dict(total_num: int, number_dict: Dict[str, float]) -> Dict[str, float]:
    result = {}
    for key, count in number_dict.items():
        weight = math.log((total_num + 1) / (count + 1))
        result[key] = weight
    return result


def _dot_product(vector1: List[float], vector2: List[float]) -> float:
    result = 0.0
    for i in range(len(vector1)):
        result += vector1[i] * vector2[i]
    return result


def _average_vector(vectors: List[List[float]]) -> List[float]:
    avg_vector = [0.0] * len(vectors[0])
    for vector in vectors:
        for i in range(len(vector)):
            avg_vector[i] += vector[i]
    for i in range(len(avg_vector)):
        avg_vector[i] /= len(vectors)
    return avg_vector