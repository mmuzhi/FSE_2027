import math


class VectorUtil:

    @staticmethod
    def _norm(vec):
        return math.sqrt(sum(val * val for val in vec))

    @staticmethod
    def _normalize(vec):
        vec_norm = VectorUtil._norm(vec)
        if vec_norm == 0.0:
            return [0.0] * len(vec)
        return [val / vec_norm for val in vec]

    @staticmethod
    def similarity(vector_1, vector_2):
        norm_vec1 = VectorUtil._normalize(vector_1)
        norm_vec2 = VectorUtil._normalize(vector_2)
        dot_product = 0.0
        for a, b in zip(norm_vec1, norm_vec2):
            dot_product += a * b
        return dot_product

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        similarities = []
        norm_vec1 = VectorUtil._norm(vector_1)

        for vec in vectors_all:
            norm_vec_all = VectorUtil._norm(vec)
            if norm_vec_all == 0.0:
                similarities.append(0.0)
                continue
            dot_product = 0.0
            for a, b in zip(vec, vector_1):
                dot_product += a * b
            denom = norm_vec1 * norm_vec_all
            if denom == 0.0:
                # Match C++ IEEE-754 double division-by-zero semantics
                if dot_product == 0.0:
                    similarity = float('nan')
                else:
                    similarity = math.copysign(math.inf, dot_product)
            else:
                similarity = dot_product / denom
            similarities.append(similarity)
        return similarities

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        if not vector_list_1 or not vector_list_2:
            raise ValueError("At least one of the lists is empty.")

        n = len(vector_list_1[0])
        mean_vec1 = [0.0] * n
        mean_vec2 = [0.0] * n

        for vec in vector_list_1:
            for i in range(n):
                mean_vec1[i] += vec[i]
        for vec in vector_list_2:
            for i in range(n):
                mean_vec2[i] += vec[i]

        len1 = len(vector_list_1)
        len2 = len(vector_list_2)
        for i in range(n):
            mean_vec1[i] /= len1
            mean_vec2[i] /= len2

        return VectorUtil.similarity(mean_vec1, mean_vec2)

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        result = {}
        for key, count in number_dict.items():
            result[key] = math.log((total_num + 1.0) / (count + 1.0))
        return result