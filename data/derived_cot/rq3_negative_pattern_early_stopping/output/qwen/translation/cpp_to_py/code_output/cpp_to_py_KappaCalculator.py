import numpy as np

class KappaCalculator:
    @staticmethod
    def kappa(test_data, k):
        data_mat = np.array(test_data, dtype=np.int32)
        rows, _ = data_mat.shape
        
        P0 = np.sum(np.diag(data_mat))
        total_sum = np.sum(data_mat)
        P0 /= total_sum
        
        row_sums = np.sum(data_mat, axis=1)
        col_sums = np.sum(data_mat, axis=0)
        pe_numerator = np.sum(row_sums * col_sums)
        pe_denominator = total_sum * total_sum
        pe = pe_numerator / pe_denominator
        
        cohens_coefficient = (P0 - pe) / (1 - pe)
        return cohens_coefficient

    @staticmethod
    def fleiss_kappa(test_data, N, k, n):
        data_mat = np.array(test_data, dtype=np.int32)
        rows, _ = data_mat.shape
        
        P0 = 0.0
        total_sum = 0.0
        
        for i in range(N):
            row = data_mat[i]
            row_sum = np.sum(row)
            total_sum += row_sum
            squared_sum = np.sum(np.square(row))
            temp = squared_sum - n
            temp /= (n - 1) * n
            P0 += temp
        
        P0 /= N
        
        col_sums = np.sum(data_mat, axis=0)
        pe = np.sum(np.square(col_sums / total_sum))
        
        ans = (P0 - pe) / (1 - pe)
        return ans