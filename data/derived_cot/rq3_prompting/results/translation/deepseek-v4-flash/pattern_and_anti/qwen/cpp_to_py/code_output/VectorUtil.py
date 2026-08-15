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
        return sum(a * b for a, b in zip(norm_vec1, norm_vec2))

    @staticmethod
    def cosine_similarities(vector_1, vectors_all):
        similarities = []
        norm_vec1 = VectorUtil._norm(vector_1)

        for vec in vectors_all:
            norm_vec_all = VectorUtil._norm(vec)
            if norm_vec_all == 0.0:
                similarities.append(0.0)
                continue

            dot_product = sum(a * b for a, b in zip(vec, vector_1))

            if norm_vec1 == 0.0:
                similarities.append(float("nan"))
            else:
                similarities.append(dot_product / (norm_vec1 * norm_vec_all))

        return similarities

    @staticmethod
    def n_similarity(vector_list_1, vector_list_2):
        if not vector_list_1 or not vector_list_2:
            raise ValueError("At least one of the lists is empty.")

        n = len(vector_list_1[0])
        mean_vec1 = [0.0] * n
        mean_vec2 = [0.0] * n

        for vec in vector_list_1:
            for i, val in enumerate(vec):
                mean_vec1[i] += val

        for vec in vector_list_2:
            for i, val in enumerate(vec):
                mean_vec2[i] += val

        for i in range(n):
            mean_vec1[i] /= len(vector_list_1)
            mean_vec2[i] /= len(vector_list_2)

        return VectorUtil.similarity(mean_vec1, mean_vec2)

    @staticmethod
    def compute_idf_weight_dict(total_num, number_dict):
        result = {}
        for key, count in number_dict.items():
            result[key] = math.log((total_num + 1.0) / (count + 1.0))
        return result