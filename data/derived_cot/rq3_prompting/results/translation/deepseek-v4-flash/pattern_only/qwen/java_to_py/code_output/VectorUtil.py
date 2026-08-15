import math


class IllegalArgumentException(ValueError):
    pass


class VectorUtil:

    @staticmethod
    def similarity(vector1, vector2):
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
    def cosineSimilarities(vector1, vectorsAll):
        similarities = []
        norm1 = math.sqrt(VectorUtil._dotProduct(vector1, vector1))
        if norm1 == 0:
            for _ in vectorsAll:
                similarities.append(0.0)
            return similarities
        for vector2 in vectorsAll:
            norm2 = math.sqrt(VectorUtil._dotProduct(vector2, vector2))
            if norm2 == 0:
                similarities.append(0.0)
            else:
                similarities.append(
                    VectorUtil._dotProduct(vector1, vector2) / (norm1 * norm2)
                )
        return similarities

    @staticmethod
    def nSimilarity(vectorList1, vectorList2):
        if not vectorList1 or not vectorList2:
            raise IllegalArgumentException("At least one of the passed lists is empty.")
        avgVector1 = VectorUtil._averageVector(vectorList1)
        avgVector2 = VectorUtil._averageVector(vectorList2)
        return VectorUtil.similarity(avgVector1, avgVector2)

    @staticmethod
    def computeIdfWeightDict(totalNum, numberDict):
        result = {}
        for key, count in numberDict.items():
            count = float(count)
            denominator = count + 1.0
            if denominator == 0.0:
                numerator = float(VectorUtil._java_int_add(totalNum, 1))
                if numerator > 0:
                    value = float('inf')
                elif numerator < 0:
                    value = float('-inf')
                else:
                    value = float('nan')
            else:
                value = VectorUtil._java_int_add(totalNum, 1) / denominator
            result[key] = VectorUtil._log(value)
        return result

    @staticmethod
    def _dotProduct(vector1, vector2):
        result = 0.0
        for i in range(len(vector1)):
            result += vector1[i] * vector2[i]
        return result

    @staticmethod
    def _averageVector(vectors):
        avgVector = [0.0] * len(vectors[0])
        for vector in vectors:
            for i in range(len(vector)):
                avgVector[i] += vector[i]
        for i in range(len(avgVector)):
            avgVector[i] /= len(vectors)
        return avgVector

    @staticmethod
    def _log(value):
        if value == 0:
            return float('-inf')
        if value < 0:
            return float('nan')
        return math.log(value)

    @staticmethod
    def _java_int_add(a, b):
        result = a + b
        result &= 0xFFFFFFFF
        if result >= 0x80000000:
            result -= 0x100000000
        return result