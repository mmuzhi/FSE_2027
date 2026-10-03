import math
from typing import List, Dict, Union

def dot_product(vector1: List[float], vector2: List[float]) -> float:
    return sum(x * y for x, y in zip(vector1, vector2))

def similarity(vector1: List[float], vector2: List[float]) -> float:
    dot_product_val = dot_product(vector1, vector2)
    norm1 = math.sqrt(dot_product(vector1, vector1))
    norm2 = math.sqrt(dot_product(vector2, vector2))
    denominator = norm1 * norm2
    return 0.0 if denominator == 0 else dot_product_val / denominator

def cosine_similarities(vector1: List[float], vectors_all: List[List[float]]) -> List[float]:
    norm1 = math.sqrt(dot_product(vector1, vector1))
    if norm1 == 0:
        return [0.0] * len(vectors_all)
    similarities = []
    for vector2 in vectors_all:
        norm2 = math.sqrt(dot_product(vector2, vector2))
        if norm2 == 0:
            similarities.append(0.0)
        else:
            similarities.append(similarity(vector1, vector2))
    return similarities

def n_similarity(vector_list1: List[List[float]], vector_list2: List[List[float]]) -> float:
    if not vector_list1 or not vector_list2:
        raise ValueError("At least one of the passed lists is empty.")
    avg_vector1 = average_vector(vector_list1)
    avg_vector2 = average_vector(vector_list2)
    return similarity(avg_vector1, avg_vector2)

def average_vector(vectors: List[List[float]]) -> List[float]:
    if not vectors:
        raise ValueError("The list of vectors is empty.")
    n = len(vectors)
    m = len(vectors[0])
    avg = [0.0] * m
    for vector in vectors:
        for i, val in enumerate(vector):
            avg[i] += val
    return [val / n for val in avg]

def compute_idf_weight_dict(total_num: int, number_dict: Dict[str, float]) -> Dict[str, float]:
    result = {}
    for key, count in number_dict.items():
        weight = math.log((total_num + 1) / (count + 1))
        result[key] = weight
    return result