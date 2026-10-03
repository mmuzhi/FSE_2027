import math
from typing import List, Dict


class VectorUtil:

    @staticmethod
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

    @staticmethod
    def cosineSimilarities(vector1: List[float], vectorsAll: List[List[float]]) -> List[float]:
        similarities = []
        norm1 = math.sqrt(VectorUtil._dotProduct(vector1, vector1))
        if norm1 == 0:
            for i in range(len(vectorsAll)):
                similarities.append(0.0)
            return similarities
        for vector2 in vectorsAll:
            norm2 = math.sqrt(VectorUtil._dotProduct(vector2, vector2))
            if norm2 == 0:
                similarities.append(0.0)
            else:
                similarity = VectorUtil._dotProduct(vector1, vector2) / (norm1 * norm2)
                similarities.append(similarity)
        return similarities

    @staticmethod
    def nSimilarity(vectorList1: List[List[float]], vectorList2: List[List[float]]) -> float:
        if not vectorList1 or not vectorList2:
            raise ValueError("At least one of the passed lists is empty.")
        avgVector1 = VectorUtil._averageVector(vectorList1)
        avgVector2 = VectorUtil._averageVector(vectorList2)
        return VectorUtil.similarity(avgVector1, avgVector2)

    @staticmethod
    def computeIdfWeightDict(totalNum: int, numberDict: Dict[str, float]) -> Dict[str, float]:
        result = {}
        for key, count in numberDict.items():
            weight = math.log((totalNum + 1) / (count + 1))
            result[key] = weight
        return result

    @staticmethod
    def _dotProduct(vector1: List[float], vector2: List[float]) -> float:
        result = 0.0
        for i in range(len(vector1)):
            result += vector1[i] * vector2[i]
        return result

    @staticmethod
    def _averageVector(vectors: List[List[float]]) -> List[float]:
        avgVector = [0.0] * len(vectors[0])
        for vector in vectors:
            for i in range(len(vector)):
                avgVector[i] += vector[i]
        for i in range(len(avgVector)):
            avgVector[i] /= len(vectors)
        return avgVector